# UI/UX Configuration File

# Colors
PRIMARY_COLOR = "#003366"  # Dark blue
SECONDARY_COLOR = "#007BFF"  # Bright blue
ACCENT_COLOR = "#28A745"  # Green
BACKGROUND_COLOR = "#F5F5F5"  # Light gray
TEXT_COLOR = "#333333"  # Dark gray
BUTTON_COLOR = "#0056b3"  # Button blue
BUTTON_HOVER_COLOR = "#004494"  # Darker blue

# Fonts
TITLE_FONT = ("Arial", 16, "bold")
LABEL_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 12, "bold")
ENTRY_FONT = ("Arial", 12)

# Padding & Spacing
PADDING = 10
BUTTON_WIDTH = 20

# style btn 
def style_button(widget):
    widget.configure(bg=BUTTON_COLOR, fg="white", font=BUTTON_FONT, width=BUTTON_WIDTH, relief="raised")
    widget.bind("<Enter>", lambda e: widget.configure(bg=BUTTON_HOVER_COLOR))
    widget.bind("<Leave>", lambda e: widget.configure(bg=BUTTON_COLOR))
