from threading import Timer
import utils as ut
import requests
from flask import Flask, redirect, request
import webbrowser


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    def open_browser():
        webbrowser.open_new('http://127.0.0.1:5000/')

    @app.route('/')
    def appSetup():
        spotifyURI = ut.getAuthURI()
        param = ut.createParams(['client_id', 'redirect_uri', 'response_type', 'state'])
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
        print(spotifyResponse.text)
        return "Hello Bitches"

    Timer(1, open_browser).start();
    return app
