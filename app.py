from threading import Timer
import utils as ut
import requests
from flask import Flask, redirect, request, render_template
import webbrowser
from SpotifyPlaylist import SpotifyPlaylist
from typing import Dict


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    def open_browser():
        webbrowser.open_new('http://127.0.0.1:5000/')

    @app.route('/')
    def appSetup():
        """Entry point for the app, duh"""
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
        param = ut.createParams(['grant_type', 'code', 'redirect_uri'])
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
        playlist_response = requests.get(spotify_playlist_uri, headers=header)
        spotify_playlist_list: Dict = playlist_response.json()['items']
        list_playlist = []

        for ind, spotify_playlist in enumerate(spotify_playlist_list):
            playlist = SpotifyPlaylist(spotify_playlist['name'])
            list_playlist.append(playlist)

            playlist_uri = spotify_playlist.get('tracks', None).get('href', None)
            tracks_response_object = requests.get(playlist_uri, headers=header)
            tracks_response_object = tracks_response_object.json()

            for idx, tracks_responce in enumerate(tracks_response_object['items']):
                track_object = tracks_responce['track']
                if track_object is None:
                    continue
                artist_names = []
                name_track = track_object['name']
                for artist in track_object['artists']:
                    artist_names.append(artist['name'])

                playlist.addToPlaylist(name_track, artist_names)
        ut.write_playlist_file(list_playlist)
        return "FeelGood"

    Timer(1, open_browser).start()
    return app

# TODO
#     1. Please refactor the code. Get playlist is a mess
#     2. Create a proper Conda Env
#     3. Start integrating youtube API
