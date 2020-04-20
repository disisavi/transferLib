from typing import Dict
from base64 import b64encode

clientDetails = {}
delimeter = "="


def createParams(listOfParameters):
    paramDict = {}
    for param in listOfParameters:
        try:
            key = param
            value = clientDetails.get(param, None)
            paramDict[key] = value
        except KeyError:
            print(" Key " + key + " not found..")

    return paramDict


def createHeader():
    header = {}
    key = 'Authorization'
    valueToEncode = clientDetails['client_id'] + ':' + clientDetails['client_secret']
    value = "Basic ".encode('utf-8') + b64encode(valueToEncode.encode('utf-8'))
    header[key] = value

    return header


def getAuthURI():
    return clientDetails["spotifyURI"]


def getTokenURI():
    return "https://accounts.spotify.com/api/token"


def getState():
    return clientDetails.get('state', None)


def setAuthCode(code):
    clientDetails['code'] = code


def createRedirectURI(uri: str, params: Dict):
    redirectURI = uri + '?'
    for key, value in params.items():

        if isinstance(value, str):
            redirectURI = redirectURI + key + '=' + value + '&'

        if isinstance(value, list):
            redirectURI = redirectURI + key
            for things in value:
                redirectURI = redirectURI + ' ' + things

            redirectURI = redirectURI + '&'

    if redirectURI[-1] == '&':
        redirectURI = redirectURI[:-1]

    return redirectURI


with open('dev.properties', 'r') as propFile:
    for line in propFile:
        if len(line.strip()) == 0:
            continue

        lineSplit = line.replace(" ", "").replace("\n", "").split(delimeter)
        if len(lineSplit) != 2:
            raise Exception("Invalid File")
        clientDetails[lineSplit[0]] = lineSplit[1]
