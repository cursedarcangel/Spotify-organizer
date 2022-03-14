import spotipy, os, sys, json, spotipy
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


sp=spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private playlist-modify-public playlist-read-private"))


def checkPlaylist(sp, playlist):
    playlists = sp.current_user_playlists()                          
    user_id = sp.me()['id']
    for plist in playlists['items']:
        if playlist == plist['name']:
            return True
    return False

def getPlaylistTracks(username, playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


#Take all songs from one playlist and add it to another playlist, alphabetically by artist
def addPlaylist(sp):

    playlists = sp.current_user_playlists()    
    user_id = sp.me()['id']                       
    print()
    print('Your playlists:')
    for playlist in playlists['items']:    
        if playlist['owner']['id'] == user_id:                                                                                          
            print(playlist['name'], ':', playlist['tracks']['total'], 'tracks')
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

    for track in reversed(source['tracks']['items']):
        counter = 0
        added = False
        while True:
            print(json.dumps(target, sort_keys=True, indent=4))
            for track2 in target['tracks']['items']:
                artists = [track['track']['artists'][0]['name'], track2['track']['artists'][0]['name']]
                artists.sort()
                if artists[0] == track['track']['artists'][0]['name']:
                    sp.playlist_add_items(playlist_id=target['id'], items=[track['track']['id']], position=counter)
                    print(f"{track['track']['name']} was added to {target['name']}")
                    added = True
                    break
                counter += 1
            if added:
                break
            else:
                sp.playlist_add_items(playlist_id=target['id'], items=[track['track']['id']], position=counter)
                print(f"{track['track']['name']} was added to {target['name']}")


#Get artist and song name and output to file
def getSongInfo(sp):
    playlists = sp.current_user_playlists()    
    user_id = sp.me()['id']                       
    print()
    print('Your playlists:')
    for playlist in playlists['items']:    
        if playlist['owner']['id'] == user_id:                                                                                          
            print(playlist['name'], ':', playlist['tracks']['total'], 'tracks')
    print()

    while True:
        source = input('What playlist would you like to take from?\n')
        if checkPlaylist(sp, source):
            break
        else:
            print("That playlist does not exist. Please check your spelling.")
    output = input('What file would you like to output to?\n')

    with open(output, 'a') as f:
        offset = 0
        for playlist in playlists['items']:
            if playlist['name'] == source:
                source = getPlaylistTracks(user_id, playlist['id'])
                break
        for track in source:
            w = track['track']['artists'][0]['name'] + ' - ' + track['track']['name']
            print(w)
            f.write(w + '\n')


def main():
    print(f"Welcome {sp.me()['display_name']}. What would you like to do?\n")

    while True:
        choice = input('''1. Add a playlist to another playlist
2. Get song names and artists from a playlist
''')

        if int(choice) == 1:
            addPlaylist(sp)
            break
        elif int(choice) == 2:
            getSongInfo(sp)
            break
        else:
            print("Invalid input. What would you like to do?")
            choice = input()

main()
