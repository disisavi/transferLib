from threading import Timer
import utils as ut
import requests
from flask import Flask, redirect, request, render_template
import webbrowser


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    def open_browser():
        webbrowser.open_new('http://127.0.0.1:5000/')

    @app.route('/')
    def appSetup():
        spotifyURI = ut.getAuthURI()
        param = ut.createParams(['client_id', 'redirect_uri', 'response_type', 'scope', 'state'])
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
        print("D3 (((((((((")
        print(ut.__clientDetails)
        return "heloo"

    Timer(1, open_browser).start();
    return app
