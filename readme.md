Gesture Spotify Controller Setup Script
Introduction
Welcome to the Gesture Spotify Controller! This script automates the setup process for using gestures to control Spotify playback. You’ll be able to skip tracks and toggle play/pause with simple hand gestures detected via your webcam. Let’s get started!

Setup Instructions
Step 1: Clone the Repository
The first step is to download the Gesture Spotify Controller's code. Open your terminal and run the following commands:

git clone https://github.com/eladgura/spoty-py-?tab=readme-ov-file
cd gesture-spotify-controller
Step 2: Install Dependencies
Make sure you have Python installed (version 3.8 or later). Then, install the necessary Python packages by running:

pip install -r requirements.txt
Spotify API Configuration
Spotify’s API lets this program control playback, but you’ll need to set up an app on the Spotify Developer Dashboard first.

Go to the Spotify Developer Dashboard and log in with your Spotify account.
Click Create an App, then fill in these details:
App Name: Gesture Spotify Controller
App Description: Application to control Spotify playback using gestures.
Add a Redirect URI under your app settings:

http://localhost:8000/callback/
Save your app. Copy the Client ID and Client Secret shown on your app dashboard.
When ready, return to your terminal and run:

read -p "Enter your Spotify Client ID: " client_id
read -p "Enter your Spotify Client Secret: " client_secret
These credentials will be automatically added to the program.

Gesture Controls
Once set up, the Gesture Spotify Controller uses these gestures to control playback:

Wave Gesture (Right Hand):

Action: Skips to the next track.
How to Perform: Move your right hand left and right quickly in front of the webcam.
Thumb-Index Pinch Gesture (Left Hand):

Action: Toggles play/pause.
How to Perform: Pinch your thumb and index finger together, then release.
Login and Registration
On startup, you’ll be prompted to either register or log in:

To Register:
Face the webcam to capture your face data and confirm registration.
To Log In:
Face the webcam to verify your identity using stored face data.
To Exit:
Press q to quit the process anytime.
Notes
Spotify Premium: A Spotify Premium account is required for playback controls.
Webcam Setup: Ensure your webcam is working properly and has good lighting for gesture detection.
Exiting the Program: Press Q while the webcam feed is active to quit.
Troubleshooting
No Active Playback Device Found

Open Spotify on your phone, computer, or another device and start playing music before using this application.
Gestures Not Recognized

Ensure your hands are clearly visible to the webcam.
Use proper lighting, and keep your hands within the webcam’s field of view.
Authentication Issues

Double-check the Client ID, Client Secret, and Redirect URI you entered.
Verify the Redirect URI is listed in your Spotify Developer App settings.
Running the Program
After completing the setup, launch the Gesture Spotify Controller:

python main.py
The program will start, and you can follow the on-screen instructions.

Enjoy Your Gesture-Controlled Spotify Experience!
If you have any issues, consult the troubleshooting section or visit the Spotify Developer Documentation. Happy listening!
