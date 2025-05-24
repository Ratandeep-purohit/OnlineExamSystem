import tkinter as tk
from tkinter import messagebox, ttk
from backend.db_manager import fetch_exam_results
from gui.ui_config import PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR, TITLE_FONT, LABEL_FONT, BUTTON_FONT, BUTTON_HOVER_COLOR, PADDING
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StudentResults(tk.Frame):
    def __init__(self, parent, student_id):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.parent = parent
        self.student_id = student_id
        self.create_results_view()
    
    def create_results_view(self):
        if hasattr(self.parent, 'content_frame'):
            self.parent.content_frame.destroy()
        self.parent.content_frame = tk.Frame(self.parent, bg=BACKGROUND_COLOR)
        self.parent.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)
        
        tk.Label(self.parent.content_frame, text="Exam Results", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)
        
        self.results_tree = ttk.Treeview(self.parent.content_frame, columns=( "Title", "Score", "Status"), show="headings")
        #self.results_tree.heading("Exam ID", text="Exam ID")
        self.results_tree.heading("Title", text="Title")
        self.results_tree.heading("Score", text="Score")
        self.results_tree.heading("Status", text="Status")
        self.results_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.load_results()
        self.create_chart()
    
    def load_results(self):
        self.results_data = fetch_exam_results(self.student_id)
        if not self.results_data:
            messagebox.showinfo("No Results", "No exam results available.")
            return
        for result in self.results_data:
            if isinstance(result, dict):
                self.results_tree.insert(
                    "",
                    tk.END,
                values=(
                    result.get("subject", "N/A"),
                    result.get("score", "N/A"),
                    "Passed" if result.get("score", 0) >= 50 else "Failed"
                )
            )
        else:
            print(f"Invalid result format: {result}")
    
    def create_chart(self):
        if not self.results_data:
            return
        
        titles = [result.get("subject", "N/A") for result in self.results_data if isinstance(result, dict)]
        scores = [result.get("score", 0) for result in self.results_data if isinstance(result, dict)]
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(titles, scores, color=PRIMARY_COLOR)
        ax.set_xlabel("Scores")
        ax.set_title("Exam Performance")
        
        canvas = FigureCanvasTkAgg(fig, master=self.parent.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
