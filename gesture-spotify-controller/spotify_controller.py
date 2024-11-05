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
        try:
            self.sp.start_playback()
            print("Song is now playing.")
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error playing song: {e}")

    def pause_song(self):
        try:
            current_playback = self.sp.current_playback()
            if current_playback is None or not current_playback['is_playing']:
                print("No active playback session found.")
                return
            
            self.sp.pause_playback()
            print("Playback paused.")
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error pausing song: {e}")

    def skip_song(self):
        try:
            self.sp.next_track()
            print("Song skipped.")
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error skipping song: {e}")

    def list_devices(self):
        # Get the available devices
        devices = self.sp.devices()
        
        if devices['devices']:
            print("Available devices:")
            for device in devices['devices']:
                print(f"Name: {device['name']}, Type: {device['type']}, ID: {device['id']}, Is Active: {device['is_active']}")
        else:
            print("No available devices found.")
