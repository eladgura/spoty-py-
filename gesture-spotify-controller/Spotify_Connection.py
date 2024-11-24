import cv2
import mediapipe as mp
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials
SPOTIPY_CLIENT_ID = 'xxxxxxxxxxx'
SPOTIPY_CLIENT_SECRET = 'xxxxxxxxxx'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback/'

# Connect to Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-modify-playback-state user-read-playback-state"))


def skip_song():
    """Function to skip the currently playing song."""
    sp.next_track()
    print("Skipped song")


def play_pause_song(currently_playing):
    """Function to play or pause the currently playing song."""
    if currently_playing:
        sp.pause_playback()
        print("Paused song")
    else:
        sp.start_playback()
        print("Playing song")


# Initialize MediaPipe for hand and arm detection
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Tracking variables
previous_wrist_x = None
wave_count = 0
wave_threshold = 50  # Minimum distance for detecting a wave motion
wave_reset_time = 1.5  # Time window in seconds to reset wave detection
currently_playing = True  # To track play/pause state

# Initialize webcam
cap = cv2.VideoCapture(0)
last_wave_time = time.time()

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = holistic.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # Wave gesture detection
        if results.right_hand_landmarks:
            wrist_landmark = results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST]
            wrist_x = wrist_landmark.x * frame.shape[1]

            if previous_wrist_x is not None:
                movement_x = wrist_x - previous_wrist_x
                if abs(movement_x) > wave_threshold:
                    wave_count += 1
                    previous_wrist_x = wrist_x

                    if wave_count >= 2 and (time.time() - last_wave_time) <= wave_reset_time:
                        skip_song()
                        wave_count = 0
                        last_wave_time = time.time()

                if (time.time() - last_wave_time) > wave_reset_time:
                    wave_count = 0

            previous_wrist_x = wrist_x

        # Play/Pause gesture detection
        if results.left_hand_landmarks:
            thumb_tip = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP]
            index_tip = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP]
            wrist = results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST]

            thumb_index_distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
            palm_width = ((wrist.x - thumb_tip.x) ** 2 + (wrist.y - thumb_tip.y) ** 2) ** 0.5

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
