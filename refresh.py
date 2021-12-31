#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Leonardo Dantas
# Created Date: 12/30/2021
# version ='1.0'
# ---------------------------------------------------------------------------
'''Gets refreshed token'''
# ---------------------------------------------------------------------------

from secrets import refresh_token, base_64
import requests
import json
class Refresh:
	def __init__(self):
		'''initializes request with client:client_secret is base64 and using the refresh token'''
		self.refresh_token = refresh_token
		self.base_64 = base_64

	def ref_token(self):
		'''refreshes token making a POST request to spotify'''
		query = "https://accounts.spotify.com/api/token"
		response = requests.post(query,
			data = {"grant_type":"refresh_token", "refresh_token": refresh_token},
			headers = {"Authorization": "Basic " + base_64})
		return response.json()["access_token"]
