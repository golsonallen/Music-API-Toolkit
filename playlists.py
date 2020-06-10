import requests
import json
import pandas as pd 
from converter import get_token
from secrets import userID

class PlaylistOptimizer:

    def __init__(self):
        self.userID = userID
        self.token = get_token()

    #gets the users ID
    def get_user_ID(self):
        pass

    #creates a new playlist for the most popular songs from the user's given playlist
    def create_master_playlist(self):
        url = "https://api.spotify.com/v1/users/{}/playlists".format(self.userID)
        headers = {"Authorization": "Bearer {}".format(self.token), "Content-Type": "application/json"}
        body = {"name": "Master Playlist", "public": False}
        master_playlist = requests.post(url = url, headers = headers, data = body)
        return master_playlist.json()

    #prompts user for a link to a playlist, returns playlist ID
    def get_playlist_ID(self):
        playlist_url = "https://open.spotify.com/playlist/55LKDwMXAvVqKAP5ynQqw9"
        #playlistID = input("Please enter the link to the playlist you would like to optimize:")
        playlistID = playlist_url.split("/")[-1]
        return playlistID

    #get the playlist's items, an array of track objects
    def get_playlist_songs(self, playlistID):
        url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlistID)
        headers = {"Authorization": "Bearer {}".format(self.token)}
        params = {"limit": "100"}
        playlist_response = requests.get(url = url, headers = headers, params=params)
        #print(json.dumps(playlist_response.json(), indent=4))
        return playlist_response.json()

    #adds a track to master playlist if track's popularity is above threshold
    def add_to_master(self, playlist_songs, threshold):
        song_list = playlist_songs["items"]
        songs = {}
        songs["Title"] = []
        songs["Popularity"] = []
        for song in song_list:
            #print(song["track"]["name"], song["track"]["popularity"])
            if int(song["track"]["popularity"]) > threshold:
                #add to master playlist
                pass


    def main(self):
        playlistID = self.get_playlist_ID()
        songs = self.get_playlist_songs(playlistID)
        self.add_to_master(songs, 70)
        

playlist = PlaylistOptimizer()
playlist.main() 