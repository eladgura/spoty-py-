Gesture Spotify Controller
Overview
The Gesture Spotify Controller allows users to control Spotify playback using hand gestures detected through a webcam. The application uses MediaPipe for gesture recognition and Spotipy for interfacing with the Spotify Web API.

Features
Wave Gesture (Right Hand): Skip to the next song.
Thumb-Index Pinch Gesture (Left Hand): Toggle play/pause of the current track.
System Requirements
Operating System: Windows 10 or later
Python version: 3.8 or later
Webcam for gesture detection
Installation
Step 1: Clone the repository
Download or clone the repository:

bash
Copy code
git clone https://github.com/your-repo-name/gesture-spotify-controller.git
cd gesture-spotify-controller
Step 2: Install dependencies
Run the following command to install all required Python packages:

bash
Copy code
pip install -r requirements.txt
Spotify API Setup
To control Spotify playback, you need to register an application with Spotify and obtain the required credentials.

Step 1: Register Your Application
Visit the Spotify Developer Dashboard: Spotify for Developers.
Log in with your Spotify account and click Create an App.
Fill in the required details:
App Name: Gesture Spotify Controller
App Description: Application to control Spotify playback using gestures.
After creating the app, you will see the Client ID and Client Secret.
Step 2: Set Up Redirect URI
Go to your app's settings in the Spotify Dashboard.
In the Redirect URIs section, add the following URI:
bash
Copy code
http://localhost:8000/callback/
Save the settings.
Configuration
Step 1: Insert Spotify Credentials
Edit the Spotify_Connection.py or spotify_controller.py file to include your Spotify credentials:

python
Copy code
SPOTIPY_CLIENT_ID = 'your-client-id'
SPOTIPY_CLIENT_SECRET = 'your-client-secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback/'
Step 2: Run the Application
Launch the program:

bash
Copy code
python Spotify_Connection.py
Hand Gestures and Their Functions
Wave Gesture (Right Hand):

Action: Skips to the next track.
How to Perform: Move your right hand quickly left and right.
Thumb-Index Pinch Gesture (Left Hand):

Action: Toggles play/pause.
How to Perform: Bring your left hand's thumb and index finger close together and then separate them. Ensure this motion is visible to the webcam.
Notes
Ensure that your Spotify account is Premium, as the Spotify Web API requires a premium subscription for playback control.
The webcam feed will display a window showing recognized hand gestures. Press Q to exit the program.
Troubleshooting
No active playback device found: Open Spotify on your phone, computer, or another device and start playing a song before running the application.
Gestures not recognized: Ensure proper lighting and keep your hands in view of the webcam.
Additional Resources
Spotify Developer Dashboard: https://developer.spotify.com/dashboard/applications
Feel free to fork this project or raise an issue if you encounter any problems! 
