# main.py

from spotify_controller import SpotifyController
from gesture_controller import GestureController

if __name__ == "__main__":
    # Initialize SpotifyController
    spotify_controller = SpotifyController(
        client_id='your_client_id',
        client_secret='your_client_secret',
        redirect_uri='http://localhost:8888/callback/'
    )

    # Initialize GestureController and pass the Spotify controller to it
    gesture_controller = GestureController(spotify_controller)

    # Start detecting gestures
    gesture_controller.detect_gestures()
