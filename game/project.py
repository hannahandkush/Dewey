import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageTk
from library_game_logic import get_author_surname, get_author_first_name, check_book_position, load_books_by_genre, sort_books_by_surname, sort_books_by_first_name

# Import enhancement modules from src folder
from src.notifications import show_geese_popup_overlay, show_librarian_angry_overlay
from src.progress_tracker import load_progress, save_progress, mark_genre_complete, create_completion_badge
from src.end_screen import show_enhanced_end_screen
from src.reset_progress import confirm_reset, reset_all_progress, show_reset_success
from src.gamebackground import backgroundhandler
from src.bookspines import calculate_book_dimensions, create_book_spine_image
from src.drag_logic import DragManager


class LibraryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Dewey")
        self.root.geometry("1200x900")
        self.root.configure(bg="#f5f0e8")
        self.base_button_font_size = 32
        self.base_button_padx = 60
        self.base_button_pady = 25
        self.base_window_width = 1200
        self.base_window_height = 900
        self.current_screen = "title"
        self.story_index = 0
        self.selected_genre = None
        
        # Game state
        self.score = 0
        self.current_book_index = 0
        self.total_books = 5
        self.genre_progress = load_progress()
        self.sort_method = 'surname'  # Will be 'surname' or 'first_name'
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "..", "artifacts", "book_covers", "local_game_images.json")
        with open(json_path, "r") as f:
            full_book_data = json.load(f)
        
        self.book_cover_paths = {title: details["Local_Path"] for title, details in full_book_data.items()}
        self.show_title_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def reset_progress(self):
        """Reset all progress and start fresh."""
        # Ask for confirmation
        if confirm_reset():
            # Reset progress using the module
            self.genre_progress = reset_all_progress()
            # Show success message
            show_reset_success()
            # Refresh the title screen to update any UI
            self.show_title_screen()

# =====================================================================================================================
# -------- Title Page Section -----------------------------------------------------------------------------------------
# =====================================================================================================================
    
    def show_title_screen(self):
        self.clear_screen()
        self.current_screen = "title"

        self.canvas = tk.Canvas(self.root, bg="#f5f0e8", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Load the image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "..", "artifacts", "startgame.png")
        
        try:
            self.original_title_image = Image.open(image_path)
            self.title_screen_image = None # To be created on resize
            self.canvas.bind('<Configure>', self.on_resize_title_screen)
        except FileNotFoundError:
            pass
        
        self.start_btn = tk.Button(
            self.root, text="Start Game",
            font=("Georgia", 32, "bold"),
            bg="#4a7c8c", fg="#008080",
            padx=60, pady=25,
            command=self.show_story,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=5
        )
        self.start_btn_window = self.canvas.create_window(0, 0, window=self.start_btn, anchor='nw')
        
        # Add "Start Fresh" button
        self.reset_btn = tk.Button(
            self.root, text="Start Fresh",
            font=("Georgia", 16),
            bg="#8b0000", fg="#000000",
            padx=20, pady=10,
            command=self.reset_progress,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=3
        )
        self.reset_btn_window = self.canvas.create_window(0, 0, window=self.reset_btn, anchor='nw')

    def on_resize_title_screen(self, event):
        if not hasattr(self, 'original_title_image'):
            return
            
        new_width = event.width
        new_height = event.height
        
        # Resize image
        resized_img = self.original_title_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.title_screen_image = ImageTk.PhotoImage(resized_img)
        self.canvas.create_image(0, 0, image=self.title_screen_image, anchor='nw')
        
        # Scale and reposition button
        scale_factor_width = new_width / self.base_window_width
        scale_factor_height = new_height / self.base_window_height
        scale_factor = min(scale_factor_width, scale_factor_height)

        new_font_size = max(int(self.base_button_font_size * scale_factor), 10) # Minimum font size of 10
        new_padx = int(self.base_button_padx * scale_factor)
        new_pady = int(self.base_button_pady * scale_factor)
        
        self.start_btn.config(font=("Georgia", new_font_size, "bold"), padx=new_padx, pady=new_pady)

        btn_x = new_width * 0.15
        btn_y = new_height / 2
        self.canvas.coords(self.start_btn_window, btn_x, btn_y)
        
        # Position "Start Fresh" button (bottom left corner)
        reset_font_size = max(int(16 * scale_factor), 10)
        reset_padx = max(int(20 * scale_factor), 10)
        reset_pady = max(int(10 * scale_factor), 5)
        self.reset_btn.config(font=("Georgia", reset_font_size), padx=reset_padx, pady=reset_pady)
        
        reset_x = new_width * 0.15
        reset_y = new_height * 0.85
        self.canvas.coords(self.reset_btn_window, reset_x, reset_y)

# ====================================================================================================================
# -------- Storyline Section -----------------------------------------------------------------------------------------
# ====================================================================================================================

    def show_story(self):
        self.clear_screen()
        self.current_screen = "story"
        self.story_index = 0

        self.story_images = sorted([
            "artifacts/story/1goosedream.png",
            "artifacts/story/2angrylibrarian.png",
            "artifacts/story/3modeselect.png"
        ])
        
        self.story_canvas = tk.Canvas(self.root, bg="#f5f0e8", highlightthickness=0)
        self.story_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create Home button locally
        home_btn = tk.Button(
            self.root, text="Home",
            font=("Georgia", 12),
            bg="#4a7c8c", fg="#008080",
            padx=10, pady=5,
            command=self.show_title_screen,
            cursor="hand2"
        )
        home_btn.place(relx=1.0, rely=0, anchor='ne')

        # Create Back button locally
        if self.story_index > 0:
            back_btn = tk.Button(
                self.root, text="← Back",
                font=("Georgia", 12),
                bg="#4a7c8c", fg="#008080",
                padx=10, pady=5,
                command=self.previous_story,
                cursor="hand2"
            )
            back_btn.place(relx=0, rely=0, anchor='nw')

        self.story_canvas.bind('<Configure>', self.on_resize_story_screen)
        self.display_story_page()
    
    def on_resize_story_screen(self, event):
        if not hasattr(self, 'original_story_image'):
            return
            
        new_width = event.width
        new_height = event.height
        
        # Resize image
        resized_img = self.original_story_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.story_screen_image = ImageTk.PhotoImage(resized_img)
        self.story_canvas.create_image(0, 0, image=self.story_screen_image, anchor='nw')
        
        # Keep buttons on top
        self.story_canvas.tag_raise("button")
 
    def display_story_page(self):
        self.story_canvas.delete("all")
        
        if self.story_index < len(self.story_images):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "..", self.story_images[self.story_index])
            
            try:
                self.original_story_image = Image.open(image_path)
                # Trigger the resize event manually to draw the first image
                self.on_resize_story_screen(type('event', (object,), {'width': self.root.winfo_width(), 'height': self.root.winfo_height()}))
            except FileNotFoundError:
                # Handle missing image file
                self.story_canvas.create_text(self.root.winfo_width() / 2, self.root.winfo_height() / 2, text=f"Image not found:\n{image_path}", font=("Georgia", 18))

# ====================================================================================================================
# -------- Mode Selection -----------------------------------------------------------------------------------------
# ====================================================================================================================

            if self.story_index == 2:
                # Create genre selection buttons instead of Continue
                current_width = self.root.winfo_width()
                current_height = self.root.winfo_height()

                button_y = current_height - 100
                
                # Add completion checkmarks above buttons
                genres = ['classic', 'romance', 'thriller']
                positions = [0.25, 0.50, 0.75]
                
                for genre, position in zip(genres, positions):
                    is_completed = self.genre_progress.get(genre, {}).get('completed', False)
                    badge_x = int(current_width * position)
                    badge_y = button_y - 60  # Above the button
                    
                    if is_completed:
                        # Draw green checkmark
                        self.story_canvas.create_text(
                            badge_x, badge_y,
                            text="✓ COMPLETED",
                            font=("Georgia", 14, "bold"),
                            fill="#FFFFFF",
                            tags="completion"
                        )
                
                # Classic Button
                btn_classic = tk.Button(
                    self.root, text="Classic",
                    font=("Georgia", 20, "bold"),
                    bg="#4a7c8c", fg="#008080",
                    padx=40, pady=15,
                    command=lambda: self.start_game_with_genre('classic'),
                    cursor="hand2"
                )
                self.story_canvas.create_window(current_width * 0.25, button_y, window=btn_classic, tags="button")

                # Romance Button
                btn_romance = tk.Button(
                    self.root, text="Romance",
                    font=("Georgia", 20, "bold"),
                    bg="#4a7c8c", fg="#008080",
                    padx=40, pady=15,
                    command=lambda: self.start_game_with_genre('romance'),
                    cursor="hand2"
                )
                self.story_canvas.create_window(current_width * 0.50, button_y, window=btn_romance, tags="button")

                # Thriller Button
                btn_thriller = tk.Button(
                    self.root, text="Thriller",
                    font=("Georgia", 20, "bold"),
                    bg="#4a7c8c", fg="#008080",
                    padx=40, pady=15,
                    command=lambda: self.start_game_with_genre('thriller'),
                    cursor="hand2"
                )
                self.story_canvas.create_window(current_width * 0.75, button_y, window=btn_thriller, tags="button")

            else:
                continue_btn = tk.Button(
                    self.root,
                    text="Continue →",
                    font=("Georgia", 20, "bold"),
                    bg="#4a7c8c", fg="#008080",
                    padx=40, pady=15,
                    command=self.next_story,
                    cursor="hand2"
                )
                self.story_canvas.create_window(self.root.winfo_width() / 2, self.root.winfo_height() - 100, window=continue_btn, tags="button")

            if self.story_index > 0:
                back_btn = tk.Button(
                    self.root,
                    text="← Back",
                    font=("Georgia", 12), # Reduced font size
                    bg="#4a7c8c", fg="#008080",
                    padx=10, pady=5, # Reduced padding
                    command=self.previous_story,
                    cursor="hand2"
                )
                back_btn.place(relx=0, rely=0, anchor='nw') # Top-left corner
            else:
                # If on the first story page, ensure back button is not visible
                # This is already handled by creating it conditionally, but explicit place_forget could be used if it was persistent
                pass
    
    def next_story(self):
        self.story_index += 1
        self.display_story_page()
    
    def previous_story(self):
        self.story_index -= 1
        self.display_story_page()
    
# ====================================================================================================================
# -------- Gameplay Section -----------------------------------------------------------------------------------------
# ====================================================================================================================

    def start_game_with_genre(self, genre):
        self.selected_genre = genre
        
        self.books_pool = load_books_by_genre(genre).copy()
        random.shuffle(self.books_pool)
        
        self.books_to_place = self.books_pool[:self.total_books]
        remaining = self.books_pool[self.total_books:]
        shelf_books_unsorted = random.sample(remaining, min(4, len(remaining)))
        
        self.shelf_books = sort_books_by_surname(shelf_books_unsorted)
        
        self.current_book_index = 0
        self.score = 0       
    
        self.show_game_screen()
    
    def show_game_screen(self):
        self.clear_screen()
        self.current_screen = "game"
        self.setup_game_ui()
        self.drag_manager = DragManager(self)
        self.draw_game()
        # Create Home button locally
        home_btn = tk.Button(
            self.root, text="Home",
            font=("Georgia", 12),
            bg="#4a7c8c", fg="#008080",
            padx=10, pady=5,
            command=self.show_title_screen,
            cursor="hand2"
        )
        home_btn.place(relx=1.0, rely=0, anchor='ne')
    
    def setup_game_ui(self):
        header_frame = tk.Frame(self.root, bg="#e8d5b7", height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📚🪿📖 Dewey 📖🪿📚",
                font=("Georgia", 28, "bold"), bg="#e8d5b7", fg="#3d2817").pack(pady=10)
        
        info_frame = tk.Frame(header_frame, bg="#e8d5b7")
        info_frame.pack()
        
        self.score_label = tk.Label(info_frame, text=f"Score: {self.score}",
                                    font=("Georgia", 18), bg="#e8d5b7", fg="#4a3728")
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        self.progress_label = tk.Label(info_frame, text=f"Book: {self.current_book_index + 1}/{self.total_books}",
                                      font=("Georgia", 18), bg="#e8d5b7", fg="#4a3728")
        self.progress_label.pack(side=tk.LEFT, padx=20)
        
        self.instruction_label = tk.Label(self.root, text="", font=("Georgia", 14),
                                         bg="#f5f0e8", fg="#3d2817", wraplength=1100)
        self.instruction_label.pack(pady=10)
        
        self.main_canvas = tk.Canvas(self.root, width=1150, height=650, highlightthickness=0)
        self.main_canvas.pack(pady=5)
        
        self.book_labels = []
        self.slot_areas = []
        self.hovered_slot = None
        self.selected_slot = None
        self.book_images = []
        self.shelf_y = 530  # Updated shelf height for background image
        
        # Initialize background handler (Hannah's module)
        self.bg_handler = backgroundhandler(self.main_canvas, 1150, 650)
        if self.bg_handler.load_background():
            self.bg_handler.display_background()
            self.main_canvas.bind('<Configure>', lambda e: self.bg_handler.on_resize(e))
        else:
            self.bg_handler.create_fallback_background()
    
    def draw_game(self):
        # Redisplay background (Hannah's module)
        if hasattr(self, 'bg_handler') and self.bg_handler.original_bg_image:
            self.bg_handler.display_background()
        self.update_instructions()
        self.draw_shelf()
        self.draw_bookshelf()
        self.draw_book_to_place()
    
    def update_instructions(self):
        if self.current_book_index < len(self.books_to_place):
            current_book = self.books_to_place[self.current_book_index]
            # Unpack the 3-element tuple (no rank anymore)
            title, author, color = current_book 
            
            self.instruction_label.config(
                text=f"Drag '{title}' by {author} from the trolley to the correct spot!\n(Books are sorted alphabetically by author's surname)"
            )
            self.progress_label.config(text=f"Book: {self.current_book_index + 1}/{self.total_books}")
    
    def draw_shelf(self):
        canvas_width = 1150
        self.main_canvas.create_line(0, self.shelf_y, canvas_width, self.shelf_y,
                                     fill="#8B4513", width=14, tags="shelf")
        self.main_canvas.create_line(0, self.shelf_y + 14, canvas_width, self.shelf_y + 14,
                                     fill="#654321", width=5, tags="shelf")
    
    def draw_book_to_place(self):
        if self.current_book_index >= len(self.books_to_place):
            return

        book_width = 268
        book_height = 402
        x = 872
        y = (650 - book_height) // 2

        # Unpack the 3-element tuple (no rank)
        title, author, color = self.books_to_place[self.current_book_index] 
        
        image_path = self.book_cover_paths.get(title)
        
        if image_path:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            full_image_path = os.path.join(script_dir, "..", "artifacts", "book_covers", image_path)
            try:
                img = Image.open(full_image_path)
                img = img.resize((book_width, book_height), Image.Resampling.LANCZOS)
                book_img = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                book_img = self.create_pretty_book_cover(book_width, book_height, title, author, color)
        else:
            book_img = self.create_pretty_book_cover(book_width, book_height, title, author, color)

        self.book_images.append(book_img)
        self.main_canvas.create_image(x, y, image=book_img, anchor='nw', tags="draggable")
        
        self.main_canvas.tag_bind("draggable", "<Button-1>", self.drag_manager.start_drag)
        self.main_canvas.tag_bind("draggable", "<B1-Motion>", self.drag_manager.on_drag)
        self.main_canvas.tag_bind("draggable", "<ButtonRelease-1>", self.drag_manager.end_drag)
        self.main_canvas.tag_bind("draggable", "<Enter>", lambda e: self.main_canvas.config(cursor="hand2"))
        self.main_canvas.tag_bind("draggable", "<Leave>", lambda e: self.main_canvas.config(cursor=""))
        
        self.drag_book_info = {'width': book_width, 'height': book_height, 'x': x, 'y': y}
    
    def create_pretty_book_cover(self, width, height, title, author, base_color):
        img = Image.new('RGB', (width, height), base_color)
        draw = ImageDraw.Draw(img)
        
        draw.rectangle([0, 0, width-1, height-1], outline='#2c1810', width=3)
        draw.rectangle([5, 5, width-6, height-6], outline='white', width=2)
        
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 11)
            author_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 8)
        except:
            title_font = ImageFont.load_default()
            author_font = ImageFont.load_default()
        
        title_words = title.split()
        if len(title) > 15:
            mid = len(title_words) // 2
            title_line1 = " ".join(title_words[:mid])
            title_line2 = " ".join(title_words[mid:])
            draw.text((width//2, height//3), title_line1, fill='white', font=title_font, anchor='mm')
            draw.text((width//2, height//3 + 12), title_line2, fill='white', font=title_font, anchor='mm')
        else:
            draw.text((width//2, height//3), title, fill='white', font=title_font, anchor='mm')
        
        draw.text((width//2, height - 15), author, fill='white', font=author_font, anchor='mm')
        
        return ImageTk.PhotoImage(img)
    
    def draw_bookshelf(self):
        canvas_width = 1150
        spacing = 10
        book_widths = [random.randint(60, 90) for _ in self.shelf_books]
        total_width = sum(book_widths) + (len(self.shelf_books) - 1) * spacing
        start_x = (canvas_width - total_width) // 2
        
        current_x = start_x
        for i in range(len(self.shelf_books) + 1):
            if i == 0:
                x, width = start_x - 50, 50
            elif i == len(self.shelf_books):
                x, width = current_x, 300
            else:
                x, width = current_x - 35, 70
            
            slot = self.main_canvas.create_rectangle(x, 50, x + width, self.shelf_y,
                                                     fill="", outline="", tags=f"slot_{i}")
            self.slot_areas.append((i, slot, x + width // 2))
            
            if i < len(self.shelf_books):
                current_x += book_widths[i] + spacing
        
        current_x = start_x
        for i, (title, author, color) in enumerate(self.shelf_books):
            book_width = book_widths[i]
            book_height, font_size = self.calculate_book_dimensions(title, author, book_width)
            y = self.shelf_y - book_height
            
            self.book_labels.append({
                'index': i, 'original_x': current_x, 'current_x': current_x,
                'y': y, 'width': book_width, 'height': book_height,
                'title': title, 'author': author, 'color': color, 'font_size': font_size
            })
            
            self.draw_book_spine(i, current_x, y, book_width, book_height, color, title, author, font_size)
            current_x += book_width + spacing
    
    def calculate_book_dimensions(self, title, author, width):
        return calculate_book_dimensions(title, author, width)

    def draw_book_spine(self, index, x, y, width, height, color, title, author, font_size):
        book_img = self.create_book_spine_image(width, height, color, title, author, font_size)
        self.book_images.append(book_img)
        self.main_canvas.create_image(x, y, image=book_img, anchor='nw', tags=f"book_{index}")
    
    def create_book_spine_image(self, width, height, color, title, author, font_size):
        return create_book_spine_image(width, height, color, title, author, font_size)

# ------------------- score decision and actions -----------------------------------------------
    
    def check_answer(self):
        if self.selected_slot is None:
            return
        
        current_book = self.books_to_place[self.current_book_index]
        correct_position = check_book_position(current_book, self.shelf_books, sort_by=self.sort_method)
        
        if self.selected_slot == correct_position:
            self.score += 10
            self.shelf_books.insert(correct_position, current_book)
            # Show overlay on the game canvas
            show_geese_popup_overlay(self.main_canvas, self.root, self.score, 
                                    "Perfect! You sorted it correctly! 🪿",
                                    on_close=self.continue_after_popup)

        else:
            temp_list = self.shelf_books + [current_book]
            sorted_temp = sort_books_by_surname(temp_list)
            
            book_list = "\n".join([f"{t} by {a}" for t, a, _ in sorted_temp])
            # Show overlay on the game canvas
            show_librarian_angry_overlay(self.main_canvas, self.root, book_list,
                                        on_close=lambda: self.continue_after_popup_wrong(correct_position, current_book))
    
    def continue_after_popup(self):
        """Continue game after correct answer popup closes."""
        self.score_label.config(text=f"Score: {self.score}")
        self.current_book_index += 1
        
        if self.current_book_index >= self.total_books:
            self.end_game()
        else:
            self.next_book()
    
    def continue_after_popup_wrong(self, correct_position, current_book):
        """Continue game after wrong answer popup closes."""
        self.shelf_books.insert(correct_position, current_book)
        self.score_label.config(text=f"Score: {self.score}")
        self.current_book_index += 1
        
        if self.current_book_index >= self.total_books:
            self.end_game()
        else:
            self.next_book()
    
    def next_book(self):
        self.main_canvas.delete("all")
        self.book_images = []
        self.book_labels = []
        self.slot_areas = []
        self.hovered_slot = None
        self.selected_slot = None
        self.draw_game()

# ====================================================================================================================
# -------- Endgame Section -----------------------------------------------------------------------------------------
# ====================================================================================================================

    def end_game(self):
        self.clear_screen()
        self.current_screen = "end_game"
        
        # Mark genre as complete and save progress
        max_score = self.total_books * 10
        self.genre_progress = mark_genre_complete(
            self.genre_progress, 
            self.selected_genre, 
            self.score
        )
        
        # Show enhanced end screen
        show_enhanced_end_screen(
            self.root,
            self.score,
            max_score,
            self.selected_genre,
            on_play_again=lambda: self.start_game_with_genre(self.selected_genre),
            on_home=self.show_title_screen,
            on_continue=self.show_story  # Continue goes to genre selection
        )

def main():
    """Main function to run the game."""
    root = tk.Tk()
    game = LibraryGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    