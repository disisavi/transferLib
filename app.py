from typing import Dict
from threading import Timer
import requests
import utils as ut
from flask import Flask,redirect
import webbrowser


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)


    def open_browser():
        webbrowser.open_new('http://127.0.0.1:5000/')

    @app.route('/')
    def appSetup():    
        spotifyURL = ut.getURI()
        param = ut.createParams(['client_id', 'redirect_uri', 'response_type'])
        return redirect(ut.createRedirectURI(spotifyURL,param))    

    @app.route('/redirect')
    def res():
        print("Called")


    Timer(1, open_browser).start();
    return app

