import spotipy, os, sys, json, spotipy, webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyOAuth


with open("config.json", "r") as f:
    config = json.load(f)


os.environ["SPOTIPY_CLIENT_ID"] = config["client_id"]
os.environ["SPOTIPY_CLIENT_SECRET"] = config["client_secret"]
os.environ["SPOTIPY_REDIRECT_URI"] = "http://google.com/"


try:
    token = util.prompt_for_user_token(config["username"])
except:
    token = util.prompt_for_user_token(config["username"])


sp=spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private"))


def checkPlaylist(sp, playlist):
    playlists = sp.current_user_playlists()                          
    user_id = sp.me()['id']
    for plist in playlists['items']:
        if playlist == plist['name']:
            return True
    return False


##########################################################################################
#Take all songs from one playlist and add it to another playlist, alphabetically by artist
##########################################################################################
def addPlaylist(sp):

    playlists = sp.current_user_playlists()    
    user_id = sp.me()['id']                       
    print(sp.me()['display_name'])    
    print()
    for playlist in playlists['items']:    
        if playlist['owner']['id'] == user_id:                                                                                          
            print(playlist['name'], ':', playlist['tracks']['total'])
    print()

    while True:
        source = input('Which playlist do you want to add from?\n')

        if checkPlaylist(sp, source):
            break
        else:
            print("That playlist does not exist. Please check your spelling.")

    while True:
        target = input('Which playlist do you want to add to?\n')
        if checkPlaylist(sp, target):
            break
        else:
            print("That playlist does not exist. Please check your spelling.")

    for playlist in playlists['items']:
        if playlist['name'] == source:
            source = sp.playlist(playlist["id"])
            break

    for playlist in playlists['items']:
        if playlist['name'] == target:
            target = sp.playlist(playlist["id"])
            break

    for track in source['tracks']['items']:
        sp.playlist_add_items(playlist_id=target['id'], items=[track['track']['id']])
        print(f"{track['track']['name']} was added to {target['name']}")


def main():
    print(f"Welcome {sp.me()['display_name']}. What would you like to do?")

    while True:
        choice = input('''1. Add a playlist to another playlist
''')

        if int(choice) == 1:
            addPlaylist(sp)
            break
        else:
            print("Invalid input. What would you like to do?")
            choice = input()

main()
