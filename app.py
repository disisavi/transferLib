import threading

import utils as ut
import requests
from flask import Flask, redirect, request, render_template
import webbrowser
from SpotifyPlaylist import SpotifyPlaylist
from typing import Dict, List

# create and configure the app
app = Flask(__name__)


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')


@app.route('/')
def index():
    return render_template('index.html', redirect_link="/redirect_to_spotify", button_type="login to spotify",
                           action_text="Welcome. Please click below to login to Spotify, so that we can start getting "
                                       "the playlists. PS: You will be redirected to spotify")


@app.route('/redirect_to_spotify')
def appSetup():

    spotifyURI = ut.getAuthURI()
    param = ut.createParams(['client_id', 'redirect_uri', 'response_type', 'scope', 'state'])

    return redirect(ut.createRedirectURI(spotifyURI, param))


@app.route('/redirect', methods=['GET'])
def redirectSpotify():
    response = request.args
    state = response['state']
    if state != ut.getState():
        raise ValueError("State does not match. Incorrect request")
    if 'error' in response:
        raise Exception(response['error'])

    ut.setAuthCode(response['code'])
    param = ut.createParams(['grant_type', 'code', 'redirect_uri', 'scope'])
    header = ut.createHeader()

    uri = ut.getTokenURI()
    spotifyResponse = requests.post(uri, data=param, headers=header)
    ut.setSpotifyUserToken(spotifyResponse.json())
    return render_template("login.html")


@app.route("/getPlaylist")
def getPlaylists():
    spotify_playlist_uri = ut.getPlaylistURI()
    header = ut.createParams(['Authorization'], True)
    header['Authorization'] = 'Bearer ' + header['Authorization']
    header['content_type'] = 'application/json'

    spotify_playlist_list: List[Dict] = ut.get_till_next(spotify_playlist_uri, header)
    spotify_playlist_list.append({'name': 'My Liked Songs', 'tracks': {'href': 'https://api.spotify.com/v1/me/tracks'}})
    list_playlist = []

    for ind, spotify_playlist in enumerate(spotify_playlist_list):
        playlist = SpotifyPlaylist(spotify_playlist['name'])
        list_playlist.append(playlist)

        playlist_uri = spotify_playlist.get('tracks', None).get('href', None)

        tracks_responses = ut.get_till_next(playlist_uri, header)
        for idx, tracks_response in enumerate(tracks_responses):
            track_object = tracks_response['track']
            if track_object is None:
                continue
            artist_names = []
            name_track = track_object['name']
            for artist in track_object['artists']:
                artist_names.append(artist['name'])

            playlist.addToPlaylist(name_track, artist_names)
    ut.write_playlist_file(list_playlist)
    return "FeelGood"


if __name__ == '__main__':
    # open_browser()
    threading.Timer(1.25, lambda: webbrowser.open('http://127.0.0.1:5000/')).start()
    app.run(debug=True)
