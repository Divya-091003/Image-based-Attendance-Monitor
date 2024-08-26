import tkinter as tk
from tkinter import messagebox

def get_button(parent, text, color, command, fg="white"):
    """
    Creates a button with the given properties.

    Parameters:
    parent: The parent tkinter widget.
    text: The text to display on the button.
    color: The background color of the button.
    command: The function to call when the button is pressed.
    fg: The foreground color of the button text (default is white).

    Returns:
    A tkinter Button widget.
    """
    button = tk.Button(parent, text=text, bg=color, fg=fg, command=command, font=("Helvetica", 12))
    return button

def get_img_label(parent):
    """
    Creates a label intended for displaying images.

    Parameters:
    parent: The parent tkinter widget.

    Returns:
    A tkinter Label widget.
    """
    label = tk.Label(parent)
    return label

def msg_box(title, message):
    """
    Displays a message box with the given title and message.

    Parameters:
    title: The title of the message box.
    message: The message to display in the message box.
    """
    messagebox.showinfo(title, message)