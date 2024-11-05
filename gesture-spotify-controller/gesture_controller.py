import cv2
import mediapipe as mp
import time

class GestureController:
    def __init__(self, spotify_controller):
        self.spotify_controller = spotify_controller
        self.mp_holistic = mp.solutions.holistic
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils

        # Wave detection variables
        self.previous_wrist_x = None
        self.wave_threshold = 0.05
        self.wave_reset_time = 1.5
        self.wave_direction = None  # Track wave direction
        self.wave_confirmed = False  # Track if a full wave has been detected

        # Cooldown variables
        self.last_wave_command_time = 0  # Timestamp for the last wave command
        self.last_play_pause_command_time = 0  # Timestamp for the last play/pause command
        self.command_cooldown = 2  # Cooldown period in seconds for any command

    def detect_gestures(self):
        """Runs gesture detection to control Spotify playback."""
        cap = cv2.VideoCapture(0)
        with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            with self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False
                    holistic_results = holistic.process(image)
                    face_results = face_mesh.process(image)

                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    self._draw_landmarks(image, holistic_results, face_results)
                    self._process_wave(holistic_results)
                    self._process_play_pause(holistic_results)

                    cv2.imshow('Gesture Control', image)
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break

        cap.release()
        cv2.destroyAllWindows()

    def _draw_landmarks(self, image, holistic_results, face_results):
        """Draws the holistic and face landmarks."""
        if holistic_results.left_hand_landmarks:
            self.mp_drawing.draw_landmarks(image, holistic_results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
        if holistic_results.right_hand_landmarks:
            self.mp_drawing.draw_landmarks(image, holistic_results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(image, face_landmarks, self.mp_face_mesh.FACEMESH_TESSELATION)

    def _process_wave(self, results):
        """Detects a full wave gesture to skip the song."""
        current_time = time.time()
        if current_time - self.last_wave_command_time < self.command_cooldown:
            return  # Skip if cooldown has not passed

        hand_landmarks = results.right_hand_landmarks or results.left_hand_landmarks
        if hand_landmarks:
            wrist_x = hand_landmarks.landmark[self.mp_holistic.HandLandmark.WRIST].x

            if self.previous_wrist_x is None:
                # Initialize the first position
                self.previous_wrist_x = wrist_x

            # Detect direction changes for a full wave
            elif abs(wrist_x - self.previous_wrist_x) > self.wave_threshold:
                if self.wave_direction is None:
                    # Set the initial wave direction
                    self.wave_direction = "right" if wrist_x > self.previous_wrist_x else "left"
                elif self.wave_direction == "right" and wrist_x < self.previous_wrist_x:
                    # First direction was right, now moving left - wave confirmed
                    self.wave_confirmed = True
                    self.wave_direction = None  # Reset for next wave detection
                elif self.wave_direction == "left" and wrist_x > self.previous_wrist_x:
                    # First direction was left, now moving right - wave confirmed
                    self.wave_confirmed = True
                    self.wave_direction = None  # Reset for next wave detection

                # Execute command if wave is confirmed
                if self.wave_confirmed:
                    print("Full wave detected - skipping song")
                    self.spotify_controller.skip_song()
                    self.last_wave_command_time = current_time
                    self.wave_confirmed = False  # Reset after executing command

            # Update the previous wrist position
            self.previous_wrist_x = wrist_x

    def _process_play_pause(self, results):
        """Detects play/pause gesture."""
        current_time = time.time()
        if current_time - self.last_play_pause_command_time < self.command_cooldown:
            return  # Skip if cooldown has not passed

        hand_landmarks = results.right_hand_landmarks or results.left_hand_landmarks
        if hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[self.mp_holistic.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[self.mp_holistic.HandLandmark.THUMB_TIP]
            distance = ((index_finger_tip.x - thumb_tip.x) ** 2 + (index_finger_tip.y - thumb_tip.y) ** 2) ** 0.5

            if distance < 0.1:
                if self.spotify_controller.is_playing():
                    print("Play/Pause gesture detected - pausing song")
                    self.spotify_controller.pause_song()
                else:
                    print("Play/Pause gesture detected - playing song")
                    self.spotify_controller.play_song()
                
                # Update last command time for play/pause
                self.last_play_pause_command_time = current_time
