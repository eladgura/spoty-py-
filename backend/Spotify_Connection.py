import cv2
import mediapipe as mp
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials
SPOTIPY_CLIENT_ID = 'c0a8899afb05400093bdebff2013aee6'
SPOTIPY_CLIENT_SECRET = 'fa8e33c10c9d43f28f9f58889e250274'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback/'

# Connect to Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="your_client_id",
                                               client_secret="c0a8899afb05400093bdebff2013aee6",
                                               redirect_uri="http://localhost:8000/callback/",
                                               scope="user-modify-playback-state"))


# Function to skip track
def skip_song():
    sp.next_track()
    print("Skipped song")

# Function to play/pause track
def play_pause_song(currently_playing):
    if currently_playing:
        sp.pause_playback()
        print("Paused song")
    else:
        sp.start_playback()
        print("Playing song")

# Initialize MediaPipe for hand and arm detection
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Tracking the wrist movement for wave detection
previous_wrist_x = None
wave_count = 0
wave_threshold = 50  # Minimum distance for detecting a wave motion
wave_reset_time = 1.5  # Time window in seconds to reset wave detection

# Variables for play/pause detection
currently_playing = True

# Initialize webcam
cap = cv2.VideoCapture(0)
last_wave_time = time.time()

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Detect the face and hands
        results = holistic.process(image)

        # Convert back to BGR for display
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw the face and hand landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # Extract right hand landmarks for gesture detection
        if results.right_hand_landmarks:
            wrist_landmark = results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST]
            wrist_x = wrist_landmark.x * frame.shape[1]  # Convert normalized value to pixel x-coordinates

            # Wave detection logic (left-right motion)
            if previous_wrist_x is not None:
                movement_x = wrist_x - previous_wrist_x
                if abs(movement_x) > wave_threshold:
                    wave_count += 1
                    previous_wrist_x = wrist_x

                    # Check if enough waves happened in the time window
                    if wave_count >= 2 and (time.time() - last_wave_time) <= wave_reset_time:
                        skip_song()  # Trigger skip when wave is detected
                        wave_count = 0  # Reset wave count
                        last_wave_time = time.time()

                # Reset if wave count doesn't happen within the reset window
                if (time.time() - last_wave_time) > wave_reset_time:
                    wave_count = 0

            previous_wrist_x = wrist_x

        # Play/Pause gesture detection (open palm = play, fist = pause)
        if results.left_hand_landmarks:
            # Define open/closed hand by comparing distance between finger tips and palm
            thumb_tip = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP]
            index_tip = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP]
            wrist = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST]

            thumb_index_distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
            palm_width = ((wrist.x - thumb_tip.x) ** 2 + (wrist.y - thumb_tip.y) ** 2) ** 0.5

            # A basic approximation of play (open palm) or pause (fist) gesture
            if thumb_index_distance > palm_width * 0.4:
                if not currently_playing:
                    play_pause_song(currently_playing)
                    currently_playing = True
            else:
                if currently_playing:
                    play_pause_song(currently_playing)
                    currently_playing = False

        # Display the resulting frame
        cv2.imshow('MediaPipe Holistic', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
