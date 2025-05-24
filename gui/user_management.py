import tkinter as tk
from tkinter import messagebox, ttk
from backend.db_manager import fetch_all_users, add_user, edit_user, delete_user
from gui.ui_config import *

class UserManagement(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg = BACKGROUND_COLOR)
        self.parent = parent
        self.create_user_management()
    
    def create_user_management(self):
        # Check if user management already exists
        if hasattr(self.parent, "user_management_frame"):
            self.parent.user_management_frame.destroy()

        tk.Label(self.parent, text="User Management", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)
        
        self.user_tree = ttk.Treeview(self.parent, columns=("ID", "Name", "Role", "Email"), show="headings")
        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Name", text="Name")
        self.user_tree.heading("Role", text="Role")
        self.user_tree.heading("Email", text="Email")
        self.user_tree.pack(fill=tk.BOTH, expand=True, pady=10, padx=PADDING)
        
        self.create_crud_buttons()
        self.load_users()
        
    def create_crud_buttons(self):
        crud_frame = tk.Frame(self.parent, bg=BACKGROUND_COLOR)
        crud_frame.pack(fill=tk.X, pady=10, anchor="center")
        
        button_frame = tk.Frame(crud_frame, bg=BACKGROUND_COLOR)
        button_frame.pack(anchor="center")
        
        self.add_button = tk.Button(button_frame, text="Add", command=self.add_user)
        style_button(self.add_button)
        self.add_button.pack(side=tk.LEFT, padx=10)
        
        self.edit_button = tk.Button(button_frame, text="Edit", command=self.edit_user)
        style_button(self.edit_button)
        self.edit_button.pack(side=tk.LEFT, padx=10)
        
        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_user)
        style_button(self.delete_button)
        self.delete_button.pack(side=tk.LEFT, padx=10)

    def load_users(self):
        users = fetch_all_users()
        if not users:
            messagebox.showinfo("No Users", "No users found.")
            return
        
        for user in users:
            self.user_tree.insert("", tk.END, values=(user["_id"], user.get("first_name", "N/A"), user["role"], user["email"]))   

    def add_user(self):
        self.user_form_window("Add User", self.save_new_user)

    def save_new_user(self, user_details):
        add_user(user_details)
        self.load_users()

    def edit_user(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to edit.")
            return
        
        user_id = self.user_tree.item(selected_item, "values")[0]
        user_details = self.user_tree.item(selected_item, "values")
        self.user_form_window("Edit User", lambda details: self.save_edited_user(user_id, details), user_details)

    def save_edited_user(self, user_id, user_details):
        edit_user(user_id, user_details)
        self.load_users()

    def delete_user(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to delete.")
            return
        
        user_id = self.user_tree.item(selected_item, "values")[0]
        delete_user(user_id)
        self.load_users()

    def user_form_window(self, title, save_callback, user_details=None):
        form_window = tk.Toplevel(self.parent)
        form_window.title(title)
        
        tk.Label(form_window, text="Name:", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(form_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(form_window, text="Role:", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=10)
        role_entry = tk.Entry(form_window)
        role_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(form_window, text="Email:", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, padx=10, pady=10)
        email_entry = tk.Entry(form_window)
        email_entry.grid(row=2, column=1, padx=10, pady=10)
        
        if user_details:
            name_entry.insert(0, user_details[1])
            role_entry.insert(0, user_details[2])
            email_entry.insert(0, user_details[3])
        
        save_button = tk.Button(form_window, text="Save", command=lambda: save_callback({
            "first_name": name_entry.get(),
            "role": role_entry.get(),
            "email": email_entry.get()
        }))
        style_button(save_button)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)
