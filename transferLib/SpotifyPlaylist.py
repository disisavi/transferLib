from typing import List


class SpotifyPlaylist:
    """An Object for holding playlist objects """

    def __init__(self, name: str):
        self.playlistName: str = name
        self.listOfTracks: List[Track] = []

    def addToPlaylist(self, name, artistNameList):
        track = Track(name, artistNameList)
        self.listOfTracks.append(track)


class Track:
    """An object for holding indivisual tracks for playlist"""

    def __init__(self, name, artist_name_list: List):
        self.name = name
        self.artists = artist_name_list
