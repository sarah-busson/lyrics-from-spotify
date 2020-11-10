"""
Step 1 
Connect to Spotify and GET Player

Step 2
API to Genius 
OR scrap the lyrics ?

Step 3
Connect to WhatsApp and send the lyrics

Step 4
-> Do this for every song or for a playlist called SongstoSing??
"""
import json
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up the Spotify Authorization
spotify_client = os.environ.get('SPOTIFY_CLIENT')
spotify_secret = os.environ.get('SPOTIFY_SECRET')
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client,  
                                               client_secret=spotify_secret,
                                               redirect_uri='http://localhost:8888/callback/',
                                               scope='user-read-currently-playing'))

class GetLyrics:

    def __init__(self):
        pass

# Step 1 : Get the song currently playing on Spotify
    # Playlist ID:
    songs_to_sing = '7tPSBvTBEh7qJ4X192u9uP'

    def get_playing_song(self):
        current_song = sp.currently_playing(market='FR', additional_types='track')
        return current_song #json format
        
""" 
Now make sure that the playlist match, 
then collect title and artist 
then use it in Genius API OR scrap the genius website
then collect the lyrics or send the link ??
then connect to WhatsApp
then send lyrics or link via text
"""


