"""
Notifications Module - Canvas Overlay Version
Shows pop-ups directly on the game canvas as overlays
No separate windows!
"""

import tkinter as tk
from PIL import Image, ImageTk
import os


def show_geese_popup_overlay(canvas, root, score, message="Perfect! 🎉", on_close=None):
    """
    Show a geese pop-up as an overlay on the canvas, perfectly centered.
    
    Args:
        canvas: The game canvas to draw on
        root: The root window
        score (int): Current score to display
        message (str): Message to show
        on_close (function): Callback when popup is closed
    """
    # Get canvas dimensions
    canvas.update_idletasks()
    canvas_width = canvas.winfo_width() if canvas.winfo_width() > 1 else 1200
    canvas_height = canvas.winfo_height() if canvas.winfo_height() > 1 else 900
    
    # Calculate centered popup dimensions
    popup_width = 500
    popup_height = 450
    popup_x1 = (canvas_width - popup_width) // 2
    popup_y1 = (canvas_height - popup_height) // 2
    popup_x2 = popup_x1 + popup_width
    popup_y2 = popup_y1 + popup_height
    center_x = canvas_width // 2
    
    # Create popup box - centered
    popup_box = canvas.create_rectangle(
        popup_x1, popup_y1, popup_x2, popup_y2,
        fill="#f5f0e8",
        outline="#2d5016",
        width=5,
        tags="popup"
    )
    
    # Try to load good image (correct answer)
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        good_path = os.path.join(script_dir, "..", "..", "artifacts", "progress", "good.png")
        good_img = Image.open(good_path)
        good_img = good_img.resize((180, 180), Image.Resampling.LANCZOS)
        good_photo = ImageTk.PhotoImage(good_img)
        
        # Store reference to prevent garbage collection
        if not hasattr(canvas, '_popup_images'):
            canvas._popup_images = []
        canvas._popup_images.append(good_photo)
        
        canvas.create_image(center_x, popup_y1 + 110, image=good_photo, tags="popup")
    except:
        # Fallback: Use emoji
        canvas.create_text(
            center_x, popup_y1 + 110,
            text="🪿✨",
            font=("Arial", 50),
            tags="popup"
        )
    
    # Message
    canvas.create_text(
        center_x, popup_y1 + 230,
        text=message,
        font=("Georgia", 20, "bold"),
        fill="#2d5016",
        width=popup_width - 40,
        tags="popup"
    )
    
    # Score
    canvas.create_text(
        center_x, popup_y1 + 290,
        text=f"+10 points!",
        font=("Georgia", 18, "bold"),
        fill="#4a7c8c",
        tags="popup"
    )
    
    canvas.create_text(
        center_x, popup_y1 + 320,
        text=f"Score: {score}",
        font=("Georgia", 16),
        fill="#4a7c8c",
        tags="popup"
    )
    
    # Continue button - centered
    btn_width = 160
    btn_height = 50
    btn_x1 = center_x - btn_width // 2
    btn_y1 = popup_y1 + 360
    btn_x2 = btn_x1 + btn_width
    btn_y2 = btn_y1 + btn_height
    
    btn_bg = canvas.create_rectangle(
        btn_x1, btn_y1, btn_x2, btn_y2,
        fill="#4a7c8c",
        outline="#3d2817",
        width=2,
        tags="popup"
    )
    
    btn_text = canvas.create_text(
        center_x, btn_y1 + btn_height // 2,
        text="Continue",
        font=("Georgia", 16, "bold"),
        fill="white",
        tags="popup"
    )
    
    def close_popup(event=None):
        canvas.delete("popup")
        if hasattr(canvas, '_popup_images'):
            canvas._popup_images.clear()
        root.unbind("<Return>")
        if on_close:
            on_close()
    
    # Make button clickable
    canvas.tag_bind(btn_bg, "<Button-1>", close_popup)
    canvas.tag_bind(btn_text, "<Button-1>", close_popup)
    
    # Also allow Enter key to close
    root.bind("<Return>", close_popup)


def show_librarian_angry_overlay(canvas, root, correct_order_text, on_close=None):
    """
    Show angry librarian pop-up as an overlay on the canvas, perfectly centered.
    
    Args:
        canvas: The game canvas to draw on
        root: The root window
        correct_order_text (str): The correct book order to display
        on_close (function): Callback when popup is closed
    """
    # Get canvas dimensions
    canvas.update_idletasks()
    canvas_width = canvas.winfo_width() if canvas.winfo_width() > 1 else 1200
    canvas_height = canvas.winfo_height() if canvas.winfo_height() > 1 else 900
    
    # Calculate centered popup dimensions (taller for book list)
    popup_width = 600
    popup_height = 600
    popup_x1 = (canvas_width - popup_width) // 2
    popup_y1 = (canvas_height - popup_height) // 2
    popup_x2 = popup_x1 + popup_width
    popup_y2 = popup_y1 + popup_height
    center_x = canvas_width // 2
    
    # Create popup box
    popup_box = canvas.create_rectangle(
        popup_x1, popup_y1, popup_x2, popup_y2,
        fill="#f5f0e8",
        outline="#8b0000",
        width=5,
        tags="popup"
    )
    
    # Try to load bad image (wrong answer)
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bad_path = os.path.join(script_dir, "..", "..", "artifacts", "progress", "bad.png")
        bad_img = Image.open(bad_path)
        bad_img = bad_img.resize((160, 160), Image.Resampling.LANCZOS)
        bad_photo = ImageTk.PhotoImage(bad_img)
        
        # Store reference
        if not hasattr(canvas, '_popup_images'):
            canvas._popup_images = []
        canvas._popup_images.append(bad_photo)
        
        canvas.create_image(center_x, popup_y1 + 100, image=bad_photo, tags="popup")
    except:
        # Fallback: Angry emoji
        canvas.create_text(
            center_x, popup_y1 + 100,
            text="😤📚",
            font=("Arial", 50),
            tags="popup"
        )
    
    # Angry message
    canvas.create_text(
        center_x, popup_y1 + 200,
        text="Not quite right!",
        font=("Georgia", 20, "bold"),
        fill="#8b0000",
        width=popup_width - 60,
        tags="popup"
    )
    
    # Subtitle
    canvas.create_text(
        center_x, popup_y1 + 240,
        text="Here's the correct order:",
        font=("Georgia", 14, "italic"),
        fill="#3d2817",
        tags="popup"
    )
    
    # Correct order box
    order_box = canvas.create_rectangle(
        popup_x1 + 40, popup_y1 + 270,
        popup_x2 - 40, popup_y1 + 470,
        fill="#ffffff",
        outline="#3d2817",
        width=2,
        tags="popup"
    )
    
    canvas.create_text(
        center_x, popup_y1 + 370,
        text=correct_order_text,
        font=("Georgia", 12),
        fill="#3d2817",
        width=popup_width - 100,
        tags="popup"
    )
    
    # Try Again button - centered
    btn_width = 160
    btn_height = 50
    btn_x1 = center_x - btn_width // 2
    btn_y1 = popup_y1 + 510
    btn_x2 = btn_x1 + btn_width
    btn_y2 = btn_y1 + btn_height
    
    btn_bg = canvas.create_rectangle(
        btn_x1, btn_y1, btn_x2, btn_y2,
        fill="#8b0000",
        outline="#3d2817",
        width=2,
        tags="popup"
    )
    
    btn_text = canvas.create_text(
        center_x, btn_y1 + btn_height // 2,
        text="Try Again",
        font=("Georgia", 16, "bold"),
        fill="white",
        tags="popup"
    )
    
    def close_popup(event=None):
        canvas.delete("popup")
        if hasattr(canvas, '_popup_images'):
            canvas._popup_images.clear()
        root.unbind("<Return>")
        if on_close:
            on_close()
    
    # Make button clickable
    canvas.tag_bind(btn_bg, "<Button-1>", close_popup)
    canvas.tag_bind(btn_text, "<Button-1>", close_popup)
    
    # Also allow Enter key to close
    root.bind("<Return>", close_popup)


def show_simple_message(message_type, title, message):
    """
    Fallback function for simple message boxes.
    
    Args:
        message_type (str): 'info' or 'warning'
        title (str): Title of message box
        message (str): Message to display
    """
    from tkinter import messagebox
    if message_type == "info":
        messagebox.showinfo(title, message)
    else:
        messagebox.showwarning(title, message)
