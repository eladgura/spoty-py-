import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

class SpotifyController:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = "user-modify-playback-state user-read-playback-state"
        self.sp = self.authenticate()

    def authenticate(self):
        return spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope
        ))

    def play_song(self):
        """Starts/resumes playback on the active device."""
        try:
            self.sp.start_playback()
            print("Song is now playing.")
        except SpotifyException as e:
            print(f"Error playing song: {e}")

    def pause_song(self):
        """Pauses playback if there is an active session."""
        try:
            if self.is_playing():
                self.sp.pause_playback()
                print("Playback paused.")
            else:
                print("No active playback session found.")
        except SpotifyException as e:
            print(f"Error pausing song: {e}")

    def skip_song(self):
        """Skips to the next track."""
        try:
            self.sp.next_track()
            print("Song skipped.")
        except SpotifyException as e:
            print(f"Error skipping song: {e}")

    def is_playing(self):
        """Checks if there is an active playback session."""
        try:
            playback = self.sp.current_playback()
            return playback is not None and playback.get('is_playing', False)
        except SpotifyException as e:
            print(f"Error checking playback state: {e}")
            return False

    def list_devices(self):
        """Lists available devices."""
        devices = self.sp.devices()
        if devices['devices']:
            print("Available devices:")
            for device in devices['devices']:
                print(f"Name: {device['name']}, Type: {device['type']}, ID: {device['id']}, Is Active: {device['is_active']}")
        else:
            print("No available devices found.")
