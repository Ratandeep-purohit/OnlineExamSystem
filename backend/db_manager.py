from backend.database import db_instance
from bson.objectid import ObjectId
from datetime import datetime
from tkinter import messagebox

def create_exam(data):
    """Creates an exam and stores it in MongoDB."""
    exam_id = db_instance.insert_one("exams", data)
    if exam_id:
        print(f"✅ Exam created successfully! Exam ID: {exam_id}")
    else:
        print("❌ Error creating exam.")
    return exam_id

def fetch_exams():
    """Fetch all exams from MongoDB."""
    return db_instance.get_all_exams()

def delete_exam(exam_id):
    """Delete an exam from the database."""
    try:
        return db_instance.delete_one("exams", {"_id": ObjectId(exam_id)})
    except Exception as e:
        print("❌ Error deleting exam:", e)
        return False

def update_exam(exam_id, updated_data):
    """Update an exam in the database."""
    try:
        return db_instance.update_one("exams", {"_id": ObjectId(exam_id)}, updated_data)
    except Exception as e:
        print("❌ Error updating exam:", e)
        return False
    
def exam_submission(data):
    """Insert exam submission data into the database."""
    submission_id = db_instance.insert_one("submissions", data)
    if submission_id:
        calculate_and_store_results(data["student_id"], data["exam_id"], data["answers"])
        print("✅ Exam submitted successfully!")
        return True
    else:
        print("❌ Failed to submit exam.")
        return False

def calculate_and_store_results(student_id, exam_id, submitted_answers):
    """Check submitted answers against correct answers, generate score, and store result."""
    exam_id = ObjectId(exam_id) if ObjectId.is_valid(exam_id) else None
    try:
        exam = db_instance.find_one("exams", {"_id": ObjectId(exam_id)})
    except Exception as e: 
        print("❌ Error fetching exam:", e)
        return False
    
    if not exam:
        print("❌ Error: Exam not found!")
        return False
    
    correct_answers = {str(i): q["right_answer"] for i, q in enumerate(exam["questions"])}
    score = sum(1 for q_id, answer in submitted_answers.items() if correct_answers.get(q_id) == answer)
    
    result_data = {
        "student_id": student_id,
        "exam_id": exam_id,
        "score": score,
        "submitted_at": datetime.utcnow(),
        "subject": exam.get("subject", "Unknown")
    }
    
    result_id = db_instance.insert_one("results", result_data)
    if result_id:
        print(f"✅ Result stored successfully for Student {student_id}, Score: {score}")
        return True
    else:
        print("❌ Error storing result.")
        return False

def fetch_exam_results(student_id=None):
    """Fetch exam results from the database."""
    if student_id: 
        stats_dict = db_instance.find_all("results", {"student_id": student_id})
        return list(stats_dict)
    else:
        return db_instance.get_all_results()
    
def fetch_admin_stats():
    """Fetch overall statistics for admin dashboard."""
    total_exams = db_instance.count_documents("exams", {})
    total_students = db_instance.count_documents("users", {"role": "student"})
    total_teachers = db_instance.count_documents("users", {"role": "teacher"})
    
    results = db_instance.get_all_results()
    total_scores = sum(result["score"] for result in results if "score" in result)
    average_score = round(total_scores / len(results), 2) if results else 0
    
    return {
        "total_exams": total_exams,
        "total_students": total_students,
        "total_teachers": total_teachers,
        "average_score": average_score,
        "exam_titles": [exam["subject"] for exam in db_instance.get_all_exams()],
        "exam_averages": [round(sum(res["score"] for res in db_instance.find_all("results", {"exam_id": exam["_id"]})) / db_instance.count_documents("results", {"exam_id": exam["_id"]}), 2) if db_instance.count_documents("results", {"exam_id": exam["_id"]}) else 0 for exam in db_instance.get_all_exams()]
    }

def fetch_all_users():
    """Fetch all users (students & teachers) from the database."""
    return db_instance.find_all("users", {})

def add_user(name, email, role, password):
    """Add a new user to the database."""
    existing_user = db_instance.find_one("users", {"email": email})
    if existing_user:
        messagebox.showerror("Error", "User with this email already exists!")
        return False
    user_data = {"name": name, "email": email, "role": role, "password": password}
    return db_instance.insert_one("users", user_data)

def edit_user(user_id, updated_data):
    """Modify user details."""
    try:
        return db_instance.update_one("users", {"_id": ObjectId(user_id)}, updated_data)
    except Exception as e:
        print("❌ Error updating user:", e)
        return False

def delete_user(user_id):
    """Remove a user from the database."""
    try:
        return db_instance.delete_one("users", {"_id": ObjectId(user_id)})
    except Exception as e:
        print("❌ Error deleting user:", e)
        return False
    
def fetch_exam_by_id(exam_id):
    """Fetch Exam from DB """
    try:
        return db_instance.find_one("exams", {"_id": ObjectId(exam_id)})
    except Exception as e:
        print("❌ Error! fail to fetch exam:", e)
        return False

def fetch_student_stats(student_id):
    try:
        
        stats= {
            "upcoming exam": db_instance.count_documents("exams"),
            "completed_exam": db_instance.count_documents("submissions",{"student_id":ObjectId(student_id)}),
            "Average_score":  average_score()
        }
        def average_score():
            results_data = db_instance.find_all("results",{"student_id":ObjectId(student_id)})
            if not results_data:
                return 0
            
            total_score = 0
            num_exams = 0

            for result in results_data:
                if isinstance(result, dict) and "score" in result:
                    total_score += result.get("score", 0)
                    num_exams += 1

            # Avoid division by zero
            if num_exams == 0:
                return 0

            average_score = total_score / num_exams
            return round(average_score, 2) 
        
        return stats

    except Exception as e:
        print("❌ Failed to get stats!")
        return False


def fetch_all_users(role):
    users = db_instance.find_all("users",{"role": role})
    return list(users)