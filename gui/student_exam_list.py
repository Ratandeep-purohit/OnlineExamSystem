import tkinter as tk
from tkinter import messagebox, ttk
from backend.db_manager import fetch_exams
from gui.ui_config import *
from gui.take_exam import TakeExam
class StudentExamList(tk.Frame):
    def __init__(self, parent, student_id):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.parent = parent
        self.student_id = student_id
        self.create_exam_list()
    
    def create_exam_list(self):
        if hasattr(self.parent, 'content_frame'):
            self.parent.content_frame.destroy()
        self.parent.content_frame = tk.Frame(self.parent, bg=BACKGROUND_COLOR)
        self.parent.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)
        
        tk.Label(self.parent.content_frame, text="Upcoming Exams", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)
        
        self.exam_tree = ttk.Treeview(self.parent.content_frame, columns=("ID", "Title", "Subject", "Duration"), show="headings")
        self.exam_tree.heading("ID", text="ID")
        self.exam_tree.heading("Title", text="Title")
        self.exam_tree.heading("Subject", text="Subject")
        self.exam_tree.heading("Duration", text="Duration")
        self.exam_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        take_exam_btn = tk.Button(self.parent.content_frame, text="Take Exam", font=BUTTON_FONT, bg=PRIMARY_COLOR, fg="white", command=self.take_exam)
        take_exam_btn.pack(pady=10)
        take_exam_btn.bind("<Enter>", lambda e: take_exam_btn.config(bg=BUTTON_HOVER_COLOR))
        take_exam_btn.bind("<Leave>", lambda e: take_exam_btn.config(bg=PRIMARY_COLOR))
        
        self.load_exams()
    
    def load_exams(self):
        exams = fetch_exams()
        if not exams:
            messagebox.showinfo("No Exams", "No upcoming exams.")
            return
        
        for exam in exams:
            self.exam_tree.insert("", tk.END, values=(exam["_id"], exam["subject"], exam["subject"], exam.get("duration","N/A")))
    
    def take_exam(self):
        selected_item = self.exam_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an exam to take.")
            return
        
        exam_id = self.exam_tree.item(selected_item, "values")[0]
        messagebox.showinfo("Take Exam", f"Starting Exam: {exam_id}")
        TakeExam(self.parent, self.student_id, exam_id)
