"""
Progress Tracker Module
Handles saving and loading progress for genre completion
Shows visual indicators when genres are completed
"""

import json
import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk


def load_progress():
    """
    Load saved progress from file.
    
    Returns:
        dict: Dictionary with genre completion status and scores
    """
    default_progress = {
        'classic': {'completed': False, 'score': 0},
        'romance': {'completed': False, 'score': 0},
        'thriller': {'completed': False, 'score': 0}
    }
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        progress_path = os.path.join(script_dir, "..", "..", "game_progress.json")
        
        if os.path.exists(progress_path):
            with open(progress_path, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Could not load progress: {e}")
    
    return default_progress


def save_progress(genre_progress):
    """
    Save current progress to file.
    
    Args:
        genre_progress (dict): Dictionary with genre completion status
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        progress_path = os.path.join(script_dir, "..", "..", "game_progress.json")
        
        with open(progress_path, "w") as f:
            json.dump(genre_progress, f, indent=2)
    except Exception as e:
        print(f"Could not save progress: {e}")


def mark_genre_complete(genre_progress, genre, score):
    """
    Mark a genre as completed and save progress.
    
    Args:
        genre_progress (dict): Current progress dictionary
        genre (str): Genre that was completed
        score (int): Score achieved
    
    Returns:
        dict: Updated progress dictionary
    """
    if genre in genre_progress:
        genre_progress[genre]['completed'] = True
        genre_progress[genre]['score'] = max(genre_progress[genre]['score'], score)
    
    save_progress(genre_progress)
    return genre_progress

# --- NOVA FUNÇÃO QUE ESTAVA A FALTAR ---
def reset_progress():
    """
    Apaga o progresso atual e redefine para o estado inicial no ficheiro JSON.
    """
    default_progress = {
        'classic': {'completed': False, 'score': 0},
        'romance': {'completed': False, 'score': 0},
        'thriller': {'completed': False, 'score': 0}
    }
    save_progress(default_progress)
    return default_progress
# ---------------------------------------

def create_completion_badge(canvas, x, y, genre, is_completed):
    """
    Create a visual badge showing if genre is completed.
    """
    colors = {
        'classic': "#daa520",
        'romance': "#ff69b4", 
        'thriller': "#8b0000"
    }
    
    color = colors.get(genre, "#cccccc")
    
    badge = canvas.create_oval(
        x - 15, y - 15,
        x + 15, y + 15,
        fill=color if is_completed else "#cccccc",
        outline="#3d2817",
        width=2
    )
    
    if is_completed:
        canvas.create_text(
            x, y,
            text="✓",
            font=("Arial", 20, "bold"),
            fill="white"
        )
    
    return badge


def show_progress_summary(parent_window, genre_progress):
    """
    Show a summary popup of all genre progress.
    """
    popup = tk.Toplevel(parent_window)
    popup.title("Your Progress")
    popup.geometry("400x350")
    popup.configure(bg="#f5f0e8")
    
    title = tk.Label(
        popup,
        text="📚 Genre Progress 📚",
        font=("Georgia", 24, "bold"),
        bg="#f5f0e8",
        fg="#3d2817"
    )
    title.pack(pady=20)
    
    for genre in ['classic', 'romance', 'thriller']:
        frame = tk.Frame(popup, bg="#f5f0e8")
        frame.pack(pady=10, fill=tk.X, padx=40)
        
        completed = genre_progress.get(genre, {}).get('completed', False)
        score = genre_progress.get(genre, {}).get('score', 0)
        
        genre_label = tk.Label(
            frame,
            text=genre.capitalize(),
            font=("Georgia", 16, "bold"),
            bg="#f5f0e8",
            fg="#3d2817",
            width=10,
            anchor='w'
        )
        genre_label.pack(side=tk.LEFT, padx=10)
        
        if completed:
            status_text = f"✓ Complete! (Score: {score})"
            status_color = "#2d5016"
        else:
            status_text = "Not completed"
            status_color = "#8b0000"
        
        status_label = tk.Label(
            frame,
            text=status_text,
            font=("Georgia", 12),
            bg="#f5f0e8",
            fg=status_color
        )
        status_label.pack(side=tk.LEFT, padx=10)
    
    close_btn = tk.Button(
        popup,
        text="Close",
        font=("Georgia", 14, "bold"),
        bg="#4a7c8c",
        fg="white",
        padx=30,
        pady=10,
        command=popup.destroy,
        cursor="hand2"
    )
    close_btn.pack(pady=30)
    
    popup.transient(parent_window)
    popup.grab_set()


def get_total_completion_percentage(genre_progress):
    """
    Calculate overall completion percentage.
    """
    total_genres = 3
    completed = sum(1 for g in genre_progress.values() if g.get('completed', False))
    return (completed / total_genres) * 100