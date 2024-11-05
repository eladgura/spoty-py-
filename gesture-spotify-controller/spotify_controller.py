# spotify_controller.py

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyController:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-modify-playback-state",
            cache_path=".cache"  # Save token cache to file
        ))

    def skip_song(self):
        try:
            self.sp.next_track()
            print("Skipped to the next song.")
        except spotipy.SpotifyException as e:
            print(f"Error skipping song: {e}")

    def play_pause(self, currently_playing):
        try:
            if currently_playing:
                self.sp.pause_playback()
                print("Paused song.")
            else:
                self.sp.start_playback()
                print("Resumed song.")
        except spotipy.SpotifyException as e:
            print(f"Error with play/pause: {e}")
