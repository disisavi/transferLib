from typing import Dict

clientCred = {}
delimeter = "="


def readProp() -> Dict[str, str]:
    with open('dev.properties', 'r') as propFile:
        for line in propFile:
            if len(line.strip()) == 0:
                continue

            lineSplit = line.replace(" ", "").replace("\n", "").split(delimeter)
            if len(lineSplit) != 2:
                raise Exception("Invalid File")

            clientCred[lineSplit[0]] = lineSplit[1]

    return clientCred
