import requests

import util
from util import load_props, createParams, createHeader


def main():
    load_props()
    params = createHeader()
    param = createParams(['grant_type', "scope"])
    print(params, param)
    response = requests.post(util.getAuthURI(), headers=params, data=param)
    print(response.text)
    response.raise_for_status()


if __name__ == "__main__":
    main()
