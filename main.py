from typing import Dict
from base64 import b64encode
import requests
from readClientProperties import readProp


def createHeader(clidentDetails: Dict[str, str]):

    print(clidentDetails)
    header = {}
    key = "Authorization"
    valueToEncode = clidentDetails["client_id"] + ":" + clidentDetails["client_secret"]
    value = 'Basic '.encode("utf-8") + b64encode(valueToEncode.encode("utf-8"))

    header[key] = value
    return header


clientDetails = readProp()
spotifyURL = "https://accounts.spotify.com/api/token"

header = createHeader(clientDetails)
body = {"grant_type": "client_credentials"}

r = requests.post(spotifyURL, data=body, headers=header)
print(r.text)
