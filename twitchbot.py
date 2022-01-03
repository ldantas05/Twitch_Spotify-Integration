#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Leonardo Dantas
# Created Date: 12/30/2021
# version ='1.0'
# ---------------------------------------------------------------------------
'''Defines Websocket object and methods'''
# ---------------------------------------------------------------------------

import websockets
import json
import asyncio
import uuid
import requests
from secrets import client_id, channel_id, client_secret, twitch_refresh

class WebSocket:
	def __init__(self):
		'''initializes websocket to pubsub'''
		self.client_id = client_id
		self.channel_id = channel_id
		self.client_secret = client_secret
		self.access_token = ""
		self.get_oauth()
		self.queue = []
		self.url = "wss://pubsub-edge.twitch.tv"
		self.loop = asyncio.get_event_loop()

	def get_oauth(self):
		'''gets oauth, lasts 4 hours'''
		query = "https://id.twitch.tv/oauth2/token?grant_type=refresh_token"
		query += "&refresh_token={}".format(twitch_refresh)
		query+= "&client_id={}".format(self.client_id)
		query += "&client_secret={}".format(self.client_secret)
		response = requests.post(query)
		self.access_token = response.json()["access_token"]
	
	def get_queue(self):
		'''returns request queue'''
		return self.queue

	def dequeue(self):
		'''dequeues requests'''
		return self.queue.pop(0)

	
	async def connect(self):
		'''connects to the websocket and listens'''
		self.connection = await websockets.connect(self.url)
		nonce = uuid.uuid1().hex
		if self.connection.open:
			print("Connecting...")
			data = json.dumps({
				"type": "LISTEN",
				"nonce": str(nonce),
				"data": {
				"topics": ["channel-points-channel-v1."+str(self.channel_id)],
				"auth_token": self.access_token}
				})
			await self.sendMessage(data)
			resp = await self.connection.recv()
			print("Connected!")
			return self.connection

	async def sendMessage(self, message):
		'''method used to send PING message'''
		await self.connection.send(message)

	async def receiveMessage(self, connection):
		'''method that listens for channel point redemptions and adds to queue if there is a song request or a next song request'''
		while True:
			try:
				message = await connection.recv()
				if "PONG" not in message:
					print(message)
					if "Next song" in message:
						print("Next song request")
						self.queue.append((1,0))
					elif "Request a Song" in message:
						#received message from the socket gets parsed to get the user input
						message = json.loads(message)
						message = json.loads(message['data']['message'])
						message = message['data']['redemption']['user_input']
						print("Song add requested "+message)
						self.queue.append((2, message))
				await asyncio.sleep(3)
			except:
				break


	async def heartbeat(self, connection):
		'''function used to ping the server every 10 seconds to avoid connection from closing'''
		while True:
			try:
				ping = json.dumps({"type":"PING"})
				await connection.send(ping)
				await asyncio.sleep(10)
			except websockets.exceptions.ConnectionClosed:
				print("Server connection lost")
				break
	
