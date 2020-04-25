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
        spotifyURI = ut.getAuthURI()
        param = ut.createParams(['client_id', 'redirect_uri', 'response_type', 'scope', 'state'])
        print(param)
        return redirect(ut.createRedirectURI(spotifyURI, param))

    @app.route('/redirect', methods=['GET'])
    def redirectSpotify():
        response = request.args
        state = response['state']
        print("Hello")
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
        spotigyPlaylistURI = ut.getPlaylistURI()
        header = ut.createParams(['Authorization'], True)
        header['Authorization'] = 'Bearer ' + header['Authorization']
        playlistResponse = requests.get(spotigyPlaylistURI, headers=header)
        spotifyPlaylistList: Dict = playlistResponse.json()['items']
        list_playlist = []

        for ind, spotifyPlaylist in enumerate(spotifyPlaylistList):
            print(ind)
            playlist = SpotifyPlaylist(spotifyPlaylist['name'])
            list_playlist.append(playlist)
            playlistURI = spotifyPlaylist.get('tracks', None).get('href', None)
            tracksResponseObject = requests.get(playlistURI, headers=header)
            tracksResponseObject = tracksResponseObject.json()
            for idx, tracksResponce in enumerate(tracksResponseObject['items']):
                print("\t", idx)
                trackObject = tracksResponce['track']
                if trackObject is None:
                    continue
                artist_names = []
                nameTrack = trackObject['name']
                for artist in trackObject['artists']:
                    artist_names.append(artist['name'])

                playlist.addToPlaylist(nameTrack, artist_names)
        ut.writePlaylistToFile(list_playlist)
        return "FeelGood"

    Timer(1, open_browser).start()
    return app

#
# TODO
#     1. Please refactor the code. Get playlist is a mess
#     2. Create a proper Conda Env
#     3. Start integrating youtube API
