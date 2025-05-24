import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from backend.db_manager import fetch_admin_stats
from gui.ui_config import *

class AdminDashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.parent = parent
        self.create_dashboard()
    
    def create_dashboard(self):
        if hasattr(self.parent, 'content_frame'):
            self.parent.content_frame.destroy()
        self.parent.content_frame = tk.Frame(self.parent, bg=BACKGROUND_COLOR)
        self.parent.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)
        
        tk.Label(self.parent.content_frame, text="Admin Dashboard", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)
        
        stats = fetch_admin_stats()
        if stats:
            tk.Label(self.parent.content_frame, text=f"Total Exams: {stats['total_exams']}", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
            tk.Label(self.parent.content_frame, text=f"Total Teachers: {stats['total_teachers']}", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
            tk.Label(self.parent.content_frame, text=f"Total Students: {stats['total_students']}", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
            tk.Label(self.parent.content_frame, text=f"Average Exam Score: {stats['average_score']}%", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
        
        self.create_performance_chart(stats)

    
    def create_performance_chart(self, stats):
        if not stats or not stats['exam_titles']:
            return
        
        fig, ax = plt.subplots(figsize=(12,10))
        ax.bar(stats['exam_titles'], stats['exam_averages'], color=PRIMARY_COLOR)
        ax.set_xlabel("Exams")
        ax.set_ylabel("Average Score")
        ax.set_title("Overall Exam Performance")
        ax.set_xticklabels(stats['exam_titles'], rotation=45, ha="right")
        
        canvas = FigureCanvasTkAgg(fig, master=self.parent.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
    
