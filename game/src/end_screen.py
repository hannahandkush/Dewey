import tkinter as tk
from PIL import Image, ImageTk
import os

def show_enhanced_end_screen(parent_window, score, max_score, genre, on_play_again, on_home, genre_progress=None, on_continue=None):
    # Load progress if not provided
    if genre_progress is None:
        try:
            from progress_tracker import load_progress
            genre_progress = load_progress()
        except:
            genre_progress = {
                'classic': {'completed': False, 'score': 0},
                'romance': {'completed': False, 'score': 0},
                'thriller': {'completed': False, 'score': 0}
            }
    
    # 1. Clear window completely
    for widget in parent_window.winfo_children():
        widget.destroy()
    
    # 2. Get window size - João's improvement: use update() instead of update_idletasks()
    parent_window.update()  # João's change: Forces full update
    w = parent_window.winfo_width()
    h = parent_window.winfo_height()
    
    # Fallback size - João's improvement: better threshold
    if w < 100:  # João's change: < 100 instead of <= 1
        w, h = 900, 675 

    canvas = tk.Canvas(parent_window, bg="#f5f0e8", width=w, height=h, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # 3. Choose background based on progress
    completed = {k: v.get('completed', False) for k, v in genre_progress.items()}
    
    if all(completed.values()): 
        bg_file = "library_all_clean"
    elif completed.get('classic') and completed.get('romance'): 
        bg_file = "library_classic_romance"
    elif completed.get('classic') and completed.get('thriller'): 
        bg_file = "library_classic_thriller"
    elif completed.get('romance') and completed.get('thriller'): 
        bg_file = "library_romance_thriller"
    elif completed.get('classic'): 
        bg_file = "library_classic_only"
    elif completed.get('romance'): 
        bg_file = "library_romance_only"
    elif completed.get('thriller'): 
        bg_file = "library_thriller_only"
    else: 
        bg_file = "library_all_messy"

    # 4. Build path to image
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try multiple possible paths
    possible_paths = []
    
    # Path 1: src/ -> game/ -> GithubVersion/ -> artifacts/finalscores/
    path1_base = os.path.join(script_dir, "..", "..", "artifacts", "finalscores")
    possible_paths.append(os.path.join(path1_base, bg_file + ".png"))
    possible_paths.append(os.path.join(path1_base, bg_file))
    
    # Path 2: Just in case structure is different
    path2_base = os.path.join(script_dir, "..", "artifacts", "finalscores")
    possible_paths.append(os.path.join(path2_base, bg_file + ".png"))
    possible_paths.append(os.path.join(path2_base, bg_file))
    
    print(f"\n[EndScreen] Looking for background: {bg_file}")
    
    img_path = None
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        print(f"[EndScreen] Trying: {abs_path}")
        if os.path.exists(abs_path):
            img_path = abs_path
            print(f"[EndScreen] ✅ FOUND: {abs_path}")
            break
    
    if img_path is None:
        print(f"[EndScreen] ❌ Image not found in any location!")

    # 5. Load and display image
    image_loaded = False
    try:
        if img_path and os.path.exists(img_path):
            pil_img = Image.open(img_path)
            pil_img = pil_img.resize((w, h), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(pil_img)
            canvas.create_image(0, 0, image=bg_photo, anchor='nw')
            canvas.image = bg_photo  # Keep reference
            image_loaded = True
            print(f"[EndScreen] ✅ Background displayed successfully!")
        else:
            print(f"[EndScreen] ⚠️ Using fallback - image not found")
    except Exception as e:
        print(f"[EndScreen] ❌ Error loading image: {e}")
    
    # Fallback: Nice beige background
    if not image_loaded:
        canvas.create_rectangle(0, 0, w, h, fill="#f5f0e8", outline="")
        canvas.create_text(w/2, 50, 
                          text="⚠️ Background images not found in artifacts/finalscores/", 
                          font=("Georgia", 12), fill="#8b0000")
        print(f"[EndScreen] Using fallback background color")

    # 6. João's improvement: Score info box on the right (80% width, 25% height)
    info_frame = tk.Frame(parent_window, bg="#f5f0e8", bd=3, relief="ridge", padx=20, pady=15)
    tk.Label(info_frame, text="Session Complete!", font=("Georgia", 20, "bold"), 
             bg="#f5f0e8", fg="#3d2817").pack()
    tk.Label(info_frame, text=f"Score: {score}/{max_score}", font=("Georgia", 18), 
             bg="#f5f0e8", fg="#3d2817").pack(pady=10)
    
    # Position at 80% width (right side) and 25% height
    canvas.create_window(w*0.80, h*0.25, window=info_frame, anchor="center")

    # 7. Buttons - João's changes: "Continue" instead of "Home", positioned at 88% height
    btn_style = {"font": ("Georgia", 12, "bold"), "padx": 20, "pady": 10, "fg": "#000000", "cursor": "hand2"}

    # Try Again button
    tk.Button(parent_window, text="Try Again", bg="#4a7c8c", command=on_play_again, **btn_style).place(x=w*0.3, y=h*0.88, anchor="center")

    # New Game button
    def handle_reset():
        try:
            from progress_tracker import reset_progress
            reset_progress()
        except:
            print("Could not reset progress")
        on_home()
    tk.Button(parent_window, text="New Game", bg="#8b0000", command=handle_reset, **btn_style).place(x=w*0.5, y=h*0.88, anchor="center")

    # Continue button - Goes to genre selection if available, otherwise home
    continue_callback = on_continue if on_continue else on_home
    tk.Button(parent_window, text="Continue", bg="#6b4423", command=continue_callback, **btn_style).place(x=w*0.7, y=h*0.88, anchor="center")
