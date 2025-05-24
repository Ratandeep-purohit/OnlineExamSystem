import cv2
import face_recognition
import numpy as np
from tkinter import messagebox, Toplevel, Label , Canvas, PhotoImage
import threading
import time

class FaceMonitor:
    def __init__(self, root ,on_face_missing):
        self.root = root
        self.on_face_missing = on_face_missing # callback function to call when face is missing
        self.running = False
        self.face_window = None
        self.canvas = None
        self.cap = None

    def start_monitoring(self, frame):
        """Start face monitoring in a separate thread."""
        self.running = True
        self.frame = frame
        thread = threading.Thread(target=self.monitor_face)
        thread.daemon = True
        thread.start()
    
    def stop_monitoring(self):
        """Stop face monitoring."""
        self.running = False

    def monitor_face(self):
        """Continuously monitor the face using the webcam."""
        self.cap = None
        for cam_index in range(3):
            temp_cap = cv2.VideoCapture(cam_index)
            if temp_cap.isOpened():
                self.cap = temp_cap
                break
            temp_cap.release()

        if self.cap is None or not self.cap.isOpened():
            messagebox.showerror("Error", "Cannot access webcam. Please check your camera settings.")
            return
        
        face_missing_count = 0 # Counts the number of frames where face is missing

        self.canvas = Canvas(self.frame, width=200, height=200)
        self.canvas.pack(pady=5)

        self.face_label = Label(self.frame, text="Loading Camera...", font=("Arial", 12))
        self.face_label.pack()
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)

            frame = cv2.resize(frame, (200, 200))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = PhotoImage(data=cv2.imencode('.ppm', frame)[1].tobytes())

            self.root.after(0, self.update_canvas, img)
            
            if len(face_locations) == 0:
                face_missing_count += 1
                if self.face_label.winfo_exists():
                    self.face_label.config(text="Face Missing", fg="red")
            else:
                face_missing_count = 0 # Reset the count if face is detected 
                if self.face_label.winfo_exists():
                    self.face_label.config(text="Face Detected", fg="green")

            if face_missing_count >= 5:
                self.on_face_missing()
                break

            time.sleep(0.5) # Delay to reduce CPU usage

        self.cap.release()
        self.stop_monitoring()

    def update_canvas(self, img):
        if self.canvas.winfo_exists():
            self.canvas.img = img  # Retain reference to prevent garbage collection
            self.canvas.create_image(0, 0, anchor="nw", image=img)
