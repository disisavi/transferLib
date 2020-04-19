from typing import Dict
from base64 import b64encode

clidentDetails = {}
delimeter = "="


def createParams(listOfParameters):
    paramDict = {}
    for param in listOfParameters:
        try:
            key = param
            value = clidentDetails[param]
            paramDict[key] = value
        except KeyError:
            print(" Key " + key + " not found..")

    return paramDict


def getURI():
    return clidentDetails["spotifyURI"]


with open('dev.properties', 'r') as propFile:
    for line in propFile:
        if len(line.strip()) == 0:
            continue

        lineSplit = line.replace(" ", "").replace("\n", "").split(delimeter)
        if len(lineSplit) != 2:
            raise Exception("Invalid File")
        clidentDetails[lineSplit[0]] = lineSplit[1]

def createRedirectURI(url:str, params:Dict):
    redirectURI = url+'?'
    for key, value in params.items():
        if isinstance(value,str):
            redirectURI = redirectURI +key+'='+value+'&'
        if isinstance(value, list):
            # for now
            pass
    print("D1 "+redirectURI)
    if redirectURI[-1] == '&':
        print("D2 "+redirectURI[:-2])
        redirectURI = redirectURI[:-1]
    
    return redirectURI
