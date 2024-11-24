
# Gesture Spotify Controller Setup Script
# =======================================
# This script automates the setup for the Gesture Spotify Controller,
# including dependencies, Spotify API configuration, and running the program.
# Includes additional notes and troubleshooting steps.

echo "==========================================================="
echo "Welcome to the Gesture Spotify Controller Setup Script!"
echo "This script will guide you through the complete setup process."
echo "==========================================================="

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
echo "==========================================================="
echo "Step 3: Setting up Spotify API credentials..."
echo "Please complete the following steps manually:"
echo "1. Visit the Spotify Developer Dashboard: https://developer.spotify.com/dashboard/applications"
echo "2. Log in with your Spotify account and click 'Create an App'."
echo "   - App Name: Gesture Spotify Controller"
echo "   - App Description: Application to control Spotify playback using gestures."
echo "3. After creating the app, copy your Client ID and Client Secret."
echo "4. Add the following Redirect URI in the app settings:"
echo "   - http://localhost:8000/callback/"
echo "==========================================================="
read -p "Press Enter once you've completed the above steps..."

# Step 4: Configure Spotify Credentials
echo "Step 4: Configuring Spotify credentials..."
read -p "Enter your Spotify Client ID: " client_id
read -p "Enter your Spotify Client Secret: " client_secret

# Replacing placeholders in spotify_controller.py
echo "Updating Spotify credentials in the code..."
sed -i "s/your-client-id/$client_id/" spotify_controller.py
sed -i "s/your-client-secret/$client_secret/" spotify_controller.py
sed -i "s|http://localhost:8000/callback|http://localhost:8000/callback|" spotify_controller.py
echo "Spotify credentials updated successfully!"

# Step 5: Notes and Important Information
echo "==========================================================="
echo "Important Notes:"
echo "1. This application requires a Spotify Premium account for playback control."
echo "2. Ensure your webcam is working and placed in proper lighting for gesture detection."
echo "3. Gestures and Their Functions:"
echo "   - Wave Gesture (Right Hand): Skips to the next track."
echo "     * Move your right hand left and right quickly."
echo "   - Thumb-Index Pinch Gesture (Left Hand): Toggles play/pause."
echo "     * Bring your left hand's thumb and index finger close together and then separate them."
echo "4. To exit the program, press the 'Q' key while the webcam feed is active."
echo "==========================================================="

# Step 6: Troubleshooting
echo "==========================================================="
echo "Troubleshooting Steps:"
echo "1. No active playback device found:"
echo "   * Ensure Spotify is open and playing on your phone, computer, or another device before starting the program."
echo "2. Gestures not recognized:"
echo "   * Ensure proper lighting and keep your hands within the webcam's field of view."
echo "   * Adjust the position of your hands for better detection."
echo "3. Authentication Issues:"
echo "   * Double-check your Client ID, Client Secret, and Redirect URI."
echo "   * Ensure you have added 'http://localhost:8000/callback/' as a redirect URI in your Spotify Developer Dashboard."
echo "==========================================================="

# Step 7: Run the Application
echo "Step 7: Running the Gesture Spotify Controller..."
python main.py || { echo "Failed to run the application! Check your setup and try again."; exit 1; }
echo "Application running! Follow on-screen instructions."

echo "==========================================================="
echo "Setup and execution complete! Enjoy the Gesture Spotify Controller."
echo "==========================================================="
Detailed Explanation:
Cloning and Dependency Installation:

Automates cloning the repository and installing all Python dependencies via pip.
Spotify API Setup Instructions:

Provides clear instructions for manually setting up the Spotify Developer App and configuring credentials.
Prompts the user to input the Client ID and Client Secret.
Updating Spotify Credentials:

Uses sed to replace placeholders in spotify_controller.py with the provided credentials.
Ensures the Redirect URI matches the one registered in the Spotify Developer Dashboard.
Notes:

Lists supported gestures and their functions, ensuring users understand the system requirements and how to exit the program.
Troubleshooting Section:

Guides users through resolving common issues like authentication errors, playback problems, or gesture recognition challenges.
Running the Application:

Runs main.py and provides helpful error messages if the execution fails.
Usage:
Save this script as setup.sh.
Make it executable:
bash
Copy code
chmod +x setup.sh
Run the script:
bash
Copy code
./setup.sh
Additional Notes:
This script assumes that spotify_controller.py contains placeholders like your-client-id and your-client-secret for credentials.
If running on non-UNIX systems (e.g., Windows), you may need to manually edit the script or run commands individually since sed may not be available.





