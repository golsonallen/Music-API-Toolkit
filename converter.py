import requests
import json

#authenticate requests
def get_token():
    url = "https://accounts.spotify.com/api/token"
    encoded_id_and_secret = "YTY1Mzg1YmE2ZGI1NGZlN2E4YzI5ZDg4NmQ5MmY5MjA6NDY0ZTg4ZWY1YTNjNDQ1YzkzZTI2YzI3ZWNiZTFkZGM="
    headers = {"Authorization": "Basic " + encoded_id_and_secret}
    data = {"grant_type": "client_credentials"}
    token_response = requests.request(method = "POST", url = url, headers = headers, data = data)
    token = token_response.json()["access_token"]
    return token

temp_token = "BQAbI1vuqT9-cXHFRIOKXOGkeH6ck1yV9JTGmf5A6js32Ftib7JLSQRZA74v7fEz42Z6QsWPQOV1_c77bcM"

def get_spotify_ID():
    url = input("Please enter the song's URL: ")
    ID = url.split("/")[-1].split("?")[0]
    return ID

def get_song_name():
    token = get_token()
    url = "https://api.spotify.com/v1/tracks/" + get_spotify_ID()
    headers = {"Authorization": "Bearer " + token}
    song_response = requests.request(method = "GET", url = url, headers = headers)
    song_title = song_response.json()["name"]
    song_popularity = song_response.json()["popularity"]
    return song_title, song_popularity

def open_song():
    import os
    os.system("open \"\" https://music.apple.com/us/browse")

print(get_song_name())
#open_song()