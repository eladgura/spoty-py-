#!/bin/bash

############################################################
#          Gesture Spotify Controller Setup Script         #
# Automates setup for the Gesture Spotify Controller,      #
# including dependencies, Spotify API configuration,       #
# and running the program.                                 #
############################################################

# Step 1: Clone the repository
echo "Step 1: Cloning the repository..."
git clone https://github.com/your-repo-name/gesture-spotify-controller.git
cd gesture-spotify-controller || { echo "Failed to navigate to the project directory! Exiting."; exit 1; }
echo "Repository cloned successfully!"

# Step 2: Install dependencies
echo "Step 2: Installing dependencies..."
pip install -r requirements.txt || { echo "Failed to install dependencies! Exiting."; exit 1; }
echo "Dependencies installed successfully!"

# Step 3: Spotify API Setup Instructions
echo "Step 3: Setting up Spotify API credentials..."
echo "Complete the following steps manually:"
echo "1. Visit https://developer.spotify.com/dashboard/applications."
echo "2. Create an app with the following details:"
echo "   - App Name: Gesture Spotify Controller"
echo "   - App Description: Application to control Spotify playback using gestures."
echo "3. Add the Redirect URI: http://localhost:8000/callback/."
echo "4. Copy the Client ID and Client Secret."
read -p "Press Enter once you've completed Spotify API setup..."

# Step 4: Configure Spotify Credentials
read -p "Enter your Spotify Client ID: " client_id
read -p "Enter your Spotify Client Secret: " client_secret
echo "Configuring Spotify credentials..."
sed -i "s/your-client-id/$client_id/" spotify_controller.py
sed -i "s/your-client-secret/$client_secret/" spotify_controller.py
sed -i "s|http://localhost:8000/callback|http://localhost:8000/callback|" spotify_controller.py
echo "Spotify credentials configured successfully!"

# Notes and Gesture Information
echo "==========================================================="
echo "Notes:"
echo "- A Spotify Premium account is required for playback control."
echo "- Ensure your webcam is working and placed in proper lighting for gesture detection."
echo "- Login and Registration:"
echo "  * On startup, the application will ask you to register or log in."
echo "  * To register: Look at the webcam to capture your face data and confirm."
echo "  * To log in: Look at the webcam to verify your face."
echo "  * To exit the login/registration process, press 'q'."
echo "- Gesture Controls:"
echo "  * Wave Gesture (Right Hand): Skips to the next track."
echo "    Perform by moving your right hand left and right quickly."
echo "  * Thumb-Index Pinch Gesture (Left Hand): Toggles play/pause."
echo "    Perform by pinching and releasing your thumb and index finger."
echo "- To exit the program at any time, press the 'Q' key."
echo "==========================================================="

# Troubleshooting Information
echo "Troubleshooting:"
echo "1. If no active playback device is found:"
echo "   - Open Spotify and start playing on any device before running the program."
echo "2. If gestures are not recognized:"
echo "   - Ensure proper lighting and keep hands within the webcam's field of view."
echo "   - Adjust hand positions for better detection."
echo "3. If authentication issues occur:"
echo "   - Ensure Client ID, Client Secret, and Redirect URI are correct."
echo "   - Confirm the Redirect URI is added in the Spotify Developer Dashboard."
echo "==========================================================="

# Step 5: Run the application
echo "Step 5: Running the application..."
python main.py || { echo "Failed to run the application! Check your setup and try again."; exit 1; }
echo "Application is running! Follow on-screen instructions."
