"""
Step 1 
Get the song currently playing on Spotify

Step 2
Get the lyrics via Genius

Step 3
Connect to WhatsApp and send the lyrics

Step 4
Do this for every song playedd in the Karaoke playlist
"""
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import re
import lyricsgenius
from twilio.rest import Client 
import time

class GetLyrics:

    def __init__(self):
        self.sp = self.get_spotify_auth()
        self.client = self.get_twilio_auth()
        self.track_name, self.track_artist, self.playlist = self.get_playing_song()

# Step 0: Set up the Spotify and Twilio Authorization
    def get_spotify_auth(self):
        spotify_client = os.environ.get('SPOTIFY_CLIENT')
        spotify_secret = os.environ.get('SPOTIFY_SECRET')
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client,  
                                               client_secret=spotify_secret,
                                               redirect_uri='http://localhost:8888/callback/',
                                               scope='user-read-currently-playing'))
        return sp

    def get_twilio_auth(self):
        account_sid = os.environ.get('TWILIO_ACCOUNT')
        auth_token = os.environ.get('TWILIO_TOKEN') 
        client = Client(account_sid, auth_token) 
        return client
 
# Step 1: Get the song currently playing on Spotify
    def get_playing_song(self):
        #SPOTIFY REQUEST
        current_song = self.sp.currently_playing(market='FR', additional_types='track')
        flat_df = pd.json_normalize(current_song)
        #TRACK NAME
        track_name = flat_df['item.name'][0]
        #TRACK ARTIST (only the main artist)
        track_artist = flat_df['item.artists'][0][0]['name']
        #PLAYLIST
        """Has to be played from a playlist, not from 'Liked Songs',
        json response is a different format"""
        playlist = re.split('/', flat_df['context.href'][0])[5]

        return track_name, track_artist, playlist
    
# Step 2: Get the song lyrics from web scrapping google lyrics
    def get_lyrics(self):
        genius = lyricsgenius.Genius(os.environ.get('GENIUS_TOKEN'))
        track_name, track_artist, playlist = self.get_playing_song()
        song = genius.search_song(track_name, track_artist, get_full_info=False)
        lyrics = song.lyrics
        return lyrics

# Step 3: Send the lyrics via WhatsApp
    def send_lyrics(self):
        track_name, track_artist, playlist = self.get_playing_song()

        lyrics_gross = self.get_lyrics()
        lyrics = re.sub('\[.*\]', '\n', lyrics_gross)
        lyrics = re.sub('\n\n+', '\n\n', lyrics)

        karaoke = 'Karaoke time! 🎙\nPlaying {} from {}{}'.format(track_name, track_artist, lyrics)
        if len(karaoke) > 4199 : #text limit is 1600 characters
            message1 = self.client.messages.create(
                     from_= 'whatsapp:+14155238886', #TWILIO's WhatsApp number 
                     body= karaoke[:1599],
                     to= 'whatsapp:' + os.environ.get('SARAH_NUMBER')) 
            message2 = self.client.messages.create(
                     from_= 'whatsapp:+14155238886', #TWILIO's WhatsApp number 
                     body= karaoke[1599:3199],   
                     to= 'whatsapp:' + os.environ.get('SARAH_NUMBER'))
            message3 = self.client.messages.create(
                     from_= 'whatsapp:+14155238886', #TWILIO's WhatsApp number 
                     body= karaoke[3199:],   
                     to= 'whatsapp:' + os.environ.get('SARAH_NUMBER')) 
        elif len(karaoke) > 1599 :
            message1 = self.client.messages.create(
                     from_= 'whatsapp:+14155238886', #TWILIO's WhatsApp number 
                     body= karaoke[:1599],
                     to= 'whatsapp:' + os.environ.get('SARAH_NUMBER')) 
            message2 = self.client.messages.create(
                     from_= 'whatsapp:+14155238886', #TWILIO's WhatsApp number 
                     body= karaoke[1599:],   
                     to= 'whatsapp:' + os.environ.get('SARAH_NUMBER'))
        else:
            message = self.client.messages.create(
                     from_= 'whatsapp:+14155238886', #TWILIO's WhatsApp number 
                     body= karaoke,   
                     to= 'whatsapp:' + os.environ.get('SARAH_NUMBER')) 

if __name__ == '__main__':
    gl = GetLyrics()
    
    while True:
        if gl.get_playing_song()[2] == '7tPSBvTBEh7qJ4X192u9uP': #Karaoke playlist ID on my Spotify account
            karaoke_playlist = True
            gl.send_lyrics()
            previous_song = gl.get_playing_song()[0]
        else:
            karaoke_playlist = False
            time.sleep(10)
    
        while karaoke_playlist == True:
            playing_song = gl.get_playing_song()[0]
            if gl.get_playing_song()[2] == '7tPSBvTBEh7qJ4X192u9uP' and previous_song != playing_song:
                gl.send_lyrics()
                previous_song = playing_song
                time.sleep(10)
            elif gl.get_playing_song()[2] != '7tPSBvTBEh7qJ4X192u9uP':
                karaoke_playlist = False
            else:
                time.sleep(10)
