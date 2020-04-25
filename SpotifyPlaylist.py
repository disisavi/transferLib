from typing import List


class SpotifyPlaylist:
    def __init__(self, name: str):
        self.playlistName: str = name
        self.listOfTracks: List[Track] = []

    def addToPlaylist(self, name, artistNameList):
        track = Track(name, artistNameList)
        self.listOfTracks.append(track)


class Track:
    def __init__(self, name, artist_name_list: List):
        self.name = name
        self.artists = artist_name_list
