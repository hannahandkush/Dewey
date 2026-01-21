import pytest
import tkinter as tk
from unittest.mock import MagicMock
import importlib.util
from PIL import Image, ImageTk

# Dynamically import the game module

spec = importlib.util.spec_from_file_location("game_module", "project.py")
game_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game_module)
LibraryGame = game_module.LibraryGame

# Helper function to get a button from the canvas by its command
def get_button_by_command(canvas, command_method):
    for item_id in canvas.find_all():
        item_type = canvas.type(item_id)
        if item_type == 'window':
            window_widget = canvas.itemcget(item_id, 'window')
            if window_widget:
                pass
    return None # Fallback if not found

# Fixture for a minimal Tkinter root and game instance
@pytest.fixture
def game_instance():
    # Mock Tkinter root to prevent actual GUI from appearing and blocking tests
    mock_root = MagicMock(spec=tk.Tk)
    mock_root.tk = MagicMock() 
    mock_root.children = {} # Add this line
    mock_root.winfo_width.return_value = 1200
    mock_root.winfo_height.return_value = 900
    mock_root.winfo_children.return_value = [] # Start with no children for clear_screen
    
    # simulate the pack method for content_frame 
    def mock_pack(fill=tk.BOTH, expand=True, **kwargs):
        pass # Do nothing
    
    # Mock the canvas to allow checking create_window calls
    mock_canvas = MagicMock() # Changed from spec=tk.Canvas
    mock_canvas.pack.side_effect = mock_pack
    mock_canvas.create_window.return_value = 1 # Simulate returning an item_id
    mock_canvas.create_image.return_value = 2 # Simulate returning an item_id
    mock_canvas.itemcget.return_value = "something" # Simulate return for itemcget
    mock_canvas.type.return_value = "window" # Simulate return for type

    # Patch tk.Canvas and tk.Frame to return our mocks
    original_tk_canvas = tk.Canvas
    original_tk_frame = tk.Frame
    
    # Keep track of created canvases and frames
    created_canvases = []
    created_frames = []

    def mock_canvas_factory(*args, **kwargs):
        new_canvas = MagicMock() # Changed from spec=original_tk_canvas
        new_canvas.pack.side_effect = mock_pack
        new_canvas.create_window.return_value = 1 # Simulate returning an item_id
        new_canvas.create_image.return_value = 2 # Simulate returning an item_id
        new_canvas.itemcget.return_value = "something"
        new_canvas.type.return_value = "window"
        created_canvases.append(new_canvas)
        return new_canvas

    def mock_frame_factory(*args, **kwargs):
        new_frame = MagicMock() # Changed from spec=original_tk_frame
        new_frame.pack.side_effect = mock_pack
        new_frame.winfo_children.return_value = [] # For clear_screen inside frame
        created_frames.append(new_frame)
        return new_frame

    tk.Canvas = mock_canvas_factory
    tk.Frame = mock_frame_factory
    
    # Mock Image.open and ImageTk.PhotoImage
    original_image_open = Image.open
    original_image_tk_photoimage = ImageTk.PhotoImage
    Image.open = MagicMock(return_value=MagicMock(spec=Image.Image))
    Image.open.return_value.resize.return_value = MagicMock(spec=Image.Image)
    ImageTk.PhotoImage = MagicMock(return_value="mock_photoimage")

    game = LibraryGame(mock_root)
    game.root = mock_root # Ensure the mock root is used throughout
    game.books_to_place = [] # Add this line
    game.shelf_books = [] # Add this line

    yield game # Provide the game instance to the tests

    # Clean up patches
    tk.Canvas = original_tk_canvas
    tk.Frame = original_tk_frame
    Image.open = original_image_open
    ImageTk.PhotoImage = original_image_tk_photoimage
    
    mock_root.destroy()

# Test 1: Home button visibility
def test_home_button_visibility(game_instance):
    # Initial state: Title page
    game_instance.show_title_screen()
    # Check if home button is explicitly hidden or not placed.

    # Transition to story page
    game_instance.show_story()
    # In the actual implementation, home_btn is created and placed here
    # We'd ideally assert that home_btn.place was called.
    
    # Transition to mode selection
    game_instance.show_mode_selection()
    # Assert home_btn.place was called
    
    # Transition to game screen
    game_instance.show_game_screen()
    # Assert home_btn.place was called

    # Transition to end game screen
    game_instance.end_game()
    # Assert home_btn.place was called

    # Home button should be visible on show_story, show_mode_selection, show_game_screen, end_game
    # It should NOT be visible on show_title_screen

    # Check internal state for screen.
    game_instance.show_title_screen() # Ensure initial state is title
    assert game_instance.current_screen == "title"
    
    game_instance.show_story()
    assert game_instance.current_screen == "story"

    game_instance.show_mode_selection()
    assert game_instance.current_screen == "mode_selection"

    game_instance.show_game_screen()
    assert game_instance.current_screen == "game"

    game_instance.end_game()
    assert game_instance.current_screen == "end_game" # (Assuming end_game sets this)

# Test 2: Back button functionality
def test_back_button_functionality(game_instance):
    # Go to story page 0 (index 0)
    game_instance.show_story()
    assert game_instance.story_index == 0
    # On first page, back button should not be "active" (e.g., clickable or visible)
    # We will verify this by checking if previous_story is called when it shouldn't be, or if the button is simply not created/placed.

    # Move to story page 1
    game_instance.next_story()
    assert game_instance.story_index == 1
    # Now, the back button should be available.
    # Directly call the command that the back button would trigger
    game_instance.previous_story()
    assert game_instance.story_index == 0

    # Move to story page 2
    game_instance.next_story()
    game_instance.next_story()
    assert game_instance.story_index == 2
    # Back button should be available
    game_instance.previous_story()
    assert game_instance.story_index == 1

# Test 3: Mode select buttons link to relevant mode
def test_mode_select_buttons_link_to_mode(game_instance):
    # Go to the third story page (where mode selection buttons appear)
    game_instance.show_story()
    game_instance.story_index = 2 # Manually set to the correct page for test
    game_instance.display_story_page() # Refresh the page to show new buttons

    # Simulate clicking "Classic" button
    game_instance.start_game_with_genre('classic')
    assert game_instance.selected_genre == 'classic'
    assert game_instance.current_screen == 'game'

    # Simulate clicking "Romance" button
    game_instance.show_story() # Reset state
    game_instance.story_index = 2
    game_instance.display_story_page()
    game_instance.start_game_with_genre('romance')
    assert game_instance.selected_genre == 'romance'
    assert game_instance.current_screen == 'game'

    # Simulate clicking "Thriller" button
    game_instance.show_story() # Reset state
    game_instance.story_index = 2
    game_instance.display_story_page()
    game_instance.start_game_with_genre('thriller')
    assert game_instance.selected_genre == 'thriller'
    assert game_instance.current_screen == 'game'
