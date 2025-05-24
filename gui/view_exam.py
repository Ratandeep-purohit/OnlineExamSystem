import tkinter as tk
from tkinter import messagebox, ttk
from backend.db_manager import fetch_exams
from gui.ui_config import PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR, TITLE_FONT, LABEL_FONT, BUTTON_FONT, BUTTON_HOVER_COLOR, PADDING

class ViewExam(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BACKGROUND_COLOR)
        self.parent = parent
        self.create_exam_list()
    
    def create_exam_list(self):
        if hasattr(self.parent, 'content_frame'):
            self.parent.content_frame.destroy()
        self.parent.content_frame = tk.Frame(self.parent, bg=BACKGROUND_COLOR)
        self.parent.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)
        
        tk.Label(self.parent.content_frame, text="View Exams", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)
        
        filter_frame = tk.Frame(self.parent.content_frame, bg=BACKGROUND_COLOR)
        filter_frame.pack(pady=10)
        
        tk.Label(filter_frame, text="Search:", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=5)
        self.search_entry = tk.Entry(filter_frame, font=LABEL_FONT)
        self.search_entry.grid(row=0, column=1, padx=5)
        
        tk.Button(filter_frame, text="Search", font=BUTTON_FONT, bg=PRIMARY_COLOR, fg="white", command=self.search_exams).grid(row=0, column=2, padx=5)
        
        self.exam_tree = ttk.Treeview(self.parent.content_frame, columns=("ID", "Title", "Subject", "Duration"), show="headings")
        self.exam_tree.heading("ID", text="ID")
        self.exam_tree.heading("Title", text="Title")
        self.exam_tree.heading("Subject", text="Subject")
        self.exam_tree.heading("Duration", text="Duration")
        self.exam_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.load_exams()
    
    def load_exams(self, filter_text=""):
        for item in self.exam_tree.get_children():
            self.exam_tree.delete(item)
        
        exams = fetch_exams()
        if not exams:
            messagebox.showinfo("No Exams", "No exams available.")
            return
        
        for exam in exams:
            if filter_text.lower() in exam["title"].lower() or filter_text.lower() in exam["subject"].lower():
                self.exam_tree.insert("", tk.END, values=(exam["_id"], exam["title"], exam["subject"], exam["duration"]))
    
    def search_exams(self):
        filter_text = self.search_entry.get()
        self.load_exams(filter_text)
