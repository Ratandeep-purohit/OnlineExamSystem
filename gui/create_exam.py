import tkinter as tk
from tkinter import messagebox, Scrollbar
from gui.ui_config import PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR, TITLE_FONT, LABEL_FONT, BUTTON_FONT, BUTTON_HOVER_COLOR, PADDING
from backend.db_manager import create_exam
from datetime import datetime

class CreateExam(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.parent = parent
        self.questions_data = []
        self.create_exam_form()
    
    def create_exam_form(self):
        if hasattr(self.parent, 'content_frame') and self.parent.content_frame is not None:
            self.parent.content_frame.destroy()
        
        self.canvas = tk.Canvas(self, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = tk.Frame(self.canvas, bg=BACKGROUND_COLOR)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.parent.content_frame = tk.Frame(self.scrollable_frame, bg=BACKGROUND_COLOR)
        self.parent.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)

        tk.Label(self.parent.content_frame, text="Create Exam", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)
        
        form_frame = tk.Frame(self.parent.content_frame, bg=BACKGROUND_COLOR)
        form_frame.pack(pady=10, padx=20, anchor="center")
        
        tk.Label(form_frame, text="Exam Title:", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, sticky="w", pady=5)
        self.exam_title_entry = tk.Entry(form_frame, font=LABEL_FONT, width=40)
        self.exam_title_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(form_frame, text="Subject:", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, sticky="w", pady=5)
        self.subject_entry = tk.Entry(form_frame, font=LABEL_FONT, width=40)
        self.subject_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(form_frame, text="Duration (mins):", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, sticky="w", pady=5)
        self.duration_entry = tk.Entry(form_frame, font=LABEL_FONT, width=10)
        self.duration_entry.grid(row=2, column=1, pady=5, sticky="w")
        
        self.add_question_widgets()
        
        add_question = tk.Button(self.parent.content_frame, text="Add Another Question", font=BUTTON_FONT, bg=PRIMARY_COLOR, fg="white", command=self.add_question_widgets)
        add_question.pack(pady=10)
        add_question.bind("<Enter>", lambda e: add_question.config(bg=BUTTON_HOVER_COLOR))
        add_question.bind("<Leave>", lambda e: add_question.config(bg=PRIMARY_COLOR))
        
        submit_btn = tk.Button(self.parent.content_frame, text="Create Exam", font=BUTTON_FONT, bg=PRIMARY_COLOR, fg="white", command=self.submit_exam)
        submit_btn.pack(pady=5)
        submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg=BUTTON_HOVER_COLOR))
        submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg=PRIMARY_COLOR))
        
        # Fixed: Pack frame to display
        self.pack(fill=tk.BOTH, expand=True)
    
    def add_question_widgets(self):
        question_frame = tk.Frame(self.parent.content_frame, bd=2, relief="groove", bg="#f5f5f5")
        question_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(question_frame, text="Question:", bg="#f5f5f5").grid(row=0, column=0, sticky="w", pady=5)
        question_entry = tk.Text(question_frame, height=3, width=50)
        question_entry.grid(row=0, column=1, pady=5)
        
        options = []
        for i in range(4):
            tk.Label(question_frame, text=f"Option {chr(65+i)}:", bg="#f5f5f5").grid(row=i+1, column=0, sticky="w", pady=2)
            option_entry = tk.Entry(question_frame, width=50)
            option_entry.grid(row=i+1, column=1, pady=2)
            options.append(option_entry)
        
        tk.Label(question_frame, text="Correct Answer (A/B/C/D):", bg="#f5f5f5").grid(row=5, column=0, sticky="w", pady=5)
        correct_answer_entry = tk.Entry(question_frame, width=5)
        correct_answer_entry.grid(row=5, column=1, pady=5, sticky="w")
        
        self.questions_data.append({
            "question": question_entry,
            "options": options,
            "correct_answer": correct_answer_entry
        })
    
    def submit_exam(self):
        title = self.exam_title_entry.get()
        subject = self.subject_entry.get()
        duration = self.duration_entry.get()

        questions_list = []
        for data in self.questions_data:
            question_text = data["question"].get("1.0", tk.END).strip()
            options_text = [opt.get().strip() for opt in data["options"]]
            correct_answer = data["correct_answer"].get().strip().upper()
            
            if not question_text or not all(options_text) or correct_answer not in ["A", "B", "C", "D"]:
                messagebox.showerror("Error", "Please fill all fields correctly!")
                return
            
            questions_list.append({
                "question": question_text,
                "options": options_text,
                "right_answer": correct_answer
            })
        
        if not title or not subject or not duration.isdigit():
            messagebox.showerror("Error", "All fields are required and duration must be a number!")
            return
        data = {
            "title": title,
            "subject": subject,
            "duration": int(duration),
            "questions": questions_list,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        success = create_exam(data)
        if success:
            messagebox.showinfo("Success", "Exam Created Successfully!")
            self.parent.show_dashboard()
        else:
            messagebox.showerror("Error", "Failed to create exam!")
