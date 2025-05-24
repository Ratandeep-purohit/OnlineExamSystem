import tkinter as tk
from tkinter import messagebox
import threading
from backend.db_manager import fetch_exam_by_id, exam_submission
from backend.face_monitor import FaceMonitor
from gui.ui_config import *
from datetime import datetime

class TakeExam(tk.Frame):
    def __init__(self, parent, student_id, exam_id):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.parent = parent
        self.exam_id = exam_id
        self.student_id = student_id
        print(f"student_id: {student_id}")
        self.selected_answers = {}
        
        self.create_exam_interface()
        
    
        
        self.after(3600000,self.auto_submit)
    
    def create_exam_interface(self):
        if hasattr(self.parent, 'content_frame'):
            self.parent.content_frame.destroy()
        self.parent.content_frame = tk.Frame(self.parent, bg=BACKGROUND_COLOR)
        self.parent.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)
        
        exam = fetch_exam_by_id(self.exam_id)
        if not exam:
            messagebox.showerror("Error", "Exam not found!")
            return
        
        tk.Label(self.parent.content_frame, text=exam.get("title", "subject"), font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)
        
        self.question_frames = []
        for i, question in enumerate(exam["questions"], start=1):
            frame = tk.Frame(self.parent.content_frame, bg=BACKGROUND_COLOR)
            frame.pack(pady=5, fill=tk.X)
            
            tk.Label(frame, text=f"Q{i}: {question['question_text']}", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(anchor="w")
            
            var = tk.StringVar(value="")
            self.selected_answers[i] = var
            
            for option in question["options"]:
                tk.Radiobutton(frame, text=option, variable=var, value=option, bg=BACKGROUND_COLOR, font=LABEL_FONT, fg=TEXT_COLOR, selectcolor=PRIMARY_COLOR).pack(anchor="w")
            
            self.question_frames.append(frame)

        # Place the face monitor at the bottom-rigth corner
        self.face_monitor_frame = tk.Frame(self.parent.content_frame, width=250, height=200, bg="white")
        self.face_monitor_frame.place(relx=0.98, rely=0.98, anchor="se")

        self.face_monitor = FaceMonitor(self.face_monitor_frame, self.auto_submit)
        self.monitor_thread = threading.Thread(target=self.face_monitor.start_monitoring,args=(self.face_monitor_frame,), daemon=True)
        self.monitor_thread.start()
        
        submit_btn = tk.Button(self.parent.content_frame, text="Submit Exam", font=BUTTON_FONT, bg=PRIMARY_COLOR, fg="white", command=self.submit_exam)
        submit_btn.pack(pady=10)
        submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg=BUTTON_HOVER_COLOR))
        submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg=PRIMARY_COLOR))
    
    def submit_exam(self,alert):
        if alert : 

            exam_data = {
            "exam_id" : self.exam_id,
            "student_id" : self.student_id,
            "answers" :{str(i): var.get() for i, var in self.selected_answers.items()},
            "submitted_at": datetime.utcnow(),
            "alert": alert
            }
            success = exam_submission(exam_data)
        else :
            
            exam_data = {
            "exam_id" : self.exam_id,
            "student_id" : self.student_id,
            "answers" :{str(i): var.get() for i, var in self.selected_answers.items()},
            "submitted_at": datetime.utcnow(),
            "alert": None
            }
            success = exam_submission(exam_data)
        self.face_monitor.stop_monitoring()
        if success:
            messagebox.showinfo("Success", "Exam submitted successfully!")
            self.parent.load_dashboard()
        else:
            messagebox.showerror("Error", "Failed to submit exam!")
    
    def auto_submit(self):
        messagebox.showerror("Exam Violation!", "Exam auto-submitted due to suspicious behaviour.")
        alert = "Exam Violation!", "Exam auto-submitted due to suspicious behaviour."
        self.submit_exam(alert)
