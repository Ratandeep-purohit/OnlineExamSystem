import bcrypt
import cv2
import jwt
import os
import numpy as np
import face_recognition
from backend.database import db_instance
from datetime import datetime, timedelta


SECRET_KEY = "your_secret_key"

class Auth:
    @staticmethod
    def register(first_name,last_name,email, password, face_image, role):
        existing_user = db_instance.find_one("users", {"email": email})
        print("Existing user:", existing_user)
        if existing_user:
            print("User already exists")
            return False  # User already exists

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        face_image = cv2.resize(face_image, (320, 240))

        face_encoding = face_recognition.face_encodings(face_image,model='cnn')
        face_locations = face_recognition.face_locations(face_image,model='cnn')
        print("Detected face locations:", face_locations)
        print("Image shape:", face_image.shape)
        print("Face encoding:", face_encoding)
        if not face_encoding:
            print("No face detected")
            return False  # No face detected

        user = {
            "first_name": first_name,
            "last_name":last_name,
            "email": email,
            "password": hashed_password.decode(),
            "face_encoding": face_encoding[0].tolist(),
            "role": role  # Store user role
        }
        db_instance.insert_one("users", user)
        print("User registered successfully")
        return user

    @staticmethod
    def login(email, password):
        user = db_instance.find_one("users", {"email": email})
        if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
            return user
        return None

    @staticmethod
    def face_login(email, captured_face):
        user = db_instance.find_one("users", {"email": email})
        if not user or "face_encoding" not in user:
            return None

        stored_encoding = np.array(user["face_encoding"])
        captured_encoding = face_recognition.face_encodings(captured_face)
        if not captured_encoding:
            print("❌ No face detected")
            return None  # No face detected

        match = face_recognition.compare_faces([stored_encoding], captured_encoding[0])
        if match[0]:  # Ensure matching is done properly
            return user
        else:
            print("❌ Face did not match!")
            return None



    @staticmethod
    def generate_token(email):
        payload = {
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

