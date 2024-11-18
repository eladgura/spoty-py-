from gesture_controller import GestureController
from spotify_controller import SpotifyController
from LoginGUI import LoginRegisterGUI


class MainProgram:
    def __init__(self):
        # Initialize the login/register GUI.
        self.login_gui = LoginRegisterGUI()
        self.run_login_or_register()

    def run_login_or_register(self):
        """Run the login or registration flow using the GUI."""
        # Start the GUI flow and capture the result.
        result = self.login_gui.start_gui()

        if result == "exit":
            print("Exiting program...")
        elif result == "logged_in":
            print("Login successful. Starting main program...")
            self.run_main_program()
        else:
            print("Unknown state. Exiting program.")

    def run_main_program(self):
        """Runs the main program after successful login."""
        # Define your Spotify API credentials.
        client_id = "c0a8899afb05400093bdebff2013aee6"
        client_secret = "fa8e33c10c9d43f28f9f58889e250274"
        redirect_uri = "http://localhost:8888/callback"

        # Create an instance of the SpotifyController.
        spotify_controller = SpotifyController(client_id, client_secret, redirect_uri)
        spotify_controller.list_devices()

        # Create an instance of the GestureController with the SpotifyController.
        gesture_controller = GestureController(spotify_controller)

        # Start detecting gestures.
        gesture_controller.detect_gestures()


if __name__ == "__main__":
    MainProgram()
