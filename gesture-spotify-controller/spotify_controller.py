import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyController:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = "user-modify-playback-state user-read-playback-state"
        self.sp = self.authenticate()

    def authenticate(self):
        # Authenticate with Spotify using Spotipy
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                       client_secret=self.client_secret,
                                                       redirect_uri=self.redirect_uri,
                                                       scope=self.scope))
        return sp

    def play_song(self):
        self.sp.start_playback()
        print("Song is now playing.")

    def pause_song(self):
        self.sp.pause_playback()
        print("Song is now paused.")

    def skip_song(self):
        self.sp.next_track()
        print("Song skipped.")
