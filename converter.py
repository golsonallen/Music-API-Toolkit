import requests
import json
from secrets import encoded_id_and_secret
from selenium import webdriver
import time

#authenticate requests
def get_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + encoded_id_and_secret}
    data = {"grant_type": "client_credentials"}
    token_response = requests.request(method = "POST", url = url, headers = headers, data = data)
    token = token_response.json()["access_token"]
    return token

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
    #song_pop = song_response.json()["popularity"]
    return song_title

class AppleMusic:

    def __init__(self):
        self.driver = webdriver.Safari()
        #pause to give the site time to log me in
        
    def open_apple_music(self):
        self.driver.get("https://music.apple.com/browse")

    def login(self):
        login_buttom = self.driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/button')
        login_buttom.click()
        time.sleep(20)

        # Switch frame by id
        self.driver.switch_to.frame((self.driver.find_elements_by_tag_name("iframe")[1]))

        # Now click on button
        soundcloud_id_sign_in = self.driver.find_element_by_xpath('//*[@id="account_name_text_field"]')
        soundcloud_id_sign_in.send_keys("golsonallen@yahoo.com")

        #apple_id_sign_in = self.driver.find_element_by_xpath('//*[@id="sign_in_up_email"]')
        #apple_id_sign_in.send_keys("golsonallen@yahoo.com")
        #sign_in_buttom = self.driver.find_element_by_xpath('//*[@id="sign-in"]')
        #sign_in_buttom.click()

    def search_song_title(self):
        pass

    def play_song(self):
        pass

    def main(self):
        self.open_apple_music()
        time.sleep(12)
        self.login()

#print(get_song_name())
#converter = AppleMusic()
#converter.main()