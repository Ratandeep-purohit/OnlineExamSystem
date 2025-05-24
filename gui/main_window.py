import tkinter as tk
from tkinter import messagebox
from backend.session_manager import load_session , logout
from gui.ui_config import *
from gui.dashboard_gui import DashboardGUI

class MainWindowApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Examination System")
        self.geometry("900x600")
        self.configure(bg=BACKGROUND_COLOR)
        
        self.create_menu_bar()
        self.show_dashboard()
    
    def create_menu_bar(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        user_menu = tk.Menu(menu_bar, tearoff=0)
        user_menu.add_command(label="Profile")
        user_menu.add_separator()
        user_menu.add_command(label="Logout", command=self.logout)
        menu_bar.add_cascade(label="User", menu=user_menu)
    
    
    
    def show_dashboard(self):
        if hasattr(self, 'content_frame'):
            self.content_frame.destroy()
        self.content_frame = DashboardGUI(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)
        

    
    def logout(self):
        logout()
        self.destroy()

if __name__ == "__main__":
    app = MainWindowApp()
    app.mainloop()

