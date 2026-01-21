"""
Reset Progress Module
Handles resetting all game progress and starting fresh
"""

import os
import json
from tkinter import messagebox


def reset_all_progress():
    """
    Reset all progress to default state.
    Deletes the game_progress.json file and returns default progress.
    
    Returns:
        dict: Default progress with all genres incomplete
    """
    default_progress = {
        'classic': {'completed': False, 'score': 0},
        'romance': {'completed': False, 'score': 0},
        'thriller': {'completed': False, 'score': 0}
    }
    
    try:
        # Get the path to game_progress.json
        script_dir = os.path.dirname(os.path.abspath(__file__))
        progress_path = os.path.join(script_dir, "..", "..", "game_progress.json")
        
        # Delete the file if it exists
        if os.path.exists(progress_path):
            os.remove(progress_path)
            print("Progress file deleted successfully")
        
        # Create new empty progress file
        with open(progress_path, "w") as f:
            json.dump(default_progress, f, indent=4)
            print("New progress file created")
            
    except Exception as e:
        print(f"Error resetting progress: {e}")
    
    return default_progress


def confirm_reset():
    """
    Show confirmation dialog before resetting progress.
    
    Returns:
        bool: True if user confirmed, False otherwise
    """
    confirm = messagebox.askyesno(
        "Start Fresh?",
        "This will delete all your progress and completed genres.\n\nAre you sure you want to start fresh?",
        icon='warning'
    )
    
    return confirm


def show_reset_success():
    """
    Show success message after reset.
    """
    messagebox.showinfo(
        "Progress Reset",
        "All progress has been cleared!\nYou can now start fresh! 🎉",
        icon='info'
    )
