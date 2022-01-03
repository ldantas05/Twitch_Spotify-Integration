#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Leonardo Dantas
# Created Date: 12/30/2021
# version ='1.0'
# ---------------------------------------------------------------------------
'''Main module that integrates the twitch API and Spotify API'''
# ---------------------------------------------------------------------------

from spoty import SpotifyBot
import asyncio
import datetime
from twitchbot import WebSocket 

async def run_requests(spot_bot, client):
	'''Search song and add it to the queue, args(spot_bot = SpotifyBot Object, client = Websocket Object)
	verifies if spotify token is valid and refreshes it if it is not valid'''
	while True:
		while len(client.get_queue()) != 0:
			if(datetime.datetime.now() >= spot_bot.expiration):
				print("Refreshing token...")
				spot_bot.refresh_token()
				print("Token refreshed!")
			redemption = client.dequeue()
			if(redemption[0] == 1):
				spot_bot.next_track()
				print("Next song!")
			elif(redemption[0] == 2):
				search_song = redemption[1].split(",")
				response = spot_bot.search_track(search_song[0], search_song[1])
				if len(response["tracks"]["items"]) == 0:
					print("Could not find {} by {}".format(search_song[0], search_song[1]))
					continue
				else:
					trackId = response["tracks"]["items"][0]["uri"]
					print("Song added to queue: {} by {}".format(search_song[0], search_song[1]))
					spot_bot.add_to_queue(trackId)
		await asyncio.sleep(5)



if __name__== "__main__":
	spot_bot = SpotifyBot()
	client = WebSocket()
	loop = asyncio.get_event_loop()
	connection = loop.run_until_complete(client.connect())
	tasks = [asyncio.ensure_future(client.heartbeat(connection)),
		asyncio.ensure_future(client.receiveMessage(connection)),
		asyncio.ensure_future(run_requests(spot_bot, client))
	]
	loop.run_until_complete(asyncio.wait(tasks))
