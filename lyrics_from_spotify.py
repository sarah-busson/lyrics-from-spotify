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
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import re
import lyricsgenius

class GetLyrics:

    def __init__(self):
        self.sp = self.get_spotify_auth()

# Step 0: Set up the Spotify Authorization
    def get_spotify_auth(self):
        spotify_client = os.environ.get('SPOTIFY_CLIENT')
        spotify_secret = os.environ.get('SPOTIFY_SECRET')
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client,  
                                               client_secret=spotify_secret,
                                               redirect_uri='http://localhost:8888/callback/',
                                               scope='user-read-currently-playing'))
        return sp
# Step 1: Get the song currently playing on Spotify
    def get_playing_song(self):
        #SPOTIFY REQUEST
        current_song = self.sp.currently_playing(market='FR', additional_types='track')
        flat_df = pd.io.json.json_normalize(current_song)
        #TRACK NAME
        track_name = flat_df['item.name'][0]
        #TRACK ARTIST (only the main artist)
        track_artist = flat_df['item.artists'][0][0]['name']
        #PLAYLIST
        """Has to be played from a playlist, not from 'Liked Songs',
        json response is a different format"""
        playlist = re.split(':', flat_df['context.uri'][0])[2]

        return track_name, track_artist, playlist
    
# Step 2: Get the song lyrics from web scrapping google lyrics
    def get_lyrics(self):
        genius = lyricsgenius.Genius(os.environ.get('GENIUS_TOKEN'))
        track_name, track_artist, playlist = self.get_playing_song()
        song = genius.search_song(track_name, track_artist, get_full_info=False)
        lyrics = song.lyrics
        return print(lyrics)

"""# Step 3: Send the lyrics via WhatsApp
    def send_lyrics(self, lyrics):
        print(lyrics)"""



if __name__ == '__main__':
    gl = GetLyrics()
    gl.get_lyrics()