import requests
import json
import pandas as pd
from secrets import userID
from secrets import token

class PlaylistOptimizer:

    def __init__(self):
        self.userID = userID
        self.token = token

    #creates a new playlist for the most popular songs from the user's given playlist
    def create_new_playlist(self, name):
        url = "https://api.spotify.com/v1/users/{}/playlists".format(self.userID)
        headers = {
            "Authorization": "Bearer {}".format(self.token), 
            "Content-Type": "application/json"
        }
        body = json.dumps({
            "name": name, 
            "public": False
        })
        master_playlist = requests.post(url = url, headers = headers, data = body)
        return master_playlist.json()["id"]
    
    #prompts user for a link to a playlist, returns playlist ID
    def get_playlist_ID(self):
        playlistURL = input("Please enter the link to the playlist you would like to optimize: ")
        playlistID = playlistURL.split("/")[-1]
        return playlistID

    #get the playlist's items, an array of track objects
    def get_playlist_songs(self, old_playlistID, limit):
        url = "https://api.spotify.com/v1/playlists/{}/tracks".format(old_playlistID)
        headers = {
            "Authorization": "Bearer {}".format(self.token),
            "Content-Type": "application/json"
        }
        params = {
            "limit": str(limit)
        } 
        playlist_response = requests.get(url = url, headers = headers, params=params)
        #print(json.dumps(playlist_response.json(), indent=4))
        return playlist_response.json()["tracks"]["items"]

    #adds a track to list of songs to add if track's popularity is above threshold
    def check_songs(self, songs_data, threshold):
        songs_to_add = []
        for song in songs_data:
            if int(song["track"]["popularity"]) > threshold:
                songs_to_add.append(song["track"]["uri"])
        return songs_to_add
        
    #adds the list of songs to the playlist
    def add_songs(self, songs_to_add, new_playlistID):
        url = "https://api.spotify.com/v1/playlists/{}/tracks".format(new_playlistID)
        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }
        body = json.dumps({
            "uris": songs_to_add
        })
        requests.post(url = url, headers = headers, data=body)

    def main(self):
        print("Welcome to Playlist Optimizer!")
        new_playlist_name = input("Please enter the name for the new optimized playlist: ")
        new_playlistID = self.create_new_playlist(new_playlist_name)
        newID = self.get_playlist_ID()
        print("Optimizing playlist....")
        song_data = self.get_playlist_songs(newID, limit = 3)
        songs_to_add = self.check_songs(song_data, threshold = 77)
        self.add_songs(songs_to_add, new_playlistID)
        print("Finished")

playlist = PlaylistOptimizer()
playlist.main()