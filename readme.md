#!/bin/bash

# Gesture Spotify Controller Setup Script
# =======================================
 Automates setup for the Gesture Spotify Controller, including dependencies,
 Spotify API configuration, and running the program.

# Step 1: Clone the repository
git clone https://github.com/your-repo-name/gesture-spotify-controller.git
cd gesture-spotify-controller || { echo "Failed to navigate to the project directory! Exiting."; exit 1; }

# Step 2: Install dependencies
pip install -r requirements.txt || { echo "Failed to install dependencies! Exiting."; exit 1; }

# Step 3: Spotify API Setup Instructions
# Users are required to complete these steps manually:
# 1. Visit https://developer.spotify.com/dashboard/applications.
# 2. Create an app with:
#    - App Name: Gesture Spotify Controller
#    - App Description: Application to control Spotify playback using gestures.
# 3. Add the Redirect URI: http://localhost:8000/callback/.
# 4. Copy the Client ID and Client Secret.

read -p "Press Enter once you've completed Spotify API setup..."

# Step 4: Configure Spotify Credentials
read -p "Enter your Spotify Client ID: " client_id
read -p "Enter your Spotify Client Secret: " client_secret

# Replace placeholders in spotify_controller.py with provided credentials
sed -i "s/your-client-id/$client_id/" spotify_controller.py
sed -i "s/your-client-secret/$client_secret/" spotify_controller.py
sed -i "s|http://localhost:8000/callback|http://localhost:8000/callback|" spotify_controller.py

# Notes and Gesture Information
# - A Spotify Premium account is required for playback control.
# - Ensure your webcam is working and placed in proper lighting for gesture detection.
# - Login and Registration:
#   - On startup, the application will ask you to **register or log in**.
#   - To register a new user:
#     - Look at the webcam to capture your face data and confirm registration.
#   - To log in:
#     - Look at the webcam again to verify your face against stored data.
#   - If you wish to **exit the login/registration process**, press `q`.

# - Gestures and Their Functions:
#   - Wave Gesture (Right Hand): Skips to the next track.
#     Perform by moving your right hand left and right quickly.
#   - Thumb-Index Pinch Gesture (Left Hand): Toggles play/pause.
#     Perform by pinching and releasing your thumb and index finger.
# - To exit the program at any time, press the `Q` key while the webcam feed is active.

# Troubleshooting Information:
# 1. If no active playback device is found:
#    - Open Spotify and start playing on any device before running the program.
# 2. If gestures are not recognized:
#    - Ensure proper lighting and keep hands within the webcam's field of view.
#    - Adjust hand positions if needed.
# 3. Authentication Issues:
#    - Ensure Client ID, Client Secret, and Redirect URI are correct.
#    - Confirm the Redirect URI is added in the Spotify Developer Dashboard.

# Step 5: Run the application
python main.py || { echo "Failed to run the application! Check your setup and try again."; exit 1; }

# Completion Message
# The program will now start; follow the on-screen instructions.
