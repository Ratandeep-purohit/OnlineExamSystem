import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from backend.session_manager import load_session
from gui.ui_config import PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR, TITLE_FONT, BUTTON_FONT, BUTTON_HOVER_COLOR, PADDING
from gui.student_dashboard import StudentDashboard
from gui.teacher_dashboard import TeacherDashboard
from gui.admin_dashboard import AdminDashboard
from gui.student_exam_list import StudentExamList
from gui.student_results import StudentResults
from gui.create_exam import CreateExam
from gui.view_exam import ViewExam
from gui.user_management import UserManagement
from gui.teacher_performance import TeacherPerformance

class DashboardGUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.parent = parent
        self.sidebar = None
        self.content_frame = None
        self.user_role = None
        self.user_id = None
        self.initialize_dashboard()
    
    def initialize_dashboard(self):
        session = load_session()
        if session:
            self.user_role = session.get("role")
            self.user_id = session.get("user_id")
        else:
            messagebox.showerror("Error", "No active session found!")
            self.parent.destroy()
            return
        
        self.create_sidebar()
        self.load_dashboard()
    
    def create_sidebar(self):
        self.sidebar = tk.Frame(self, bg=PRIMARY_COLOR, width=200, height=600)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        buttons = [
            ("Dashboard", self.load_dashboard),
            ("Logout", self.logout)
        ]

        role_buttons = []
        
        if self.user_role == "student":
            role_buttons = [
                ("Exam List", self.show_exam_list),
                ("Results", self.show_results)
            ]
        elif self.user_role == "Teacher":
            role_buttons = [
                ("Create Exam", self.load_create_exam),
                ("View Exams", self.load_exam_list),
                ("Student Performance", self.load_performance)
            ]
        elif self.user_role == "Admin": 
            role_buttons = [
                ("Manage Users", self.load_user_management),
                ("View Stats", self.load_admin_stats)
            ]

        # Render role-based buttons first
        for text, command in role_buttons:
            btn = tk.Label(self.sidebar, text=text, font=BUTTON_FONT, bg=PRIMARY_COLOR, fg="white", padx=20, pady=10)
            btn.pack(fill=tk.X, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=PRIMARY_COLOR))
            btn.bind("<Button-1>", lambda e, c=command: c())

        
        for text, command in buttons:
            btn = tk.Label(self.sidebar, text=text, font=BUTTON_FONT, bg=PRIMARY_COLOR, fg="white", padx=20, pady=10)
            btn.pack(fill=tk.X, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BUTTON_HOVER_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=PRIMARY_COLOR))
            btn.bind("<Button-1>", lambda e, c=command: c())
    
    def load_dashboard(self):
        if self.content_frame:
            self.content_frame.destroy()
        
        self.content_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)
        
        if self.user_role == "student":
            print(f"student_id: {self.user_id}")
            StudentDashboard(self,self.user_id)
        elif self.user_role == "Teacher":
            TeacherDashboard(self)
        elif self.user_role == "Admin":
            print('Admin')
            AdminDashboard(self)
        else:
            tk.Label(self.content_frame, text="Invalid Role!", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)

    def show_exam_list(self):
        StudentExamList(self, self.user_id)
    
    def show_results(self):
        StudentResults(self,self.user_id )

    def load_create_exam(self):
        CreateExam(self)
    
    def load_exam_list(self):
        ViewExam(self)
    
    def load_performance(self):
        TeacherPerformance(self)        

    def load_user_management(self):
        # Destroy the previous frame if exists
        if self.content_frame:
            self.content_frame.destroy()
    
        self.content_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)

        # Load UserManagement only once
        if not hasattr(self, "user_management_frame"):
            self.user_management_frame = UserManagement(self.content_frame)
        else:
            self.user_management_frame.pack_forget()
            self.user_management_frame = UserManagement(self.content_frame)
    
    def load_admin_stats(self):
        AdminDashboard(self)

    def logout(self):
        messagebox.showinfo("Logout", "Logging out...")
        self.parent.logout()
