import re
from base64 import b64encode
from typing import Dict

import jsonpickle
from importlib_resources import files

from transferLib.SpotifyPlaylist import *


def getFilePath(packageName):
    re_iter = re.finditer(r'\.', packageName)
    indices = [m.start(0) for m in re_iter]
    end_slice = indices[len(indices) - 1]
    return packageName[0:end_slice]


class Util:

    def createParams(self, listOfParameters, spotifySpec=False):
        paramDict = {}
        if spotifySpec:
            targetDict = self.__spotifyUserToken
            print(listOfParameters, targetDict)
        else:
            targetDict = self.__clientDetails

        for param in listOfParameters:
            try:
                key = param
                value = targetDict.get(param, None)
                paramDict[key] = value
            except KeyError:
                print(" Key " + key + " not found..")

        return paramDict

    def createHeader(self):
        header = {}
        key = 'Authorization'
        valueToEncode = self.__clientDetails['client_id'] + ':' + self.__clientDetails['client_secret']
        value = "Basic ".encode('utf-8') + b64encode(valueToEncode.encode('utf-8'))
        header[key] = value

        return header

    # I will, at some later point, convert these URI's into its own property
    def getAuthURI(self):
        return self.__clientDetails["spotifyURI"]

    def getTokenURI(self):
        return "https://accounts.spotify.com/api/token"

    def getPlaylistURI(self):
        return "https://api.spotify.com/v1/me/playlists"

    def getState(self):
        return self.__clientDetails.get('state', None)

    def setAuthCode(self, code):
        self.__clientDetails['code'] = code

    def setSpotifyUserToken(self, token: Dict):
        self.__spotifyUserToken = token
        self.__spotifyUserToken['Authorization'] = self.__spotifyUserToken.pop('access_token', None)

    def createRedirectURI(self, uri: str, params: Dict):
        redirectURI = uri + '?'
        for key, value in params.items():
            redirectURI = redirectURI + key + '=' + value + '&'

        if redirectURI[-1] == '&':
            redirectURI = redirectURI[:-1]

        redirectURI = redirectURI.replace(" ", "%20")
        return redirectURI

    def write_playlist_file(self, list_of_playlists: List[SpotifyPlaylist]):
        global __spotify_playlist_list
        __spotify_playlist_list = list_of_playlists
        with open('playlist.json', 'w') as pfile:
            jsonStr = jsonpickle.encode(list_of_playlists, unpicklable=False)
            pfile.write(jsonStr)

    def __init__(self):
        self.__spotify_playlist_list: List[SpotifyPlaylist] = []
        self.__spotifyUserToken = {}
        self.__clientDetails = {}
        self.delimeter = "="
        self.file_name = 'dev.properties'

        propFile = files(getFilePath(__name__)).joinpath('dev.properties').read_text()

        for line in propFile.split('\n'):
            if len(line.strip()) == 0:
                continue

            lineSplit = line.replace(" ", "").replace("\n", "").split(self.delimeter)
            if len(lineSplit) != 2:
                raise Exception("Invalid File", lineSplit)
            self.__clientDetails[lineSplit[0]] = lineSplit[1].replace(",", " ")
