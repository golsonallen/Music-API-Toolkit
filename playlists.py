import requests
import json
from secrets import userID
from secrets import token

class PlaylistOptimizer:

    def __init__(self):
        self.userID = userID
        self.token = token

    #creates a new playlist for the most popular songs from the user's given playlist
    def create_new_playlist(self):
        name = input("Please enter the name for the new optimized playlist: ")
        url = "https://api.spotify.com/v1/users/{}/playlists".format(self.userID)
        headers = {
            "Authorization": "Bearer {}".format(self.token), 
            "Content-Type": "application/json"
        }
        body = json.dumps({
            "name": name, 
            "public": False
        })
        new_playlist = requests.post(url = url, headers = headers, data = body)
        return new_playlist.json()["id"]
    
    #prompts user for a link to a playlist, returns playlist ID
    def get_playlist_ID(self):
        playlistURL = input("Please enter the playlist's link: ")
        playlistID = playlistURL.split("/")[-1]
        return playlistID

    #get the playlist's items, an array of track objects
    def get_playlist_songs(self, limit):
        old_playlistID = self.get_playlist_ID()
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
    def check_songs_popularity(self, limit, threshold):
        songs_data = self.get_playlist_songs(limit)
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
        print("Enter (1) to create a new playlist or (2) to add songs to an existing playlist")
        choice = int(input("Choice: "))
        if choice == 1:
            new_playlistID = self.create_new_playlist()
        else:
            print("For the playlist you would like to add songs to,", end = " ")
            new_playlistID = self.get_playlist_ID()
        print("Optimizing playlist....")
        songs_to_add = self.check_songs_popularity(limit = 100, threshold = 77)
        self.add_songs(songs_to_add, new_playlistID)
        print("Finished")

playlist = PlaylistOptimizer()
playlist.main()