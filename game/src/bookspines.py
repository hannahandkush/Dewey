"""
Bookshelf Renderer Module
Improved book spine rendering with better dimensions and fonts
Created from Hannah's bookspines.py
"""

from PIL import Image, ImageDraw, ImageFont, ImageTk


def calculate_book_dimensions(title, author, width):
    """
    Calculate optimal book dimensions based on title, author, and width.
    Hannah's improved version with larger fonts and better fitting.
    
    Args:
        title (str): Book title
        author (str): Book author
        width (int): Book spine width
    
    Returns:
        tuple: (height, font_size)
    """
    max_font_size = 24  # Hannah's improved: increased from 18
    min_font_size = 16  # Hannah's improved: increased from 12
    max_book_height = 400  # Hannah's improved: decreased from 500
    min_book_height = 300  # Hannah's improved: increased from 200
    
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
        
        # Hannah's improvement: check both height AND width constraints
        if required_height <= max_book_height and text_fits_width:
            return required_height, font_size

    return int(total_length) + vertical_padding, min_font_size


def create_book_spine_image(width, height, color, title, author, font_size):
    """
    Create a book spine image with improved rendering.
    Hannah's version with swapped font indices for better appearance.
    
    Args:
        width (int): Spine width
        height (int): Spine height
        color (str): Background color
        title (str): Book title
        author (str): Book author
        font_size (int): Font size to use
    
    Returns:
        ImageTk.PhotoImage: The rendered book spine image
    """
    img = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(img)
    
    # Create 3D effect with shading
    dark = darken_color(color)
    light = lighten_color(color)
    
    # Draw shading
    for i in range(10):
        draw.rectangle([i, 0, i+1, height], fill=dark)
    for i in range(10):
        draw.rectangle([width-i-1, 0, width-i, height], fill=light)
    draw.rectangle([8, 8, width-8, 22], fill=light)
    draw.rectangle([0, 0, width-1, height-1], outline='black', width=3)
    
    title_text = title
    author_text = author.upper()
    separator = "    "
    
    # Determine text color based on background
    text_fill_color = 'black' if color == "#ffb6c1" else ('#006400' if color == "#e8d5b7" else 'white')

    try:
        # Hannah's improvement: swapped font indices for better appearance
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size, index=2)
        author_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size, index=1)
    except IOError:
        title_font = ImageFont.load_default()
        author_font = ImageFont.load_default()

    # Create rotated text image
    text_img_width = height - 60
    text_img_height = width - 20
    
    text_img = Image.new('RGBA', (text_img_width, text_img_height), (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_img)

    # Calculate text positioning
    title_length = title_font.getlength(title_text)
    separator_length = title_font.getlength(separator)
    author_length = author_font.getlength(author_text)
    total_length = title_length + separator_length + author_length
    
    text_img_center_x = text_img_width // 2
    text_img_center_y = text_img_height // 2

    start_x = text_img_center_x - (total_length / 2)

    # Draw title and author
    text_draw.text((start_x, text_img_center_y), title_text, fill=text_fill_color, font=title_font, anchor='lm')
    start_x += title_length + separator_length
    text_draw.text((start_x, text_img_center_y), author_text, fill=text_fill_color, font=author_font, anchor='lm')
    
    # Rotate and paste onto spine
    rotated = text_img.rotate(90, expand=True)
    paste_x = (width - rotated.width) // 2
    paste_y = (height - rotated.height) // 2
    img.paste(rotated, (paste_x, paste_y), rotated)
    
    return ImageTk.PhotoImage(img)

def darken_color(color):
    """Darken a color for shading effect"""
    if isinstance(color, str):
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    else:
        r, g, b = color
    r, g, b = max(0, r - 50), max(0, g - 50), max(0, b - 50)
    if isinstance(color, str):
        return f'#{r:02x}{g:02x}{b:02x}'
    return (r, g, b)


def lighten_color(color):
    """Lighten a color for highlight effect"""
    if isinstance(color, str):
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    else:
        r, g, b = color
    r, g, b = min(255, r + 50), min(255, g + 50), min(255, b + 50)
    if isinstance(color, str):
        return f'#{r:02x}{g:02x}{b:02x}'
    return (r, g, b)
