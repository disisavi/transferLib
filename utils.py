from typing import Dict
from base64 import b64encode

__spotifyUserToken = {}
__clientDetails = {}
delimeter = "="


def createParams(listOfParameters):
    paramDict = {}
    for param in listOfParameters:
        try:
            key = param
            value = __clientDetails.get(param, None)
            paramDict[key] = value
        except KeyError:
            print(" Key " + key + " not found..")

    return paramDict


def createHeader():
    header = {}
    key = 'Authorization'
    valueToEncode = __clientDetails['client_id'] + ':' + __clientDetails['client_secret']
    value = "Basic ".encode('utf-8') + b64encode(valueToEncode.encode('utf-8'))
    header[key] = value

    return header


# I will, at some later point, convert these URI's into its own property
def getAuthURI():
    return __clientDetails["spotifyURI"]


def getTokenURI():
    return "https://accounts.spotify.com/api/token"


def getPlaylistURI():
    return "https://api.spotify.com/v1/me/playlists"


def getState():
    return __clientDetails.get('state', None)


def setAuthCode(code):
    __clientDetails['code'] = code


def setSpotifyUserToken(token: Dict):
    __spotifyUserToken = token


def createRedirectURI(uri: str, params: Dict):
    redirectURI = uri + '?'
    for key, value in params.items():
        redirectURI = redirectURI + key + '=' + value + '&'

    if redirectURI[-1] == '&':
        redirectURI = redirectURI[:-1]

    redirectURI = redirectURI.replace(" ", "%20")
    return redirectURI


with open('dev.properties', 'r') as propFile:
    for line in propFile:
        if len(line.strip()) == 0:
            continue

        lineSplit = line.replace(" ", "").replace("\n", "").split(delimeter)
        if len(lineSplit) != 2:
            raise Exception("Invalid File")
        __clientDetails[lineSplit[0]] = lineSplit[1].replace(",", " ")
