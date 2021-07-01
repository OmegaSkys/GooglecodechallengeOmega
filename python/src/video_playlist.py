"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name):

        self.playlist_name = name

        self.id = name.lower()

        self.videos = []

    def is_valid_name(name):
         if len(name.split(' ')) > 1:
             return False
         return True