from gesture_controller import GestureController
from spotify_controller import SpotifyController
from login_register import FaceRecognition

class MainProgram:
    def __init__(self):
        # Initialize face recognition system
        self.face_recognition = FaceRecognition()

        # Start login or registration flow
        self.run_login_or_register()

    def run_login_or_register(self):
        while True:
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            
            choice = input("Choose an option: ")
            
            if choice == "1":
                self.face_recognition.register()  # Register a new user
            elif choice == "2":
                if self.face_recognition.login():  # Log in successfully
                    self.run_main_program()  # Proceed to the main program
                    break  # Exit the login/register loop
            elif choice == "3":
                print("Exiting program...")
                self.face_recognition.close()
                break  # Exit the program
            else:
                print("Invalid option. Please choose again.")

    def run_main_program(self):
        """Runs the main program after successful login."""
        # Define your Spotify API credentials
        client_id = "c0a8899afb05400093bdebff2013aee6"  # Replace with your actual client ID
        client_secret = "fa8e33c10c9d43f28f9f58889e250274"  # Replace with your actual client secret
        redirect_uri = "http://localhost:8888/callback"  # Your defined redirect URI

        # Create an instance of the SpotifyController
        spotify_controller = SpotifyController(client_id, client_secret, redirect_uri)
        spotify_controller.list_devices()

        # Create an instance of the GestureController with the SpotifyController
        gesture_controller = GestureController(spotify_controller)

        # Start detecting gestures
        gesture_controller.detect_gestures()

if __name__ == "__main__":
    MainProgram()  # Run the main program
