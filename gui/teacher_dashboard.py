import tkinter as tk
from tkinter import messagebox
from gui.ui_config import PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR, TITLE_FONT, LABEL_FONT, BUTTON_FONT, BUTTON_HOVER_COLOR, PADDING

class TeacherDashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.parent = parent
        self.create_dashboard()
    
    def create_dashboard(self):
        if hasattr(self.parent, 'content_frame'):
            self.parent.content_frame.destroy()
        self.parent.content_frame = tk.Frame(self.parent, bg=BACKGROUND_COLOR)
        self.parent.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)
        
        tk.Label(self.parent.content_frame, text="Teacher Dashboard", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)
        
        stats_frame = tk.Frame(self.parent.content_frame, bg=BACKGROUND_COLOR)
        stats_frame.pack(pady=20)
        
        tk.Label(stats_frame, text="Total Exams Created: 8", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=20, pady=10)
        tk.Label(stats_frame, text="Total Students: 120", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=1, padx=20, pady=10)
        tk.Label(stats_frame, text="Average Exam Score: 78%", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=2, padx=20, pady=10)
        
        btn_frame = tk.Frame(self.parent.content_frame, bg=BACKGROUND_COLOR)
        btn_frame.pack(pady=20)
        
        create_exam_btn = tk.Button(btn_frame, text="Create Exam", font=BUTTON_FONT, bg=PRIMARY_COLOR, fg="white", command=self.create_exam)
        create_exam_btn.grid(row=0, column=0, padx=10)
        create_exam_btn.bind("<Enter>", lambda e: create_exam_btn.config(bg=BUTTON_HOVER_COLOR))
        create_exam_btn.bind("<Leave>", lambda e: create_exam_btn.config(bg=PRIMARY_COLOR))
        
        view_exams_btn = tk.Button(btn_frame, text="View Exams", font=BUTTON_FONT, bg=PRIMARY_COLOR, fg="white", command=self.view_exams)
        view_exams_btn.grid(row=0, column=1, padx=10)
        view_exams_btn.bind("<Enter>", lambda e: view_exams_btn.config(bg=BUTTON_HOVER_COLOR))
        view_exams_btn.bind("<Leave>", lambda e: view_exams_btn.config(bg=PRIMARY_COLOR))
    
    def create_exam(self):
        messagebox.showinfo("Create Exam", "Open Create Exam Page")

    def view_exams(self):
        messagebox.showinfo("View Exams", "Open View Exams Page")
    
    def logout(self):
        messagebox.showinfo("Logout", "Logging out...")
        self.parent.destroy()
