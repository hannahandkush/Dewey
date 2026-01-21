"""
Background Handler Module
Handles loading and displaying the gameplay background image
Created from Hannah's gamebackground.py
"""

import os
from PIL import Image, ImageTk


class backgroundhandler:
    """Handles gameplay background image loading and display"""
    
    def __init__(self, canvas, canvas_width=1150, canvas_height=650):
        """
        Initialize the background handler.
        
        Args:
            canvas: The tkinter Canvas to draw on
            canvas_width: Width of the canvas
            canvas_height: Height of the canvas
        """
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.original_bg_image = None
        self.bg_photo = None
    
    def load_background(self):
        """
        Load the gameplay background image.
        Tries multiple possible filenames and locations.
        
        Returns:
            bool: True if image loaded successfully, False otherwise
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)  # Go up from Functions/ to game/
        grandparent_dir = os.path.dirname(parent_dir)  # Go up from game/ to GithubVersion/
        
        # Try different possible filenames
        possible_files = [
            "gameplay_background.png",
            "gameplay_background.jpg",
            "gameplaybackground.png",
            "gameplaybackground.jpg"
        ]
        
        bg_image_path = None
        for filename in possible_files:
            test_path = os.path.join(grandparent_dir, "artifacts", "gameplay", filename)
            print(f"[backgroundhandler] Trying: {test_path}")
            if os.path.exists(test_path):
                bg_image_path = test_path
                print(f"[backgroundhandler] ✅ Found image: {filename}")
                break
        
        if bg_image_path is None:
            print(f"[backgroundhandler] ❌ No background image found")
            return False
        
        try:
            self.original_bg_image = Image.open(bg_image_path)
            print("[backgroundhandler] ✅ Image loaded successfully!")
            return True
        except Exception as e:
            print(f"[backgroundhandler] ❌ Error loading image: {e}")
            return False
    
    def display_background(self, canvas_width=None, canvas_height=None):
        """
        Display the background image on the canvas, scaled to fit.
        
        Args:
            canvas_width: Override canvas width (optional)
            canvas_height: Override canvas height (optional)
        """
        if self.original_bg_image is None:
            print("[backgroundhandler] No image to display")
            return
        
        # Use provided dimensions or defaults
        width = canvas_width if canvas_width else self.canvas_width
        height = canvas_height if canvas_height else self.canvas_height
        
        # Make sure canvas has been rendered (not 1x1)
        if width <= 1 or height <= 1:
            width = self.canvas_width
            height = self.canvas_height
        
        try:
            # Resize image to canvas size
            resized_img = self.original_bg_image.resize((width, height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_img)
            
            # Remove old background if exists
            self.canvas.delete("background")
            
            # Draw new background
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor='nw', tags="background")
            
            # Make sure background is behind everything
            self.canvas.tag_lower("background")
            
            print("[backgroundhandler] ✅ Background displayed")
        except Exception as e:
            print(f"[backgroundhandler] ❌ Error displaying: {e}")
    
    def create_fallback_background(self):
        """Create a simple colored background as fallback"""
        self.canvas.create_rectangle(
            0, 0, self.canvas_width, self.canvas_height,
            fill="#f5f0e8", outline="", tags="background"
        )
        print("[backgroundhandler] Using fallback background")
    
    def on_resize(self, event):
        """
        Handle canvas resize event.
        Call this from canvas <Configure> event.
        
        Args:
            event: The tkinter event object
        """
        if self.original_bg_image is None:
            return
        
        new_width = event.width
        new_height = event.height
        
        self.display_background(new_width, new_height)
