import cv2
import face_recognition
import numpy as np
from tkinter import messagebox

def open_face_capture(callback):
    cap = cv2.VideoCapture(0)
    face_detected = False
    captured_face = None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            captured_face = rgb_frame  # Store the face image in RGB format
            face_detected = True

        cv2.imshow("Face Capture - Press 'c' to Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('c') and face_detected:
            break
    
    cap.release()
    cv2.destroyAllWindows()

    if captured_face is not None:
        callback(captured_face)  # ✅ Return the captured face image
    else:
        messagebox.showerror("Error", "No face detected, try again!")

def capture_face_for_registration(callback):
    """Capture face for registration."""
    open_face_capture(callback)

def capture_face():
    """Capture face for login and return the image."""
    captured_face = None
    def set_face(face):
        nonlocal captured_face
        captured_face = face
    open_face_capture(set_face)
    return captured_face


