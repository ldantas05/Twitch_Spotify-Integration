#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Leonardo Dantas
# Created Date: 12/30/2021
# version ='1.0'
# ---------------------------------------------------------------------------
'''Defines SpotifyBot object and methods'''
# ---------------------------------------------------------------------------

import json
import requests
import urllib.parse
import time
import datetime
from secrets import spotify_username
from refresh import Refresh

class SpotifyBot:
	def __init__(self):
		'''initializes "Bot" with new oauth token'''
		self.spotify_token = ""
		self.refresh_token()
		self.expiration = (datetime.datetime.now() + datetime.timedelta(0, 3500))

	def search_track(self, song, artist):
		'''searches for track in spotify libary and returns Spotify Song URI, args(song=string, artist=string)'''
		encoded_song = urllib.parse.quote("artist:{} track:{}".format(artist,song))
		type_search = "track"
		query = "https://api.spotify.com/v1/search?q={}&type={}&limit=1".format(encoded_song, type_search)
		response = requests.get(query,
								headers = {"Content-Type": "application/json",
								"Authorization": "Bearer {}".format(self.spotify_token)})
		response_json = response.json()
		return response_json

	def add_to_queue(self, track_id):
		'''adds song to the user queue, args(track_id = string), trakc_id is Spotify Uri'''
		encoded_track = urllib.parse.quote(track_id)
		query = "https://api.spotify.com/v1/me/player/queue?uri={}".format(encoded_track)
		response = requests.post(query,
								headers= {"Content-Type":"application/json",
								"Authorization": "Bearer {}".format(self.spotify_token)})
	
	def next_track(self):
		'''skips to the next song'''
		query = "https://api.spotify.com/v1/me/player/next"
		response = requests.post(query,
								headers= {"Content-Type":"application/json",
								"Authorization": "Bearer {}".format(self.spotify_token)})

	
	def refresh_token(self):
		'''refreshes bearer token'''
		refreshCaller = Refresh()
		self.spotify_token = refreshCaller.ref_token()
		self.expiration = (datetime.datetime.now() + datetime.timedelta(0, 3500))



