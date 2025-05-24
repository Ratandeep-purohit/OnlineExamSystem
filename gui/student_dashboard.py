import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from backend.db_manager import fetch_student_stats
from gui.ui_config import *
from gui.student_exam_list import StudentExamList
from gui.student_results import StudentResults

class StudentDashboard(tk.Frame):
    def __init__(self, parent, student_id):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.parent = parent
        self.student_id = student_id
    
        self.create_dashboard()
    
    
    def create_dashboard(self):
        if hasattr(self.parent, 'content_frame'):
            self.parent.content_frame.destroy()
        self.parent.content_frame = tk.Frame(self.parent, bg=BACKGROUND_COLOR)
        self.parent.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)
        
        tk.Label(self.parent.content_frame, text="Student Dashboard", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)
        
        stats_data = fetch_student_stats(self.student_id)
        if stats_data and isinstance(stats_data, list) and len(stats_data) > 0:
            stats = stats_data  # Get the first item if it's a list
            
        else:
            stats = {"upcoming_exams": 0, "completed_exams": 0, "average_score": 0, "subject": [], "score": []}

        stats_frame = tk.Frame(self.parent.content_frame, bg=BACKGROUND_COLOR)
        stats_frame.pack(pady=20)
        
        tk.Label(stats_frame, text=f"Upcoming Exams: {stats.get('upcoming_exams',0)}", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=20, pady=10)
        tk.Label(stats_frame, text=f"Completed Exams: {stats.get('completed_exams',0)}", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=1, padx=20, pady=10)
        tk.Label(stats_frame, text=f"Average Score: {stats.get('average_score',0)}%", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=2, padx=20, pady=10)
    

        self.create_performance_chart(stats)
    
    def create_performance_chart(self, stats):
        print(f"Stats Data: {stats}")  # ✅ Add this to debug

        if not stats.get('subject',[]):
            return
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(stats['subject'], stats['score'], marker='o', linestyle='-', color=PRIMARY_COLOR)
        ax.set_xlabel("Exams")
        ax.set_ylabel("Scores")
        ax.set_title("Student Performance Trend")
        ax.set_xticks(range(len(stats['subject']))) 
        ax.set_xticklabels(stats['subject'], rotation=45, ha="right")
        
        canvas = FigureCanvasTkAgg(fig, master=self.parent.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
    
    def show_exam_list(self):
        self.parent.content_frame.destroy()
        StudentExamList(self.parent, self.student_id)
    
    def show_results(self):
        self.parent.content_frame.destroy()
        StudentResults(self.parent, self.student_id)
    
    def logout(self):
        messagebox.showinfo("Logout", "Logging out...")
        self.parent.destroy()