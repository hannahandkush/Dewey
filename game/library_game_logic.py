import random
import os
import json

def get_author_surname(author):
    """
    Extract the surname (last name) from an author's full name.
    """
    return author.split()[-1]

def sort_books_by_rank(books): # Renamed function
    """
    Sort a list of books by their assigned rank.
    """
    # Assuming books are (title, author, color, rank) tuples
    return sorted(books, key=lambda x: x[3])

def check_book_position(book, shelf_books):
    """
    Calculate the correct position for a book on a sorted shelf.
    """
    temp_list = shelf_books + [book]
    sorted_list = sort_books_by_rank(temp_list) # Call sort_books_by_rank
    return sorted_list.index(book)

def load_books_by_genre(genre):
    """
    Load book data for a specific genre, including rank, from a list-based JSON structure.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to game_images.json (now a list of book dictionaries, includes rank)
    game_images_json_path = os.path.join(script_dir, "..", "artifacts", "book_covers", "game_images.json")

    all_books_raw_list = [] # It's a list now
    try:
        with open(game_images_json_path, "r") as f:
            all_books_raw_list = json.load(f) # Loads a list
    except FileNotFoundError:
        print(f"Error: game_images.json not found at {game_images_json_path}")
        return []
    
    genre_colors = {
        'classic': "#e8d5b7",
        'romance': "#ffb6c1",
        'thriller': "#3d2817"
    }
    default_color = genre_colors.get(genre, "#cccccc")

    filtered_books = []
    for book_data in all_books_raw_list: # Iterate the list
        if book_data.get("Genre") and book_data["Genre"].lower() == genre.lower():
            title = book_data.get("title")
            author_first = book_data.get("author first name", "")
            author_surname = book_data.get("author surname", "")
            full_author = f"{author_first} {author_surname}".strip() # Construct full name
            color = genre_colors.get(book_data["Genre"].lower(), default_color)
            rank = book_data.get("rank") # Get the rank
            filtered_books.append((title, full_author, color, rank)) # Store rank
            
    return filtered_books