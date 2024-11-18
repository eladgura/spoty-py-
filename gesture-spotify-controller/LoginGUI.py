import tkinter as tk
from tkinter import messagebox
import cv2  # OpenCV is used for capturing and processing video frames.


class LoginRegisterGUI:
    def __init__(self):
        self.result = None

    def start_gui(self):
        """Start the GUI and return the result."""
        self.window = tk.Tk()
        self.window.title("Login/Register")
        self.window.geometry("400x300")
        self.create_main_menu()
        self.window.mainloop()
        return self.result  # Return the result after GUI closes

    def create_main_menu(self):
        """Create the main menu with options."""
        tk.Label(self.window, text="Face Recognition System", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.window, text="Register", command=self.register).pack(pady=10)
        tk.Button(self.window, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.window, text="Exit", command=self.exit_program).pack(pady=10)

    def register(self):
        """Handle the registration process."""
        messagebox.showinfo("Info", "Registration: Position yourself in front of the camera.")
        try:
            if self.face_capture("register"):  # Simulate face capture and storage.
                messagebox.showinfo("Success", "Face registered successfully!")
            else:
                messagebox.showwarning("Failed", "Face registration failed. Try again.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register face: {str(e)}")

    def login(self):
        """Handle the login process."""
        messagebox.showinfo("Info", "Login: Position yourself in front of the camera.")
        try:
            if self.face_capture("login"):  # Simulate face matching.
                messagebox.showinfo("Success", "Login successful!")
                self.result = "logged_in"
                self.window.quit()  # Close the GUI
            else:
                messagebox.showwarning("Failed", "Face not recognized. Try again.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to log in: {str(e)}")

    def exit_program(self):
        """Exit the program."""
        self.result = "exit"
        self.window.quit()

    def face_capture(self, mode):
        """Simulate face capture and processing."""
        # Open the webcam for video capture.
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Cannot access the camera")

        cv2.namedWindow("Face Recognition")
        face_detected = False
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    raise Exception("Failed to read from camera.")

                # Display the video frame.
                cv2.imshow("Face Recognition", frame)
                cv2.putText(frame, "Press 'q' to confirm detection, or 'ESC' to exit.", 
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                # Check for user input.
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):  # Confirm detection.
                    face_detected = True
                    break
                elif key == 27:  # ESC key to cancel.
                    break
        finally:
            # Ensure resources are released properly.
            cap.release()
            cv2.destroyAllWindows()

        if mode == "register" and face_detected:
            # Placeholder logic for saving face data.
            print("Simulated: Face data saved for registration.")
            return True
        elif mode == "login" and face_detected:
            # Placeholder logic for verifying face data.
            print("Simulated: Face data matched for login.")
            return True
        return False
