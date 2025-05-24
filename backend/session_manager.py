import json
import os

SESSION_FILE = "session.json"

def save_session(user_id, role):
    if not user_id or not role:
        print("❌ ERROR: Cannot save empty session data!")
        return

    session_data = {"user_id": str(user_id), "role": role}
    try:
        print(f"📝 Attempting to save session: {session_data}")  # ✅ Debugging print
        with open("session.json", "w") as file:
            json.dump(session_data, file)
        print(f"✅ Session saved successfully: {session_data}")  # Debugging print
    except Exception as e:
        print(f"❌ ERROR in save_session: {e}")

def load_session():
    if not os.path.exists("session.json"):
        print("❌ ERROR: Session file not found! Creating a new one.")  
        try:
            with open("session.json", "w") as file:
                json.dump({}, file)  # ✅ Creates an empty session file  
        except Exception as e:
            print(f"❌ ERROR in load_session (creating new file): {e}")
        return None

    try:
        with open("session.json", "r") as file:
            session_data = json.load(file)
            if not session_data:  # ✅ Handle empty JSON file
                print("❌ ERROR: Session file is empty!")
                
                return None
            if "user_id" not in session_data or "role" not in session_data:
                print("❌ ERROR: Invalid session data!")
                return None
            return session_data
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Corrupt session file! Resetting session. Details: {e}")
        try:
            os.remove("session.json")  # ✅ Delete corrupt session file
        except Exception as e:
            print(f"❌ ERROR in load_session (removing corrupt file): {e}")
        return None
    except Exception as e:
        print(f"❌ ERROR in load_session: {e}")
        return None

def clear_session():
    """Clears the user session."""
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
            print("✅ Session cleared successfully.")
    except Exception as e:
        print(f"❌ ERROR in clear_session: {e}")

def is_logged_in():
    """Checks if a user is logged in."""
    try:
        return os.path.exists(SESSION_FILE)
    except Exception as e:
        print(f"❌ ERROR in is_logged_in: {e}")
        return False

def logout():
    """Logs out the current user by clearing the session."""
    try:
        clear_session()
        print("✅ Logged out successfully.")
    except Exception as e:
        print(f"❌ ERROR in logout: {e}")

def validate_session(session):
    required_keys = ["role", "user_id"]
    return all(key in session for key in required_keys)