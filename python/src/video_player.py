"""A video player class."""
import random
from src.video_library import VideoLibrary
from src.video_playlist import Playlist

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.extra_items = {}
        self.playlists = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        print("Here's a list of all available videos:")
        template = "{} ({}) [{}]"
        str_lst = []
        for video in self._video_library.get_all_videos():
            title = video._title
            video_id = video._video_id
            tags_tup = video._tags
            tags_str = " ".join(tags_tup)
            str_lst.append(template.format(title, video_id, tags_str))
        str_lst.sort()
        for s in str_lst:
            print(s)

    def is_playing(self):
        "Return video object current playing"
        videos = self._video_library.get_all_videos()
        for v in videos:
            if v._status == 1:
                return(v)
        return(None)

    def is_paused(self):
        "Return video object current playing"
        videos = self._video_library.get_all_videos()
        for v in videos:
            if v._status == 2:
                return(v)
        return(None)

    def play_video(self, video_id):
        "Plays the respective video."

        playing_video = self._video_library.get_video(video_id)
        "Args:video_id: The video_id to be played."
        if playing_video is None:
            print("Cannot play video: Video does not exist")
        else:
            if self.is_playing() is not None:
                print("Stopping video: {}".format(self.is_playing()._title))
                self.is_playing()._status=0
            elif self.is_paused()is not None:
                print("Stopping video: {}".format(self.is_paused()._title))
                self.is_paused()._status = 0
            print("Playing video: {}".format(playing_video._title))
            playing_video._status = 1

    def stop_video(self):
        if self.is_playing() is None:
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video: {}".format(self.is_playing()._title))
            self.is_playing()._status = 0

    def play_random_video(self):
        """Plays a random video from the video library."""
        video = random.choice(self._video_library.get_all_videos())
        self.play_video(video.video_id)


    def pause_video(self):
        """Pauses the current video."""
        if self.is_paused() is not None:
            print("Video already paused: {}".format(self.is_paused()._title))
        elif self.is_playing() is not None:
            print("Pausing video: {}".format(self.is_playing()._title))
            self.is_playing()._status = 2
        else:
            print("Cannot pause video: No video is currently playing")


    def continue_video(self):
        """Resumes playing the current video."""
        if self.is_playing() is not None:
            print("Cannot continue video: Video is not paused")
        elif self.is_paused() is not None:
            print("Continuing video: {}".format(self.is_paused()._title))
            self.is_paused()._status = 1
        else:
            print("Cannot continue video: No video is currently playing")


    def show_playing(self):
        """Displays video currently playing."""
        if self.is_playing() is not None:
            currplayed = self.is_playing()._tags
            print("Currently playing: {} ({}) [{}]".format(self.is_playing()._title, self.is_playing()._video_id, " ".join(currplayed)))
        elif self.is_paused() is not None:
            currplayed = self.is_paused()._tags
            print("Currently playing: {} ({}) [{}] - PAUSED".format(self.is_paused()._title, self.is_paused()._video_id, " ".join(currplayed)))
        else:
            print("No video is currently playing")


    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        new_playlist_id = playlist_name.lower()
        if new_playlist_id in self.playlists.keys():
            print("Cannot create playlist: A playlist with the same name already exists")
            return

        new_playlist = Playlist(playlist_name)
        self.playlists[new_playlist_id] = new_playlist
        print(f"Successfully created new playlist: {playlist_name}")



    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist_id = playlist_name.lower()
        if not playlist_id in self.playlists.keys():
            print("Cannot add video to another_playlist: Playlist does not exist")
            return

        if not self._video_library.get_video(video_id):
            print(f"Cannot add video to {playlist_name}: Video does not exist")
            return

        if video_id in self.playlists[playlist_id].videos:
            print(f"Cannot add video to {playlist_name}: Video already added")
            return

        video = self._video_library.get_video(video_id)
        self.playlists[playlist_id].videos.append(video_id)
        print(f"Added video to {playlist_name}: {video.title}")
        return


    def show_all_playlists(self):
        """Display all playlists."""

        if len(self.playlists.keys()) == 0:
            print("No playlists exist yet")
            return

        all_playlists = self.playlists.keys()
        sorted_playlists_names = sorted(all_playlists)

        print("Showing all playlists:")
        for sorted_playlist_name in sorted_playlists_names:
            print(self.playlists.get(sorted_playlist_name).name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name."""
        playlist_id = playlist_name.lower()
        if not playlist_id in self.playlists.keys():
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return

        playlist = self.playlists.get(playlist_id)
        videos = playlist.videos

        if len(videos) == 0:
            print(f"Showing playlist: {playlist_name}")
            print("No videos here yet")
            return

        print(f"Showing playlist: {playlist_name}")
        for video_id in videos:
            print(self._video_library.get_video(video_id))
        return

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist_id = playlist_name.lower()
        if not playlist_id in self.playlists.keys():
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return

        if not self._video_library.get_video(video_id):
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return

        if not video_id in self.playlists[playlist_id].videos:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            return

        video = self._video_library.get_video(video_id)

        self.playlists[playlist_id].videos.remove(video_id)
        print(f"Removed video from {playlist_name}: {video.title}")
        return

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_id = playlist_name.lower()
        if not playlist_id in self.playlists.keys():
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return

        self.playlists.get(playlist_id).videos = []
        print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_id = playlist_name.lower()
        if not playlist_id in self.playlists.keys():
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return

        self.playlists.pop(playlist_id)
        print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        all_videos.sort(key=lambda x: x.title)
        matching_videos = []
        for video in all_videos:
            if search_term.lower() in video.title.lower():
                matching_videos.append(video)

        matching_videos.sort(key=lambda x: x.title)

        if len(matching_videos) == 0:
            print(f"No search results for {search_term}")
            return

        print("Here are the results for cat:")
        for i, matching_video in enumerate(matching_videos):
            print(f"{i + 1}) {str(matching_video)}")

        print(
            "Would you like to play any of the above? If yes, specify the number of the video.\nIf your answer is not a valid number, we will assume it's a no.")
        video_number = input()

        # print(video_number)

        try:
            int_video_number = int(video_number)
            if int_video_number > len(matching_videos) or int_video_number < 0:
                return
            else:
                self.play_video(matching_videos[int_video_number - 1].video_id)
        except ValueError:
            return


def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        if not video_tag.startswith('#'):
            print(f"No search results for {video_tag}")
            return

        all_videos = self._video_library.get_all_videos()
        matching_videos = []
        for video in all_videos:
            if video_tag.lower() in list(map(str.lower, video.tags)):
                matching_videos.append(video)

        matching_videos.sort(key=lambda x: x.title)

        if len(matching_videos) == 0:
            print(f"No search results for {video_tag}")
            return

        print(f"Here are the results for {video_tag}:")
        for i, matching_video in enumerate(matching_videos):
            print(f"{i + 1}) {str(matching_video)}")

        print(
            "Would you like to play any of the above? If yes, specify the number of the video.\nIf your answer is not a valid number, we will assume it's a no.")
        video_number = input()

        # print(video_number)

        try:
            int_video_number = int(video_number)
            if int_video_number > len(matching_videos) or int_video_number < 0:
                return
            else:
                self.play_video(matching_videos[int_video_number - 1].video_id)
        except ValueError:
            return

def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
