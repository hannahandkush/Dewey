import tkinter as tk
from tkinter import messagebox
import random
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageTk
from library_game_logic import get_author_surname, check_book_position, load_books_by_genre, sort_books_by_rank


class LibraryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Dewey's Library Sorting Game")
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
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "..", "artifacts", "book_covers", "local_game_images.json")
        with open(json_path, "r") as f:
            full_book_data = json.load(f)
        
        self.book_cover_paths = {title: details["Local_Path"] for title, details in full_book_data.items()}
        
        self.show_title_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # -------- Title Page Section --------------------------------------------------------------------------------------------------------------
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
        
    # -------- Storyline Section ---------------------------------------------------------------------------------------------------------------
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

            if self.story_index == 2:
                # Create genre selection buttons instead of Continue
                current_width = self.root.winfo_width()
                current_height = self.root.winfo_height()

                button_y = current_height - 100
                
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
    

    
    # -------- Gameplay Section ----------------------------------------------------------------------------------------------------------------
    def start_game_with_genre(self, genre):
        self.selected_genre = genre
        self.books_pool = load_books_by_genre(genre).copy()
        random.shuffle(self.books_pool)
        
        self.books_to_place = self.books_pool[:self.total_books]
        remaining = self.books_pool[self.total_books:]
        self.shelf_books = sort_books_by_rank(random.sample(remaining, min(4, len(remaining))))
        
        self.current_book_index = 0
        self.score = 0
        
        self.show_game_screen()
    
    def show_game_screen(self):
        self.clear_screen()
        self.current_screen = "game"
        self.setup_game_ui()
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
        
        tk.Label(header_frame, text="📚 Dewey's Library 📚",
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
        
        self.main_canvas = tk.Canvas(self.root, bg="#f5f0e8", width=1150, height=650, highlightthickness=0)
        self.main_canvas.pack(pady=5)
        
        self.book_labels = []
        self.slot_areas = []
        self.hovered_slot = None
        self.selected_slot = None
        self.book_images = []
        self.shelf_y = 400
    
    def draw_game(self):
        self.update_instructions()
        self.draw_shelf()
        self.draw_bookshelf()
        self.draw_book_to_place()
    
    def update_instructions(self):
        if self.current_book_index < len(self.books_to_place):
            current_book = self.books_to_place[self.current_book_index]
            # Unpack the 4-element tuple
            title, author, color, rank = current_book 
            self.instruction_label.config(
                text=f"Drag '{title}' (Rank: {rank}) from the trolley to the correct spot!\n(Books are sorted by rank)"
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

        # Unpack the 4-element tuple
        title, author, color, rank = self.books_to_place[self.current_book_index] 
        
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
        
        self.main_canvas.tag_bind("draggable", "<Button-1>", self.start_drag)
        self.main_canvas.tag_bind("draggable", "<B1-Motion>", self.on_drag)
        self.main_canvas.tag_bind("draggable", "<ButtonRelease-1>", self.end_drag)
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
        
# -- bookshelf with other books ---
    
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
            
            self.main_canvas.tag_bind(f"slot_{i}", "<Enter>", lambda e, idx=i: self.on_slot_hover(idx))
            self.main_canvas.tag_bind(f"slot_{i}", "<Leave>", lambda e: self.on_slot_leave())
            
            if i < len(self.shelf_books):
                current_x += book_widths[i] + spacing
        
        current_x = start_x
        for i, (title, author, color, rank) in enumerate(self.shelf_books):
            book_width = book_widths[i]
            book_height, font_size = self.calculate_book_dimensions(title, author, book_width)
            y = self.shelf_y - book_height
            
            self.book_labels.append({
                'index': i, 'original_x': current_x, 'current_x': current_x,
                'y': y, 'width': book_width, 'height': book_height,
                'title': title, 'author': author, 'color': color, 'font_size': font_size,
                'rank': rank
            })
            
            self.draw_book_spine(i, current_x, y, book_width, book_height, color, title, author, font_size, rank)
            current_x += book_width + spacing
    
    def calculate_book_dimensions(self, title, author, width):
        max_font_size = 18
        min_font_size = 12
        max_book_height = 450
        min_book_height = 200
        
        title_text = title
        author_text = author.upper()
        separator = "    "
        
        vertical_padding = 60
        horizontal_padding = 20

        for font_size in range(max_font_size, min_font_size - 1, -1):
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size, index=1)
                author_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size, index=2)
            except:
                title_font = ImageFont.load_default()
                author_font = ImageFont.load_default()
            
            title_length = title_font.getlength(title_text)
            separator_length = title_font.getlength(separator)
            author_length = author_font.getlength(author_text)
            total_length = title_length + separator_length + author_length
            
            required_height = int(total_length) + vertical_padding
            text_fits_width = total_length <= (width - horizontal_padding)
            
            if required_height <= max_book_height and text_fits_width:
                return required_height, font_size

        return int(total_length) + vertical_padding, min_font_size

    def draw_book_spine(self, index, x, y, width, height, color, title, author, font_size, rank):
        book_img = self.create_book_spine_image(width, height, color, title, author, font_size, rank)
        self.book_images.append(book_img)
        self.main_canvas.create_image(x, y, image=book_img, anchor='nw', tags=f"book_{index}")
    
    def create_book_spine_image(self, width, height, color, title, author, font_size, rank):
        img = Image.new('RGB', (width, height), color)
        draw = ImageDraw.Draw(img)
        
        dark = self.darken_color(color)
        light = self.lighten_color(color)
        
        for i in range(10):
            draw.rectangle([i, 0, i+1, height], fill=dark)
        for i in range(10):
            draw.rectangle([width-i-1, 0, width-i, height], fill=light)
        draw.rectangle([8, 8, width-8, 22], fill=light)
        draw.rectangle([0, 0, width-1, height-1], outline='black', width=3)
        
        title_text = title
        author_text = author.upper()
        separator = "    "
        
        text_fill_color = 'black' if color == "#ffb6c1" else ('#006400' if color == "#e8d5b7" else 'white')

        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size, index=1)
            author_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size, index=2)
        except IOError:
            title_font = ImageFont.load_default()
            author_font = ImageFont.load_default()

        text_img_width = height - 60
        text_img_height = width - 20
        
        text_img = Image.new('RGBA', (text_img_width, text_img_height), (255, 255, 255, 0))
        text_draw = ImageDraw.Draw(text_img)

        title_length = title_font.getlength(title_text)
        separator_length = title_font.getlength(separator)
        author_length = author_font.getlength(author_text)
        total_length = title_length + separator_length + author_length
        
        text_img_center_x = text_img_width // 2
        text_img_center_y = text_img_height // 2

        start_x = text_img_center_x - (total_length / 2)

        text_draw.text((start_x, text_img_center_y), title_text, fill=text_fill_color, font=title_font, anchor='lm')
        start_x += title_length + separator_length
        
        text_draw.text((start_x, text_img_center_y), author_text, fill=text_fill_color, font=author_font, anchor='lm')
        
        rotated = text_img.rotate(90, expand=True)
        paste_x = (width - rotated.width) // 2
        paste_y = (height - rotated.height) // 2
        img.paste(rotated, (paste_x, paste_y), rotated)
        
        return ImageTk.PhotoImage(img)
    
    # ----------------------------------------------------------------------------------------
    
    # -------------------
    
    def darken_color(self, color):
        if isinstance(color, str):
            color = color.lstrip('#')
            r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        else:
            r, g, b = color
        r, g, b = max(0, r - 50), max(0, g - 50), max(0, b - 50)
        if isinstance(color, str):
            return f'#{r:02x}{g:02x}{b:02x}'
        return (r, g, b)
    
    def lighten_color(self, color):
        if isinstance(color, str):
            color = color.lstrip('#')
            r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        else:
            r, g, b = color
        r, g, b = min(255, r + 50), min(255, g + 50), min(255, b + 50)
        if isinstance(color, str):
            return f'#{r:02x}{g:02x}{b:02x}'
        return (r, g, b)

    def start_drag(self, event):
        self.dragging = True
    
    @staticmethod
    def rect_overlap(rect1, rect2):
        # rect is (x1, y1, x2, y2)
        return not (rect1[2] < rect2[0] or # rect1 is to the left of rect2
                    rect1[0] > rect2[2] or # rect1 is to the right of rect2
                    rect1[3] < rect2[1] or # rect1 is above rect2
                    rect1[1] > rect2[3])   # rect1 is below rect2

    def on_drag(self, event):
        if not hasattr(self, 'dragging') or not self.dragging:
            return
        
        bbox = self.main_canvas.bbox("draggable")
        if not bbox:
            return
        
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        dx, dy = event.x - center_x, event.y - center_y
        self.main_canvas.move("draggable", dx, dy)
        
        for slot_idx, slot_rect, _ in self.slot_areas:
            coords = self.main_canvas.coords(slot_rect)
            if coords and self.rect_overlap(bbox, coords):
                self.on_slot_hover(slot_idx)
                return
        self.on_slot_leave()
    
    def end_drag(self, event):
        self.dragging = False
        
        bbox = self.main_canvas.bbox("draggable") # Get the bounding box of the dragged item
        if not bbox: # If for some reason bbox is empty, reset and return
            self.main_canvas.delete("draggable")
            self.draw_book_to_place()
            self.on_slot_leave()
            return

        for slot_idx, slot_rect, _ in self.slot_areas:
            coords = self.main_canvas.coords(slot_rect)
            if coords and self.rect_overlap(bbox, coords): # Use rect_overlap here
                self.selected_slot = slot_idx
                self.check_answer()
                return
        
        self.main_canvas.delete("draggable")
        self.draw_book_to_place()
        self.on_slot_leave()
    
    def on_slot_hover(self, slot_idx):
        if not self.dragging:
            return
        if self.hovered_slot == slot_idx:
            return
        self.hovered_slot = slot_idx
        
        # Get the width of the book being dragged to determine gap size
        gap_size = self.drag_book_info.get('width', 268) # Default width if not set

        for book in self.book_labels:
            if book['index'] >= slot_idx:
                book['current_x'] = book['original_x'] + gap_size
            else:
                book['current_x'] = book['original_x']
            self.redraw_book(book)
    
    def on_slot_leave(self):
        if self.selected_slot is not None:
            return
        self.hovered_slot = None
        for book in self.book_labels:
            book['current_x'] = book['original_x']
            self.redraw_book(book)
    
    def redraw_book(self, book):
        self.main_canvas.delete(f"book_{book['index']}")
        self.draw_book_spine(book['index'], book['current_x'], book['y'],
                            book['width'], book['height'], book['color'],
                            book['title'], book['author'], book['font_size'],
                            book['rank']) # Pass rank to draw_book_spine
    
    def check_answer(self):
        if self.selected_slot is None:
            return
        
        current_book = self.books_to_place[self.current_book_index]
        correct_position = check_book_position(current_book, self.shelf_books)
        
        if self.selected_slot == correct_position:
            self.score += 10
            self.shelf_books.insert(correct_position, current_book)
            messagebox.showinfo("Correct! 🎉", f"Perfect! +10 points!\nScore: {self.score}")
        else:
            temp_list = self.shelf_books + [current_book]
            # Assumes temp_list books are (title, author, color, rank)
            book_list = "\n".join([f"'{b[0]}' by {b[1]} (Rank: {b[3]})" for b in sort_books_by_rank(temp_list)]) # Changed sort_books_by_author to sort_books_by_rank
            messagebox.showwarning("Not quite! 😅", f"You're dumb:\n\n{book_list}")
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
    
    def end_game(self):
        self.clear_screen()
        self.current_screen = "end_game"
        
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

        canvas = tk.Canvas(self.root, bg="#f5f0e8", width=1200, height=900, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        canvas.create_text(600, 250, text="Game Complete! 🎉",
                          font=("Georgia", 48, "bold"), fill="#3d2817")
        
        canvas.create_text(600, 350, text=f"Final Score: {self.score}/{self.total_books * 10}",
                          font=("Georgia", 36), fill="#4a7c8c")
        
        if self.score == self.total_books * 10:
            canvas.create_text(600, 450, text="Perfect! The library is organized! 📚✨",
                              font=("Georgia", 24, "italic"), fill="#6b4423")
        else:
            canvas.create_text(600, 450, text="Great job helping organize! 📚",
                              font=("Georgia", 24, "italic"), fill="#6b4423")
        
        play_again_btn = tk.Button(
            self.root, text="Play Again",
            font=("Georgia", 24, "bold"),
            bg="#4a7c8c", fg="#008080",
            padx=40, pady=20,
            command=self.show_title_screen,
            cursor="hand2"
        )
        canvas.create_window(600, 600, window=play_again_btn)

if __name__ == "__main__":
    root = tk.Tk()
    game = LibraryGame(root)
    root.mainloop()