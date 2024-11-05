from gesture_controller import GestureController
from spotify_controller import SpotifyController  # Make sure to import your SpotifyController class

if __name__ == "__main__":
    # Define your Spotify API credentials
    client_id = "c0a8899afb05400093bdebff2013aee6"  # Replace with your actual client ID
    client_secret = "fa8e33c10c9d43f28f9f58889e250274"  # Replace with your actual client secret
    redirect_uri = "http://localhost:8888/callback"  # Your defined redirect URI

    # Create an instance of the SpotifyController
    spotify_controller = SpotifyController(client_id, client_secret, redirect_uri)

    # Create an instance of the GestureController with the SpotifyController
    gesture_controller = GestureController(spotify_controller)

    # Start detecting gestures
    gesture_controller.detect_gestures()
