from backend.session_manager import load_session
from gui.login_gui import LoginRegisterGUI
from gui.main_window import MainWindowApp

if __name__ == "__main__":

    session = load_session()
    if session:
        app = MainWindowApp()
    else:
        app = LoginRegisterGUI()

    app.mainloop()


