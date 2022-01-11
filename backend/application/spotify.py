import spotipy
from spotipy.oauth2 import SpotifyOAuth
from os import environ
scope = "user-library-read user-read-currently-playing user-modify-playback-state user-read-playback-state app-remote-control streaming"

environ['SPOTIPY_CLIENT_ID'] = 'e885a29021304c4b897cdce8dea137a9'
environ['SPOTIPY_CLIENT_SECRET'] = 'a3d74d52e10449d7bf49aa2fca638744'
environ['SPOTIPY_REDIRECT_URI'] = 'https://example.com/callback/'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def play_music():
    try:
        sp.start_playback()
        return{}
    except Exception as e:
        if e.reason == 'NO_ACTIVE_DEVICE':
            return {'text':'Deseja usar qual dispositivo?', 'context':'expecting_device'}

def search_music(query):
    uri =sp.search(query, 1,0,'track,artist')['tracks']['items'][0]['uri']
    try:
        sp.start_playback(uris=[uri])
        return{}
    except Exception as e:
        if e.reason == 'NO_ACTIVE_DEVICE':
            return {'text':'Deseja usar qual dispositivo?', 'context':'expecting_device'}

def stop_music():
    try:
        sp.pause_playback()
    except:
        return 'Não há nada tocando no spotify'

def __get_current_volume():
    return next((x for x in sp.devices()['devices'] if x['is_active'] ==True), None)['volume_percent']

def volume_up():
    vol = __get_current_volume() + 20
    if vol > 100:
        vol = 100
    sp.volume(vol)
def volume_down():
    vol = __get_current_volume() - 20
    if vol < 0:
        vol = 0
    sp.volume(vol)

def next_music():
    sp.next_track()

def prev_music():
    sp.previous_track()