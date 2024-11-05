import cv2
import mediapipe as mp
import time

class GestureController:
    def __init__(self, spotify_controller):
        self.spotify_controller = spotify_controller

        # Initialize the holistic and drawing modules from mediapipe
        self.mp_holistic = mp.solutions.holistic
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils

        # Wave detection variables
        self.previous_wrist_x = None
        self.wave_count = 0
        self.wave_threshold = 0.05  # Adjust this value for sensitivity
        self.wave_reset_time = 1.5
        self.last_wave_time = time.time()

        # Play/pause detection variables
        self.currently_playing = True

    def detect_gestures(self):
        cap = cv2.VideoCapture(0)
        
        with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            with self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Process image
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False
                    holistic_results = holistic.process(image)
                    face_results = face_mesh.process(image)

                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    # Draw landmarks
                    self._draw_holistic_landmarks(image, holistic_results)
                    self._draw_face_landmarks(image, face_results)

                    # Process gestures
                    self._process_wave(holistic_results)
                    self._process_play_pause(holistic_results)
                    self._process_face_gestures(face_results)

                    cv2.imshow('Gesture Control', image)

                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break

        cap.release()
        cv2.destroyAllWindows()

    def _draw_holistic_landmarks(self, image, results):
        """Draws the holistic landmarks on the image."""
        if results.left_hand_landmarks:
            self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)

        if results.right_hand_landmarks:
            self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)

        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS)

    def _draw_face_landmarks(self, image, results):
        """Draws the face landmarks on the image."""
        if results.multi_face_landmarks:
         for face_landmarks in results.multi_face_landmarks:
            if hasattr(self.mp_face_mesh, 'FACE_CONNECTIONS'):
                self.mp_drawing.draw_landmarks(image, face_landmarks, self.mp_face_mesh.FACE_CONNECTIONS)
            else:
                self.mp_drawing.draw_landmarks(image, face_landmarks, self.mp_face_mesh.FACEMESH_TESSELATION)
                

    def _process_wave(self, results):
        """Detects a wave gesture to skip the song."""
        hand_landmarks = (results.left_hand_landmarks or results.right_hand_landmarks)

        if hand_landmarks:
            wrist_x = hand_landmarks.landmark[self.mp_holistic.HandLandmark.WRIST].x
            
            if self.previous_wrist_x is None:
                self.previous_wrist_x = wrist_x
            
            if abs(wrist_x - self.previous_wrist_x) > self.wave_threshold:
                if time.time() - self.last_wave_time > self.wave_reset_time:
                    if wrist_x > self.previous_wrist_x:
                        print("Wave detected - skipping song")
                        self.spotify_controller.skip_song()
                    self.last_wave_time = time.time()
                self.previous_wrist_x = wrist_x

    def _process_play_pause(self, results):
        """Detects play/pause gesture based on hand position."""
        hand_landmarks = (results.left_hand_landmarks or results.right_hand_landmarks)

        if hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[self.mp_holistic.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[self.mp_holistic.HandLandmark.THUMB_TIP]

            distance = ((index_finger_tip.x - thumb_tip.x) ** 2 + (index_finger_tip.y - thumb_tip.y) ** 2) ** 0.5
            
            if distance < 0.1:  # Adjust the threshold as needed
                if self.currently_playing:
                    print("Play/Pause gesture detected - pausing song")
                    self.spotify_controller.pause_song()
                else:
                    print("Play/Pause gesture detected - playing song")
                    self.spotify_controller.play_song()
                
                self.currently_playing = not self.currently_playing

    def _process_face_gestures(self, results):
        """Detects smile as a facial gesture to skip songs."""
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]

            left_mouth_corner = face_landmarks.landmark[61]
            right_mouth_corner = face_landmarks.landmark[291]
            upper_lip_center = face_landmarks.landmark[13]
            lower_lip_center = face_landmarks.landmark[14]

            smile_width = abs(right_mouth_corner.x - left_mouth_corner.x)
            smile_height = abs(upper_lip_center.y - lower_lip_center.y)

            if smile_height / smile_width > 0.3:  # Adjust as needed
                print("Smile detected - skipping song")
                self.spotify_controller.skip_song()
