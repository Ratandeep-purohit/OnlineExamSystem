import tkinter as tk
from tkinter import ttk, messagebox
from backend.db_manager import fetch_all_users, fetch_exam_results
from gui.ui_config import PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR, TITLE_FONT, LABEL_FONT, BUTTON_FONT, BUTTON_HOVER_COLOR, PADDING
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TeacherPerformance(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.parent = parent
        self.create_performance_view()
        
    def create_performance_view(self):
        if hasattr(self.parent, 'content_frame'):
            self.parent.content_frame.destroy()
        self.parent.content_frame = tk.Frame(self.parent, bg=BACKGROUND_COLOR)
        self.parent.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)

        tk.Label(self.parent.content_frame, text="Student Performance", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.parent.content_frame, textvariable=self.search_var, font=LABEL_FONT, width=30)
        search_entry.pack(pady=5)
        search_entry.bind("<KeyRelease>", self.filter_students)

        self.students_tree = ttk.Treeview(self.parent.content_frame, columns=("Student ID", "Name"), show="headings")
        self.students_tree.heading("Student ID", text="Student ID")
        self.students_tree.heading("Name", text="Name")
        self.students_tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.students_tree.bind("<Double-1>", self.view_student_performance)

        self.load_students()

    def load_students(self):
        self.students_data = fetch_all_users("student")
        self.display_students(self.students_data)

    def display_students(self, data):
        self.students_tree.delete(*self.students_tree.get_children())
        for student in data:
            self.students_tree.insert("", tk.END, values=(student.get("student_id"), student.get("name")))

    def filter_students(self, event):
        query = self.search_var.get().lower()
        filtered_data = [student for student in self.students_data if query in student.get("name", "").lower() or query in str(student.get("student_id"))]
        self.display_students(filtered_data)

    def view_student_performance(self, event):
        selected_item = self.students_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student.")
            return

        student_id = self.students_tree.item(selected_item, "values")[0]
        student_results = fetch_exam_results(student_id)
        if not student_results:
            messagebox.showinfo("No Results", f"No exam results found for student ID {student_id}.")
            return

        self.show_performance_chart(student_results)

    def show_performance_chart(self, results):
        subjects = [result.get("subject", "N/A") for result in results]
        scores = [result.get("score", 0) for result in results]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(subjects, scores, color=PRIMARY_COLOR)
        ax.set_xlabel("Scores")
        ax.set_title("Student Performance")

        canvas = FigureCanvasTkAgg(fig, master=self.parent.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
