import cv2
import json
import mediapipe as mp

class FaceRecognition:
    def __init__(self):
        # Initialize Mediapipe for Face Detection
        self.mp_face = mp.solutions.face_detection
        self.face_detection = self.mp_face.FaceDetection(min_detection_confidence=0.2)

        # Initialize OpenCV for Webcam
        self.cap = cv2.VideoCapture(0)
        self.user_db_file = "user_db.json"
    
    def load_user_db(self):
        """Loads the user database from the JSON file."""
        try:
            with open(self.user_db_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_user_db(self, user_db):
        """Saves the user database to the JSON file."""
        with open(self.user_db_file, 'w') as f:
            json.dump(user_db, f, indent=4)

    def extract_face_features(self, frame):
        """Extracts the face features (bounding box) from a given frame."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)
        if results.detections:
            face = results.detections[0].location_data.relative_bounding_box
            return (face.xmin, face.ymin, face.width, face.height)
        return None

    def register(self):
        """Handles user registration by capturing and storing face features."""
        user_db = self.load_user_db()
        
        username = input("Enter your name: ")
        user_id = input("Enter your unique user ID: ")
        
        print("Please look into the camera for face registration.")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break
            
            face_features = self.extract_face_features(frame)
            
            if face_features:
                # Store the face features (bounding box), name, and ID in the user_db
                user_db[user_id] = {"name": username, "features": face_features}
                self.save_user_db(user_db)
                print(f"User {username} (ID: {user_id}) registered successfully!")
                break
            
            # Show webcam feed
            cv2.imshow("Register - Face Capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def login(self):
        """Handles user login by comparing the captured face with stored features."""
        user_db = self.load_user_db()
        
        user_id = input("Enter your user ID to log in: ")
        
        if user_id not in user_db:
            print(f"No user found with ID {user_id}.")
            return False
        
        stored_face = user_db[user_id]["features"]
        username = user_db[user_id]["name"]
        
        print(f"Welcome, {username}. Please look into the camera to verify your face.")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break
            
            face_features = self.extract_face_features(frame)
            
            if face_features:
                # Compare bounding box coordinates (simplified matching)
                if (abs(face_features[0] - stored_face[0]) < 0.1 and
                    abs(face_features[1] - stored_face[1]) < 0.1 and
                    abs(face_features[2] - stored_face[2]) < 0.1 and
                    abs(face_features[3] - stored_face[3]) < 0.1):
                    print(f"Login successful! Welcome back, {username}.")
                    return True
                else:
                    print("Face does not match.")
                    return False
            
            # Show webcam feed
            cv2.imshow("Login - Face Capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def close(self):
        """Releases the webcam and closes any OpenCV windows."""
        self.cap.release()
        cv2.destroyAllWindows()
