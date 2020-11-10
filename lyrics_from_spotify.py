"""
Step 1 
Connect to Spotify and GET Player

Step 2
Scrap the lyrics (on google)

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

# Step 1: Get the song currently playing on Spotify
    # Playlist ID:
    songs_to_sing = '7tPSBvTBEh7qJ4X192u9uP'

    def get_playing_song(self):
        #SPOTIFY REQUEST
        current_song = sp.currently_playing(market='FR', additional_types='track')
        flat_df = pd.io.json.json_normalize(current_song)
        #TRACK NAME
        track_name = flat_df['item.name'][0]
        #TRACK ARTIST (only the main artist)
        track_artist = flat_df['item.artists'][0][0]['name']
        #PLAYLIST
        playlist = re.split(':', flat_df['context.uri'][0])[2]

        return track_name, track_artist, playlist
    
# Step 2: Get the song lyrics from web scrapping google lyrics




""" 
Now make sure that the playlist match, WAIT
then collect title and artist           V
then scrap the google lyrics            
then collect the lyrics or send the link ??
then connect to WhatsApp
then send lyrics or link via text
"""


