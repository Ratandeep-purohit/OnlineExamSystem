import tkinter as tk
from tkinter import messagebox
from gui.main_window import MainWindowApp
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from backend.auth import Auth
from backend.face_capture import capture_face, capture_face_for_registration
from backend.session_manager import load_session , save_session
from gui.ui_config import *

class LoginRegisterGUI(tk.Tk):
    face_image = None
    def __init__(self):
        super().__init__()
        self.title("Login & Register")
        self.geometry("400x500")
        self.current_frame = None
        
         # Check if user is already logged in
        session = load_session()
        if session:
            self.destroy()
            self.open_main_window()
        else:
            self.show_login()
    
    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)
        
        tk.Label(self.current_frame, text="Login", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)
        
        tk.Label(self.current_frame, text="Email:", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
        self.email_entry = tk.Entry(self.current_frame, font=ENTRY_FONT)
        self.email_entry.pack()
        
        tk.Label(self.current_frame, text="Password:", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
        self.password_entry = tk.Entry(self.current_frame, show="*", font=ENTRY_FONT)
        self.password_entry.pack()
        
        show_pass_btn = tk.Button(self.current_frame, text="Show Password", command=self.toggle_password, relief="flat")
        show_pass_btn.pack(pady=5)
        show_pass_btn.bind("<ButtonPress>", lambda e: self.password_entry.config(show=""))
        show_pass_btn.bind("<ButtonRelease>", lambda e: self.password_entry.config(show="*"))
        
        login_btn = tk.Button(self.current_frame, text="Login", command=self.login)
        style_button(login_btn)
        login_btn.pack(pady=10)
        
        face_login_btn = tk.Button(self.current_frame, text="Login with Face", command=self.face_login)
        style_button(face_login_btn)
        face_login_btn.pack()
        
        register_btn = tk.Button(self.current_frame, text="Go to Register", command=self.show_register)
        style_button(register_btn)
        register_btn.pack(pady=10)
    
    def show_register(self):
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)
        
        tk.Label(self.current_frame, text="Register", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=20)

        tk.Label(self.current_frame,text="First Name:", font=LABEL_FONT, bg=BACKGROUND_COLOR,fg=TEXT_COLOR).pack()
        self.reg_first_name_entry = tk.Entry(self.current_frame, font=ENTRY_FONT)
        self.reg_first_name_entry.pack()

        tk.Label(self.current_frame, text= "Last Name:", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
        self.reg_last_name_entry = tk.Entry(self.current_frame, font=ENTRY_FONT)
        self.reg_last_name_entry.pack()

        tk.Label(self.current_frame, text="Email:", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
        self.reg_email_entry = tk.Entry(self.current_frame, font=ENTRY_FONT)
        self.reg_email_entry.pack()
        
        tk.Label(self.current_frame, text="Password:", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
        self.reg_password_entry = tk.Entry(self.current_frame, show="*", font=ENTRY_FONT)
        self.reg_password_entry.pack()
        
        show_pass_btn = tk.Button(self.current_frame, text="Show Password", command=self.toggle_register_password, relief="flat")
        show_pass_btn.pack(pady=5)
        show_pass_btn.bind("<ButtonPress>", lambda e: self.reg_password_entry.config(show=""))
        show_pass_btn.bind("<ButtonRelease>", lambda e: self.reg_password_entry.config(show="*"))
        
        tk.Label(self.current_frame, text="Role:", font=LABEL_FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
        self.role_var = tk.StringVar(value="Student")
        tk.OptionMenu(self.current_frame, self.role_var, "Student", "Teacher", "Admin").pack()
        
        register_btn = tk.Button(self.current_frame, text="Register", command=self.register)
        style_button(register_btn)
        register_btn.pack(pady=10)
        
    
        
        login_btn = tk.Button(self.current_frame, text="Go to Login", command=self.show_login)
        style_button(login_btn)
        login_btn.pack(pady=10)
    
    def toggle_password(self):
        pass
    
    def toggle_register_password(self):
        pass
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = Auth.login(email, password)
        if user:
            user_id = user["_id"]
            role = user["role"]
            save_session(user_id,role)
            messagebox.showinfo("Login Success", f"Logged in as {role}")
            self.open_main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")
    
    def face_login(self):
        captured_face = capture_face()
        user = Auth.face_login(self.email_entry.get(),captured_face)
        if user:
            user_id = user["_id"]
            role = user["role"]
            save_session(user_id,role)
            messagebox.showinfo("Face Login Success", f"Logged in as {role}")
            if self.winfo_exists():  # ✅ Ensure the window still exists before withdrawing
                self.withdraw()
            
            self.open_main_window()
        else:
            messagebox.showerror("Face Login Failed", "Face not recognized")
    
    def register(self):
        first_name = self.reg_first_name_entry.get(),
        last_name = self.reg_last_name_entry.get(),
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        role = self.role_var.get()
        def register_with_face(face_image):
            success = Auth.register(first_name, last_name, email, password, face_image, role )
            if success:
                messagebox.showinfo("Registration Successful", "You can now log in")
                self.show_login()
            else:
                messagebox.showerror("Registration Failed", "User already exists or face not detected")
        capture_face_for_registration(register_with_face)
    
   


    def open_main_window(self):
        session_data = load_session()
       
        if not session_data:
            messagebox.showerror("Error", "No active session found. Please log in again.")
            self.deiconify()  # Show the login window if session fails
            return
        
        self.withdraw() # this will hide the login window 
        app = MainWindowApp()
        app.mainloop()
        self.destroy()

if __name__ == "__main__":
    app = LoginRegisterGUI()
    app.mainloop()
