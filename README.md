# 📚 Dewey's Library Sorting Game

**Introduction to Python - Final Project**  
**ISA Masters in Green Data Science**  
**Academic Year 2025-2026**
---

## 📖 Project Overview

Dewey's Library Sorting Game is an interactive educational application that teaches library organization principles through an engaging sorting challenge. Players help organize a library's book collection by placing books in correct alphabetical order while dealing with mischievous geese who have disrupted the shelves.

### 🎯 Educational Objectives:
- **Library Science:** Understanding alphabetical organization systems
- **Critical Thinking:** Distinguishing between first names and surnames
- **Pattern Recognition:** Identifying correct alphabetical order
- **Attention to Detail:** Following dynamic sorting instructions

### 🎮 Game Concept:
The game presents players with five books already on a shelf and one new book that needs to be placed in the correct position. The twist: each game session randomly chooses to sort books by either the author's **first name** OR **surname**, requiring players to read instructions carefully and apply the appropriate sorting logic.

---

## ✅ Project Requirements Compliance

| # | Requirement | Status | Implementation Details |
|---|-------------|--------|----------------------|
| **1** | Implemented in Python | ✅ | Python 3.x with modern libraries |
| **2** | Main + 3+ tested functions | ✅ | `main()` + 6 core functions in library_game_logic.py |
| **3** | project.py in root | ✅ | Main file: project6.py (632 lines) |
| **4** | Functions at same indentation | ✅ | All functions defined at module level |
| **5** | test_project.py with pytest | ✅ | Comprehensive test suite with 15+ functions |
| **6** | At least one class | ✅ | `LibraryGame` class with 30+ methods |
| **7** | Additional classes/functions | ✅ | `backgroundhandler`, `DragManager` + 20+ utility functions |
| **8** | Significant time/effort | ✅ | 1600+ total lines, complex GUI, multiple features |
| **9** | Limited manual input | ✅ | All data loaded from JSON and files |
| **10** | requirements.txt | ✅ | All dependencies properly listed |

---

## 🏗️ Project Architecture

```
GithubVersion/
│
├── game/
│   ├── project6.py              # Main application (632 lines)
│   ├── library_game_logic.py    # Core sorting algorithms and validation
│   ├── test_project.py          # Comprehensive test suite (15+ tests)
│   ├── requirements.txt         # Project dependencies
│   ├── README.md                # This documentation
│   │
│   └── src/                     # Modular enhancement system
│       ├── __init__.py          # Package initialization
│       ├── notifications.py     # Canvas overlay feedback system
│       ├── progress_tracker.py  # JSON-based persistence
│       ├── end_screen.py        # Dynamic end screens
│       ├── reset_progress.py    # Progress reset functionality
│       ├── gamebackground.py    # Background image management
│       ├── bookspines.py        # 3D book spine rendering
│       └── drag_logic.py        # Drag-and-drop mechanics
│
├── artifacts/
│   ├── story/                   # Story sequence images (3 slides)
│   │   ├── 1goosedream.png
│   │   ├── 2angrylibrarian.png
│   │   └── 3modeselect.png
│   │
│   ├── progress/                # Feedback images
│   │   ├── good.png             # Success feedback (happy geese)
│   │   └── bad.png              # Error feedback (angry librarian)
│   │
│   ├── gameplay/
│   │   └── gameplay_background.png  # Main game screen background
│   │
│   ├── finalscores/             # 8 dynamic end screen backgrounds
│   │   ├── library_all_messy         # Starting state (0 genres)
│   │   ├── library_classic_only      # 1 genre completed
│   │   ├── library_romance_only      # 1 genre completed
│   │   ├── library_thriller_only     # 1 genre completed
│   │   ├── library_classic_romance   # 2 genres completed
│   │   ├── library_classic_thriller  # 2 genres completed
│   │   ├── library_romance_thriller  # 2 genres completed
│   │   └── library_all_clean         # All genres completed!
│   │
│   └── book_covers/
│       └── local_game_images.json    # Complete book database
│
└── game_progress.json           # Auto-generated progress file
```

---

## 🚀 Installation & Setup

### Prerequisites:
- Python 3.8 or higher
- pip package manager

### Installation Steps:

```bash
# 1. Clone or download the repository
cd GithubVersion/game

# 2. Install required dependencies
pip install -r requirements.txt

# 3. Run the game
python project6.py

# 4. Run tests (optional)
pytest test_project.py -v
```

---

## 🎮 How to Play

### Game Flow:

**1. Title Screen**
- Click "Start Game" to begin
- Click "Start Fresh" to reset all progress

**2. Story Sequence (3 slides)**
- Introduction: Dreaming geese
- Problem: Angry librarian discovers chaos
- Solution: Help organize the library
- Navigate with "Next" and "Back" buttons

**3. Genre Selection**
Choose from three literary genres:
- 📕 **Classic Literature** - Timeless works
- 💕 **Romance** - Love stories
- 🔪 **Thriller** - Suspenseful novels

Visual indicators:
- ✓ Checkmark on completed genres
- Colored badges (gold, pink, red)
- Best score display

**4. Sorting Challenge (Main Gameplay)**

**Critical:** Read the instruction carefully!
- Each game randomly selects: **Sort by FIRST NAME** or **Sort by SURNAME**
- This changes with every new game session

**Gameplay:**
1. Five books appear on the library shelf
2. A new book appears at the bottom of the screen
3. **Drag and drop** the new book to its correct alphabetical position
4. Instant feedback:
   - ✅ **Correct:** Happy geese appear (+10 points, continue to next book)
   - ❌ **Wrong:** Angry librarian shows correct order (try again, no points)
5. Complete 5 books to finish the round (maximum 50 points)

**5. End Screen**
- View your final score
- Background image reflects your overall progress
- Three options:
  - **Try Again:** Replay the same genre (new random sorting method)
  - **New Game:** Reset all progress, return to title
  - **Continue:** Return to genre selection

---

## 🔧 Technical Implementation

### Main Components:

#### **LibraryGame Class** (project6.py)
The central game controller managing all aspects:

**Core Responsibilities:**
- **UI Management:** All screen rendering and transitions
- **Game State:** Score tracking, current genre, progress
- **Event Handling:** Mouse events, keyboard shortcuts, window resize
- **Logic Integration:** Connects UI with game logic modules

**Key Methods:**
- `show_title_screen()` - Renders main menu
- `show_story()` - Manages story sequence with navigation
- `show_game_screen()` - Initializes gameplay interface
- `draw_game()` - Renders books and game elements
- `check_answer()` - Validates player's book placement
- `next_book()` - Advances to next sorting challenge
- `end_game()` - Transitions to end screen with results

#### **Core Functions** (library_game_logic.py)

**Required Tested Functions:**

1. **`get_author_surname(author: str) -> str`**
   ```python
   # Extracts surname from full author name
   # "Jane Austen" -> "Austen"
   # "Gabriel García Márquez" -> "Márquez"
   ```

2. **`get_author_first_name(author: str) -> str`**
   ```python
   # Extracts first name from full author name
   # "Jane Austen" -> "Jane"
   # "F. Scott Fitzgerald" -> "F."
   ```

3. **`check_book_position(books, new_book, position, sort_by) -> bool`**
   ```python
   # Validates alphabetical placement
   # Returns True if book is in correct position
   # Core algorithm: insert book, sort list, compare
   ```

**Supporting Functions:**

4. **`load_books_by_genre(genre: str) -> list`**
   - Loads book data from JSON database
   - Returns list of (title, author, color) tuples

5. **`sort_books_by_surname(books: list) -> list`**
   - Sorts books alphabetically by author surname
   - Used for validation and displaying correct order

6. **`sort_books_by_first_name(books: list) -> list`**
   - Sorts books alphabetically by author first name
   - Alternative sorting method

---

## 🧪 Testing Suite

### Test Coverage (test_project.py)

**15+ Comprehensive Test Functions:**

**Author Name Parsing Tests:**
- `test_get_author_surname()` - Standard surname extraction
- `test_get_author_surname_multiple_names()` - Handles middle names
- `test_get_author_surname_single_word()` - Edge case: single name
- `test_get_author_first_name()` - Standard first name extraction
- `test_get_author_first_name_complex()` - Handles initials, prefixes

**Book Position Validation Tests:**
- `test_check_book_position_correct()` - Validates correct placements
- `test_check_book_position_incorrect()` - Detects wrong placements
- `test_check_book_position_beginning()` - Tests first position
- `test_check_book_position_end()` - Tests last position
- `test_check_book_position_empty_shelf()` - Edge case: empty list

**Sorting Algorithm Tests:**
- `test_sort_books_by_surname()` - Surname sorting accuracy
- `test_sort_books_by_first_name()` - First name sorting accuracy
- `test_sort_identical_surnames()` - Duplicate handling
- `test_sort_mixed_case()` - Case sensitivity handling

**Data Loading Tests:**
- `test_load_books_by_genre()` - JSON loading functionality
- `test_load_books_invalid_genre()` - Error handling

**Progress Tracking Tests:**
- `test_save_and_load_progress()` - Persistence verification
- `test_mark_genre_complete()` - Completion tracking

**Running Tests:**
```bash
# Run all tests with verbose output
pytest test_project.py -v

# Run specific test
pytest test_project.py::test_check_book_position_correct -v

# Run with coverage report
pytest test_project.py --cov=library_game_logic --cov-report=html
```

**Expected Result:** All tests pass ✅

---

## 🎨 Key Features

### 1. Dual Sorting System 🔀

**Innovation:** Each game session uses ONE of two sorting methods:
- Sort alphabetically by **author's first name** (A-Z)
- Sort alphabetically by **author's surname** (A-Z)

**Implementation:**
```python
self.sort_method = random.choice(['surname', 'first_name'])
```

**Educational Impact:**
- Teaches difference between first names and surnames
- Requires careful attention to instructions
- Adds significant replay value
- Mirrors real-world library practices (most libraries sort by surname)

**Example:**
```
Books: Jane Austen, Emily Brontë, Charles Dickens

Sort by FIRST NAME:
Charles Dickens, Emily Brontë, Jane Austen

Sort by SURNAME:
Jane Austen, Emily Brontë, Charles Dickens
```

### 2. Canvas Overlay Notification System 🎭

**Design Philosophy:** Non-blocking, integrated feedback

**Traditional Approach (Modal Dialogs):**
- ❌ Interrupts game flow
- ❌ Requires clicking through dialogs
- ❌ Feels disconnected from game

**Our Approach (Canvas Overlays):**
- ✅ Appears directly on game canvas
- ✅ Smooth, integrated animations
- ✅ Click anywhere to dismiss
- ✅ Professional appearance

**Implementation:**
```python
# Centered popup calculation
popup_x = (canvas_width - popup_width) // 2
popup_y = (canvas_height - popup_height) // 2

# Everything uses 'popup' tag for easy removal
canvas.create_rectangle(..., tags="popup")
canvas.create_image(..., tags="popup")
canvas.delete("popup")  # Remove all at once
```

**Feedback Types:**
- **Correct Answer:** Happy geese image with success message
- **Wrong Answer:** Angry librarian image with correct order displayed

### 3. Progress Tracking & Persistence 📊

**Storage System:**
- **Format:** JSON file (`game_progress.json`)
- **Location:** Project root (auto-created on first run)
- **Structure:**
  ```json
  {
    "classic": {"completed": true, "score": 50},
    "romance": {"completed": false, "score": 0},
    "thriller": {"completed": true, "score": 40}
  }
  ```

**Features:**
- Tracks completion status per genre (boolean)
- Stores best score achieved per genre (integer)
- Persists across game sessions
- Safe reset functionality with confirmation

**Visual Indicators:**
- ✓ Checkmarks on genre selection screen
- Colored completion badges (genre-specific colors)
- Best score display for completed genres

**Reset Functionality:**
- "Start Fresh" button on title screen
- Confirmation dialog prevents accidental deletion
- Safely deletes and recreates progress file

### 4. Dynamic End Screen System 🖼️

**Progression-Based Backgrounds:**

The game includes **8 different background images** that change based on which genres you've completed:

| Completed Genres | Background Image | Visual State |
|-----------------|------------------|--------------|
| None (0/3) | `library_all_messy` | Chaos - books everywhere |
| Classic only (1/3) | `library_classic_only` | Classics section organized |
| Romance only (1/3) | `library_romance_only` | Romance section organized |
| Thriller only (1/3) | `library_thriller_only` | Thriller section organized |
| Classic + Romance (2/3) | `library_classic_romance` | Two sections clean |
| Classic + Thriller (2/3) | `library_classic_thriller` | Two sections clean |
| Romance + Thriller (2/3) | `library_romance_thriller` | Two sections clean |
| All three (3/3) | `library_all_clean` | Perfect! Fully organized |

**Implementation:**
```python
completed = {k: v.get('completed', False) 
             for k, v in genre_progress.items()}

if all(completed.values()): 
    bg_file = "library_all_clean"
elif completed.get('classic') and completed.get('romance'): 
    bg_file = "library_classic_romance"
# ... (checking all 8 combinations)
else: 
    bg_file = "library_all_messy"
```

**Educational Value:**
- Visual reward for completing genres
- Shows progressive improvement
- Motivates players to complete all genres
- Creates sense of accomplishment

### 5. Professional Book Spine Rendering 📚

**3D Visual Effects:**
- Left edge shading (darker) for depth
- Right edge highlighting (lighter) for dimension
- Top accent strip for detail
- Black border outline for definition
- Rotated text for realistic spine orientation

**Genre Color Coding:**
- **Classic Literature:** Beige (#e8d5b7) - Traditional, scholarly
- **Romance:** Pink (#ffb6c1) - Warm, emotional
- **Thriller:** Dark Red (#8b4513) - Intense, mysterious

**Responsive Text Rendering:**
- Font size range: 16-24pt (auto-adjusted)
- Text fits width constraint
- Handles long titles gracefully
- Proper centering and rotation
- Readable at all window sizes

**Algorithm:**
```python
# Find optimal font size that fits
for font_size in range(24, 15, -1):
    if text_fits_width and height_ok:
        return font_size
```

### 6. Responsive Design System 📱

**Window Resize Handling:**
- All UI elements scale proportionally
- Background images resize dynamically (LANCZOS resampling)
- Text remains readable at any size
- Buttons maintain proper spacing and proportions
- Percentage-based positioning

**Supported Window Modes:**
- Default windowed (1200x900)
- Maximized window
- Custom sizes (any reasonable dimensions)
- Fullscreen compatible

**Implementation:**
```python
canvas.bind('<Configure>', self.on_resize)

def on_resize(self, event):
    new_width = event.width
    new_height = event.height
    # Recalculate all positions and sizes
```

### 7. Modular Architecture 🧩

**src/ Folder Organization:**

**Design Principle:** Separation of concerns - each module has one clear responsibility

1. **notifications.py** (Canvas overlays)
   - Non-blocking feedback system
   - Centered popup calculations
   - Image loading and display
   - Event binding for dismissal

2. **progress_tracker.py** (Persistence)
   - JSON file reading/writing
   - Default value handling
   - Completion tracking
   - Visual badge creation

3. **end_screen.py** (End screens)
   - Dynamic background selection
   - Score display
   - Button placement
   - Continue/Reset/Home logic

4. **reset_progress.py** (Reset functionality)
   - Confirmation dialogs
   - Safe file deletion
   - Fresh state creation
   - Success notifications

5. **gamebackground.py** (Background management)
   - Image loading with multiple path attempts
   - Responsive resizing
   - Canvas z-order management
   - Fallback color handling

6. **bookspines.py** (Book rendering)
   - 3D visual effects (shading, highlights)
   - Text sizing algorithms
   - Rotation and positioning
   - Color utilities

7. **drag_logic.py** (Drag-and-drop)
   - Mouse event management
   - Position tracking
   - Visual feedback during drag
   - Drop zone detection

**Benefits:**
- Easy to maintain and extend
- Clear file responsibilities
- Reusable components
- Simplified testing
- Professional structure

---

## 📦 Dependencies

### requirements.txt:
```
tkinter          # GUI framework (included with Python)
Pillow>=10.0.0   # Image processing library
pytest>=7.0.0    # Testing framework
```

### Installation Notes:
- **tkinter:** Usually pre-installed with Python
  - Windows/Mac: Included by default
  - Linux: `sudo apt-get install python3-tk`
- **Pillow:** `pip install Pillow`
- **pytest:** `pip install pytest`

---

## 🎓 Educational Value

### Skills Taught:

**Library Science Concepts:**
- Alphabetical organization systems (Dewey Decimal principles)
- Author name structure (first name vs. surname)
- Genre classification (Classic, Romance, Thriller)
- Systematic shelf organization

**Computer Science Concepts Demonstrated:**
- **Object-Oriented Programming:**
  - Classes and methods
  - Encapsulation and abstraction
  - State management
  
- **GUI Development:**
  - Event-driven programming
  - Canvas drawing and manipulation
  - Responsive layout design
  - User interaction handling

- **Data Structures:**
  - Lists and tuples
  - Dictionaries for lookup
  - JSON serialization
  
- **Algorithms:**
  - Sorting algorithms (alphabetical)
  - Comparison operations
  - Search and validation

- **Software Engineering:**
  - Modular design
  - Separation of concerns
  - Error handling
  - Comprehensive testing
  - Documentation

**Critical Thinking:**
- Pattern recognition (alphabetical order)
- Attention to detail (reading instructions)
- Quick decision-making
- Learning from mistakes (seeing correct order)

---

## 🔬 Technical Challenges Solved

### 1. Canvas Layer Management (Z-Order)

**Problem:** Background images appeared above book spines and game elements

**Solution:** Canvas tag system with explicit ordering
```python
canvas.create_image(0, 0, image=bg, tags="background")
canvas.tag_lower("background")  # Push to bottom layer
```

**Learning:** tkinter canvas uses a stack-based z-order system

### 2. Dynamic Path Resolution

**Problem:** Hardcoded paths broke when running from different directories

**Solution:** Relative path calculation from script location
```python
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "..", "artifacts", "story", "image.png")
```

**Learning:** Always use `os.path` for cross-platform compatibility

### 3. Responsive Window Sizing

**Problem:** Fixed pixel positions broke when window resized

**Solution:** Percentage-based positioning and `<Configure>` event binding
```python
canvas.bind('<Configure>', self.on_resize)

def on_resize(self, event):
    # Recalculate positions based on new dimensions
    center_x = event.width * 0.5
    button_y = event.height * 0.85
```

**Learning:** Responsive design requires proportional calculations

### 4. JSON Progress Persistence

**Problem:** Game state lost between sessions, crashes on missing file

**Solution:** Try-except with default value fallback
```python
try:
    with open("game_progress.json", "r") as f:
        return json.load(f)
except FileNotFoundError:
    return default_progress
```

**Learning:** Always handle file I/O exceptions gracefully

### 5. Custom Drag-and-Drop Implementation

**Problem:** tkinter doesn't have built-in drag-and-drop for canvas items

**Solution:** Mouse event binding state machine
```python
canvas.bind('<Button-1>', self.on_click)      # Start drag
canvas.bind('<B1-Motion>', self.on_drag)       # During drag
canvas.bind('<ButtonRelease-1>', self.on_release)  # End drag

# Track state
self.dragging = False
self.drag_data = {"item": None, "x": 0, "y": 0}
```

**Learning:** Complex interactions require state tracking

### 6. Image Memory Management

**Problem:** Images disappeared after function returns (garbage collection)

**Solution:** Maintain references in instance variables
```python
self.image_ref = ImageTk.PhotoImage(img)
canvas.create_image(x, y, image=self.image_ref)
# Keep reference alive as long as needed
```

**Learning:** Python garbage collection requires explicit reference management

### 7. Module Import from Subdirectories

**Problem:** Importing from `src/` folder failed

**Solution:** Proper package structure with `__init__.py`
```
src/
├── __init__.py  # Makes it a package
├── notifications.py
└── ...

# Now can import:
from src.notifications import show_popup
```

**Learning:** Python packages require `__init__.py` files

---

## 🚀 Future Enhancement Possibilities

### Gameplay Enhancements:
- [ ] **Multiple difficulty levels**
  - Easy: 3 books per round
  - Medium: 5 books (current)
  - Hard: 8 books per round
  - Expert: 10 books with time limit

- [ ] **Timed challenges**
  - Speed mode with countdown timer
  - Bonus points for quick correct answers
  - Time penalties for mistakes

- [ ] **Additional sorting methods**
  - By book title (A-Z)
  - By publication year
  - By Dewey Decimal number
  - Mixed sorting (combines multiple methods)

- [ ] **More literary genres**
  - Science Fiction
  - Historical Fiction
  - Biography/Autobiography
  - Fantasy
  - Mystery (distinct from Thriller)
  - Non-Fiction

### Technical Enhancements:
- [ ] **Sound system**
  - Background music (volume controls)
  - Success/failure sound effects
  - Ambient library sounds
  - Mute option

- [ ] **Leaderboard system**
  - Local high scores database
  - Online leaderboard (requires backend)
  - Weekly/monthly challenges
  - Achievement system

- [ ] **Hint system**
  - Show first letter of correct slot
  - Highlight correct position (limited uses)
  - Tutorial mode for beginners
  - Progressive hints (costs points)

- [ ] **Multiplayer mode**
  - Local hot-seat (take turns)
  - Split-screen competition
  - Online multiplayer (requires networking)
  - Cooperative mode (team play)

- [ ] **Analytics dashboard**
  - Track accuracy over time
  - Genre performance comparison
  - Learning curve visualization
  - Mistake pattern analysis

- [ ] **Accessibility features**
  - Screen reader support
  - High contrast mode
  - Larger text options
  - Keyboard-only controls
  - Color blind friendly palette

---

## 📄 License & Academic Integrity

This project was developed as coursework for:

- **Course:** Introduction to Python
- **Program:** Masters in Green Data Science
- **Institution:** Instituto Superior de Agronomia (ISA)
- **Academic Year:** 2025-2026
- **Instructor:** Prof. Manuel Campagnolo (mlc@isa.ulisboa.pt)
- **Teaching Assistant:** Mekaela Stevenson (mekaela@edu.ulisboa.pt)

**Academic Use:** This code is submitted for academic evaluation. It should not be copied, redistributed, or reused for other academic submissions without proper attribution and permission.

**Citation:** If referencing this work, please cite:
```
Vale, L. (2026). Dewey's Library Sorting Game: An Interactive Educational 
Application for Library Organization. Introduction to Python Final Project, 
ISA Masters in Green Data Science.
```

---

## 🙏 Acknowledgments

- **Instructor & Teaching Assistant:** For guidance, feedback, and support throughout the course
- **ISA Masters Program:** For providing the educational framework and learning opportunity
- **Python Community:** For excellent documentation and open-source libraries
- **Library Science Community:** For alphabetization standards and organizational principles

**Special Thanks:**
- The tkinter and Pillow development teams for robust, well-documented libraries
- The pytest team for making Python testing straightforward and effective
- Fellow students for collaborative learning and mutual support

---

## 📧 Contact & Support

**Author:** Luis Vale  
**Student ID:** 25952  
**Program:** ISA Masters in Green Data Science  
**Email:** [Available through ISA academic system]

**For Project Questions:**
- Review this README documentation
- Check inline code comments for implementation details
- Examine `test_project.py` for usage examples
- Review function docstrings for parameter specifications

**For Bug Reports:**
- Include steps to reproduce
- Note your Python version (`python --version`)
- Specify operating system
- Provide error messages if applicable

---

## 🎯 Quick Reference

### Running the Game:
```bash
cd GithubVersion/game
python project6.py
```

### Running Tests:
```bash
pytest test_project.py -v
```

### File Structure:
- **Main:** `project6.py` (632 lines)
- **Logic:** `library_game_logic.py` (6 functions)
- **Tests:** `test_project.py` (15+ functions)
- **Modules:** `src/` (7 enhancement files)
- **Data:** `artifacts/` (images, JSON)

### Key Features:
1. Dual sorting (first name/surname)
2. Canvas overlays (smooth feedback)
3. Progress tracking (JSON persistence)
4. Dynamic backgrounds (8 variations)
5. Professional UI (3D books, responsive)
6. Comprehensive testing (15+ tests)
7. Modular architecture (7 modules)

---

## 📊 Project Statistics

- **Total Lines of Code:** ~1,600
- **Main File:** 632 lines
- **Test Functions:** 15+
- **Enhancement Modules:** 7
- **Classes Implemented:** 3 (LibraryGame, backgroundhandler, DragManager)
- **Tested Functions:** 6
- **JSON Data Points:** 50+ books across 3 genres
- **Visual Assets:** 20+ images
- **Development Time:** Significant effort across multiple weeks

---

**Thank you for reviewing Dewey's Library Sorting Game!**

*Keep those geese happy and the librarian satisfied!* 🪿📚✨

---
