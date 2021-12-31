# Setup
This works using python3 so make sure to download the latest version and install the following libraries using: </br>
```python -m pip install websockets requests```

Download the full repository and fill up the values in secrets.py

# Spotify
For spotify make sure to get your spotify username, your refresh token and your enconded client id and secret from your App. </br>
The scope rquired for modifying the player is "user-modify-playback-state". </br>
To encode your id and secret usiung this website https://www.base64encode.org/ this should be in the client_id:client_secret form.

# Twitch
For twitch, get your client_id, client_secret, refresh_tokan and channel_id. For the bearer token the required scope is "channel:read:redemptions" you need a USER access token.</br>

# Running
To run the "bot" go into the folder where the scripts live and run </br>
```python main.py```

# Acknowledgements
This integration is based on the codes from:
- https://github.com/EuanMorgan/SpotifyDiscoverWeeklyRescuer
- https://github.com/SlackingVeteran/twitch-pubsub

