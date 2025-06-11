import math
import time
import random
from graphics import Canvas

# --- Canvas and Game Constants ---
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
GRID_SIZE = 20 # Size of Karol and the goal, also movement step
INITIAL_DELAY = 0.1
KAROL_IMAGE = "Karol.png"
MAX_SCORE = 50 # Maximum score to win the game
BACKGROUND_CHANGE_DELAY = 2 # Delay for background cycling on start/end screens

# --- Color Palettes ---
# Start Screen Color Palettes
START_PALETTES = [
    {
        "bg": ["#FF5733", "#FF8D33", "#FFC133", "#FFE433", "#FFF8DC"], # Sunset Hues
        "shimmer": ["#FFFFFF", "#FFDAB9", "#FFDEAD"]
    },
    {
        "bg": ["#228B22", "#3CB371", "#66CDAA", "#8FBC8F", "#B0E0E6"], # Forest & Gold
        "shimmer": ["#FFD700", "#DAA520", "#B8860B"]
    },
    {
        "bg": ["#000080", "#0000CD", "#1E90FF", "#87CEEB", "#ADD8E6"], # Ocean Depths
        "shimmer": ["#FFFFFF", "#F0F8FF", "#E0FFFF"]
    },
    {
        "bg": ["#8B4513", "#A0522D", "#D2B48C", "#F5DEB3", "#FFFACD"], # Warm Earth
        "shimmer": ["#F4A460", "#D2691E", "#CD853F"]
    },
    {
        "bg": ["#8A2BE2", "#4B0082", "#9400D3", "#FF00FF", "#00FFFF"], # Vibrant Neon
        "shimmer": ["#FFFFFF", "#00FF00", "#FFD700"]
    }
]

# Button Colors (for Start Screen)
BUTTON_COLOR = "#FF6347" 	 	# Tomato
BUTTON_HOVER_COLOR = "#FF4500" 	# OrangeRed
BUTTON_SHADOW_COLOR = "#CD5C5C" # IndianRed
BUTTON_HIGHLIGHT_COLOR = "#FFDAB9" # PeachPuff
BUTTON_TEXT_COLOR = "white"

# Restart Screen Color Palettes
RESTART_PALETTES = [
    {
        "bg": ["#2F4F4F", "#708090", "#A9A9A9", "#D3D3D3", "#F5F5F5"], # Cool Grays
        "shimmer": ["#FFFFFF", "#E0E0E0", "#C0C0C0"]
    },
    {
        "bg": ["#006400", "#228B22", "#3CB371", "#66CDAA", "#8FBC8F"], # Deep Forest
        "shimmer": ["#F0FFF0", "#90EE90", "#32CD32"]
    },
    {
        "bg": ["#000033", "#000066", "#000099", "#0000CC", "#0000FF"], # Cosmic Blues
        "shimmer": ["#ADD8E6", "#B0E0E6", "#87CEEB"]
    },
    {
        "bg": ["#8B0000", "#CD5C5C", "#FFA07A", "#FFD700", "#FFEFD5"], # Autumn Glow
        "shimmer": ["#FFFFFF", "#FFDAB9", "#FFDEAD"]
    }
]

# Restart Button Colors
RESTART_BUTTON_COLOR = "#4682B4" 	 	# SteelBlue
RESTART_BUTTON_HOVER_COLOR = "#5F9EA0" 	# CadetBlue
RESTART_BUTTON_SHADOW_COLOR = "#2F4F4F" # DarkSlateGray
RESTART_BUTTON_HIGHLIGHT_COLOR = "#AFEEEE" # PaleTurquoise
RESTART_BUTTON_TEXT_COLOR = "white"

# Mode Selection Button Colors
MODE_BUTTON_COLOR = "#4CAF50" # Green
MODE_BUTTON_HOVER_COLOR = "#45A049" # Darker Green
MODE_BUTTON_SHADOW_COLOR = "#388E3C" # Even Darker Green
MODE_BUTTON_HIGHLIGHT_COLOR = "#8BC34A" # Light Green
MODE_BUTTON_TEXT_COLOR = "white"

# --- Helper Functions ---

def rgb_to_hex(r, g, b):
    """Converts RGB color values to a hexadecimal string."""
    return f"#{r:02x}{g:02x}{b:02x}"

def estimate_text_width(text, font_size, multiplier):
    """
    Estimates the pixel width of text for centering purposes.
    This is a heuristic and may not be perfectly accurate for all fonts/sizes.
    """
    return font_size * multiplier * len(text)

def draw_centered_text(canvas, center_x, y, text, font_size, color, font='Arial', multiplier=0.5):
    """
    Draws text horizontally centered on the canvas.
    Returns the ID of the created text object.
    """
    text_width = estimate_text_width(text, font_size, multiplier)
    true_x = center_x - text_width / 2
    return canvas.create_text(
        true_x, y,
        text,
        font=font,
        font_size=font_size,
        color=color
    )

def draw_dynamic_background(canvas, palette):
    """
    Draws a background with a gradient and shimmering stars based on a given palette.
    Returns a list of all created background element IDs.
    """
    background_elements = []
    gradient_colors = palette["bg"]
    shimmer_colors = palette["shimmer"]

    gradient_steps = len(gradient_colors)
    step_height = CANVAS_HEIGHT / gradient_steps

    for i in range(gradient_steps):
        y_start = i * step_height
        y_end = (i + 1) * step_height
        rect = canvas.create_rectangle(0, y_start, CANVAS_WIDTH, y_end, gradient_colors[i], gradient_colors[i])
        background_elements.append(rect)

    for _ in range(100): # Number of sparkles
        x = random.randint(0, CANVAS_WIDTH)
        y = random.randint(0, CANVAS_HEIGHT)
        size = random.randint(1, 3)
        color = random.choice(shimmer_colors)
        oval = canvas.create_oval(x, y, x + size, y + size, color, color)
        background_elements.append(oval)
    return background_elements

def draw_colorful_polygon(canvas, center_x, center_y, num_sides=4, radius=10, rotation_offset=0.1):
    """Draws a colorful, layered polygon."""
    base_points = []
    for n in range(num_sides):
        angle = 2 * math.pi * n / num_sides + rotation_offset
        x = center_x + radius * math.sin(angle)
        y = center_y - radius * math.cos(angle)
        base_points.append((x, y))

    layers = 5
    for i in range(layers):
        factor = i / layers
        points = []
        for x, y in base_points:
            new_x = center_x + (x - center_x) * (1 - factor * 0.9)
            new_y = center_y + (y - center_y) * (1 - factor * 0.9)
            points.extend([new_x, new_y])

        r = int(255 * abs(math.sin(factor * math.pi)))
        g = int(255 * abs(math.sin(factor * math.pi + 2 * math.pi / 3)))
        b = int(255 * abs(math.sin(factor * math.pi + 4 * math.pi / 3)))
        color = rgb_to_hex(r, g, b)

        polygon_id = canvas.create_polygon(*points)
        canvas.set_color(polygon_id, color)

def place_goal(canvas):
    """Places a new goal (colorful polygon inside a rectangle) on the canvas."""
    cols = CANVAS_WIDTH // GRID_SIZE
    rows = CANVAS_HEIGHT // GRID_SIZE
    x = random.randint(0, cols - 1) * GRID_SIZE
    y = random.randint(0, rows - 1) * GRID_SIZE

    center_x = x + GRID_SIZE / 2
    center_y = y + GRID_SIZE / 2
    draw_colorful_polygon(canvas, center_x, center_y)

    return canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, "#3e85c6")

def get_position(canvas, obj):
    """Returns the top-left (x, y) coordinates of a canvas object."""
    x = canvas.get_left_x(obj)
    y = canvas.get_top_y(obj)
    if x is None or y is None:
        return -1, -1 # Indicates object might have been deleted or not yet drawn
    return int(x), int(y)

def is_out_of_bounds(x, y, obj_width, obj_height):
    """Checks if the given coordinates are outside the canvas boundaries."""
    return x < 0 or x + obj_width > CANVAS_WIDTH or y < 0 or y + obj_height > CANVAS_HEIGHT

def draw_button(canvas, x, y, width, height, text, font_size, base_color, hover_color, shadow_color, highlight_color, text_color, text_multiplier=0.5):
    """
    Draws a generic button with shadow and highlight.
    Returns the IDs of the button elements and its bounds for later manipulation.
    """
    # Shadow
    shadow_offset = 5
    shadow_rect = canvas.create_rectangle(
        x + shadow_offset, y + shadow_offset,
        x + width + shadow_offset, y + height + shadow_offset,
        shadow_color, shadow_color
    )

    # Button body
    button_rect = canvas.create_rectangle(
        x, y,
        x + width, y + height,
        base_color, shadow_color # Fill and outline
    )

    # Highlight
    highlight_rect = canvas.create_rectangle(
        x + 3, y + 3,
        x + width - 3, y + 20,
        highlight_color, highlight_color
    )

    # Button text
    text_y = y + height / 2 - font_size / 2
    button_label = draw_centered_text(canvas, x + width / 2, text_y, text, font_size, text_color, multiplier=text_multiplier)

    return button_rect, button_label, shadow_rect, highlight_rect, (x, y, width, height)


def draw_start_button(canvas):
    """
    Draws the 'Start Game' button with shadow and highlight.
    Returns the IDs of the button elements for later manipulation.
    """
    button_width = 200
    button_height = 70
    button_x = (CANVAS_WIDTH - button_width) / 2
    button_y = (CANVAS_HEIGHT - button_height) / 2 + 50 # Slightly lower than center
    font_size = 24
    button_text = "🚀 Start Game 🚀"
    
    return draw_button(canvas, button_x, button_y, button_width, button_height, button_text, font_size,
                       BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_SHADOW_COLOR, BUTTON_HIGHLIGHT_COLOR, BUTTON_TEXT_COLOR, 0.59)


def draw_mode_selection_screen(canvas):
    """
    Draws the mode selection screen with two buttons: Classic and Infinite.
    Returns a dictionary of button data for interaction.
    """
    mode_title = draw_centered_text(canvas, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 100, "Choose Your Quest!", 30, "white", font='Impact', multiplier=0.5)

    button_width = 250
    button_height = 60
    button_spacing = 20
    
    # Classic Mode Button
    classic_x = (CANVAS_WIDTH - button_width) / 2
    classic_y = CANVAS_HEIGHT / 2 - button_height - button_spacing / 2
    classic_button_data = draw_button(canvas, classic_x, classic_y, button_width, button_height, "⚔️ Classic Mode (3 Lives)", 20,
                                      MODE_BUTTON_COLOR, MODE_BUTTON_HOVER_COLOR, MODE_BUTTON_SHADOW_COLOR, MODE_BUTTON_HIGHLIGHT_COLOR, MODE_BUTTON_TEXT_COLOR, 0.55)

    # Infinite Mode Button
    infinite_x = (CANVAS_WIDTH - button_width) / 2
    infinite_y = CANVAS_HEIGHT / 2 + button_spacing / 2
    infinite_button_data = draw_button(canvas, infinite_x, infinite_y, button_width, button_height, "♾️ Infinite Mode (No Walls)", 20,
                                        MODE_BUTTON_COLOR, MODE_BUTTON_HOVER_COLOR, MODE_BUTTON_SHADOW_COLOR, MODE_BUTTON_HIGHLIGHT_COLOR, MODE_BUTTON_TEXT_COLOR, 0.4)
    
    return {
        "title_id": mode_title,
        "classic": {"ids": classic_button_data[:4], "bounds": classic_button_data[4], "mode": "classic"},
        "infinite": {"ids": infinite_button_data[:4], "bounds": infinite_button_data[4], "mode": "infinite"}
    }


def wait_for_start_button_click(canvas, initial_button_rect, initial_shadow_rect, initial_highlight_rect, initial_button_label, initial_button_bounds, initial_game_title_text):
    """
    Waits for the user to click the 'Start Game' button.
    Includes hover and click effects and cycles through start screen backgrounds.
    """
    button_x, button_y, button_width, button_height = initial_button_bounds
    is_hovering = False
    current_bg_elements = []
    palette_index = 0

    # Store initial IDs for recreation
    game_title_id = initial_game_title_text
    button_rect_id = initial_button_rect
    button_label_id = initial_button_label
    shadow_rect_id = initial_shadow_rect
    highlight_rect_id = initial_highlight_rect

    while True:
        # Delete old background elements
        for element_id in current_bg_elements:
            canvas.delete(element_id)
        
        # Draw new background
        current_bg_elements = draw_dynamic_background(canvas, START_PALETTES[palette_index])
        palette_index = (palette_index + 1) % len(START_PALETTES)

        # Redraw title and button on top of new background
        # Delete old button and title elements before recreating
        canvas.delete(game_title_id)
        canvas.delete(button_rect_id)
        canvas.delete(button_label_id)
        canvas.delete(shadow_rect_id)
        canvas.delete(highlight_rect_id)

        # Recreate title
        game_title_id = draw_centered_text(canvas, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 100, "🤖 Karol's Quest 🤖", 36, "white", font='Impact', multiplier=0.5)
        
        # Recreate button elements
        shadow_rect_id = canvas.create_rectangle(
            button_x + 5, button_y + 5,
            button_x + button_width + 5, button_y + button_height + 5,
            BUTTON_SHADOW_COLOR, BUTTON_SHADOW_COLOR
        )
        button_rect_id = canvas.create_rectangle(
            button_x, button_y,
            button_x + button_width, button_y + button_height,
            BUTTON_COLOR, BUTTON_SHADOW_COLOR
        )
        highlight_rect_id = canvas.create_rectangle(
            button_x + 3, button_y + 3,
            button_x + button_width - 3, button_y + 20,
            BUTTON_HIGHLIGHT_COLOR, BUTTON_HIGHLIGHT_COLOR
        )
        button_label_id = draw_centered_text(canvas, button_x + button_width / 2, button_y + button_height / 2 - 24 / 2, "🚀 Start Game 🚀", 24, BUTTON_TEXT_COLOR, multiplier=0.59)


        # Check for mouse position for hover effect
        mouse_x = canvas.get_mouse_x()
        mouse_y = canvas.get_mouse_y()
        current_hovering = (button_x <= mouse_x <= button_x + button_width and
                            button_y <= mouse_y <= button_y + button_height)

        if current_hovering and not is_hovering:
            # Mouse entered button area
            canvas.set_color(button_rect_id, BUTTON_HOVER_COLOR)
            canvas.set_color(highlight_rect_id, BUTTON_HIGHLIGHT_COLOR) # Ensure highlight stays visible
            is_hovering = True
        elif not current_hovering and is_hovering:
            # Mouse left button area
            canvas.set_color(button_rect_id, BUTTON_COLOR)
            canvas.set_color(highlight_rect_id, BUTTON_HIGHLIGHT_COLOR) # Reset highlight
            is_hovering = False

        # Check for click
        click = canvas.get_last_click()
        if click is not None:
            click_x, click_y = click
            if current_hovering: # If clicked while hovering over the button
                # Click effect: briefly change color, then fade out
                canvas.set_color(button_rect_id, BUTTON_HOVER_COLOR) # Darker on click
                canvas.set_color(highlight_rect_id, BUTTON_HIGHLIGHT_COLOR)
                time.sleep(0.1) # Short delay for visual feedback

                # Clear ALL start screen elements (including background)
                canvas.delete(button_rect_id)
                canvas.delete(button_label_id)
                canvas.delete(shadow_rect_id)
                canvas.delete(highlight_rect_id)
                canvas.delete(game_title_id) # Delete the game title
                for element_id in current_bg_elements:
                    canvas.delete(element_id)
                
                return # Exit the loop, game can start

        time.sleep(BACKGROUND_CHANGE_DELAY) # Delay for background change, not game loop


def wait_for_mode_selection(canvas, mode_buttons_data):
    """
    Waits for the user to click one of the mode selection buttons.
    Handles hover and click effects and cycles through start screen backgrounds.
    Returns the selected game mode ('classic' or 'infinite').
    """
    current_bg_elements = []
    palette_index = 0
    
    # Store initial IDs for recreation from mode_buttons_data
    title_id = mode_buttons_data["title_id"]
    classic_button_ids = mode_buttons_data["classic"]["ids"]
    classic_button_bounds = mode_buttons_data["classic"]["bounds"]
    infinite_button_ids = mode_buttons_data["infinite"]["ids"]
    infinite_button_bounds = mode_buttons_data["infinite"]["bounds"]

    # Unpack button IDs for easier access
    classic_rect_id, classic_label_id, classic_shadow_id, classic_highlight_id = classic_button_ids
    infinite_rect_id, infinite_label_id, infinite_shadow_id, infinite_highlight_id = infinite_button_ids

    is_classic_hovering = False
    is_infinite_hovering = False

    while True:
        # Delete old background elements and foreground elements from previous iteration
        for element_id in current_bg_elements:
            canvas.delete(element_id)
        canvas.delete(title_id)
        
        # Delete old button elements before recreating
        for btn_id in classic_button_ids: canvas.delete(btn_id)
        for btn_id in infinite_button_ids: canvas.delete(btn_id)

        # Draw new background
        current_bg_elements = draw_dynamic_background(canvas, START_PALETTES[palette_index])
        palette_index = (palette_index + 1) % len(START_PALETTES)

        # Recreate title
        title_id = draw_centered_text(canvas, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 148, "Choose Your Quest", 30, "white", font='Impact', multiplier=0.45)

        # Recreate Classic Mode Button
        classic_rect_id, classic_label_id, classic_shadow_id, classic_highlight_id, _ = draw_button(
            canvas, classic_button_bounds[0], classic_button_bounds[1], classic_button_bounds[2], classic_button_bounds[3],
            "⚔️ Classic Mode (3 Lives)", 20, MODE_BUTTON_COLOR, MODE_BUTTON_HOVER_COLOR, MODE_BUTTON_SHADOW_COLOR, MODE_BUTTON_HIGHLIGHT_COLOR, MODE_BUTTON_TEXT_COLOR, 0.47
        )
        mode_buttons_data["classic"]["ids"] = (classic_rect_id, classic_label_id, classic_shadow_id, classic_highlight_id)

        # Recreate Infinite Mode Button
        infinite_rect_id, infinite_label_id, infinite_shadow_id, infinite_highlight_id, _ = draw_button(
            canvas, infinite_button_bounds[0], infinite_button_bounds[1], infinite_button_bounds[2], infinite_button_bounds[3],
            "♾️ Infinite Mode (No Walls)", 20, MODE_BUTTON_COLOR, MODE_BUTTON_HOVER_COLOR, MODE_BUTTON_SHADOW_COLOR, MODE_BUTTON_HIGHLIGHT_COLOR, MODE_BUTTON_TEXT_COLOR, 0.46
        )
        mode_buttons_data["infinite"]["ids"] = (infinite_rect_id, infinite_label_id, infinite_shadow_id, infinite_highlight_id)

        mouse_x = canvas.get_mouse_x()
        mouse_y = canvas.get_mouse_y()

        # Check hover for Classic button
        current_classic_hovering = (classic_button_bounds[0] <= mouse_x <= classic_button_bounds[0] + classic_button_bounds[2] and
                                    classic_button_bounds[1] <= mouse_y <= classic_button_bounds[1] + classic_button_bounds[3])
        if current_classic_hovering and not is_classic_hovering:
            canvas.set_color(classic_rect_id, MODE_BUTTON_HOVER_COLOR)
            is_classic_hovering = True
        elif not current_classic_hovering and is_classic_hovering:
            canvas.set_color(classic_rect_id, MODE_BUTTON_COLOR)
            is_classic_hovering = False

        # Check hover for Infinite button
        current_infinite_hovering = (infinite_button_bounds[0] <= mouse_x <= infinite_button_bounds[0] + infinite_button_bounds[2] and
                                     infinite_button_bounds[1] <= mouse_y <= infinite_button_bounds[1] + infinite_button_bounds[3])
        if current_infinite_hovering and not is_infinite_hovering:
            canvas.set_color(infinite_rect_id, MODE_BUTTON_HOVER_COLOR)
            is_infinite_hovering = True
        elif not current_infinite_hovering and is_infinite_hovering:
            canvas.set_color(infinite_rect_id, MODE_BUTTON_COLOR)
            is_infinite_hovering = False

        click = canvas.get_last_click()
        if click is not None:
            if current_classic_hovering:
                canvas.set_color(classic_rect_id, MODE_BUTTON_HOVER_COLOR)
                time.sleep(0.1)
                # Clear all mode selection elements
                canvas.delete(title_id)
                for btn_id in classic_button_ids: canvas.delete(btn_id)
                for btn_id in infinite_button_ids: canvas.delete(btn_id)
                for element_id in current_bg_elements: canvas.delete(element_id)
                return "classic"
            elif current_infinite_hovering:
                canvas.set_color(infinite_rect_id, MODE_BUTTON_HOVER_COLOR)
                time.sleep(0.1)
                # Clear all mode selection elements
                canvas.delete(title_id)
                for btn_id in classic_button_ids: canvas.delete(btn_id)
                for btn_id in infinite_button_ids: canvas.delete(btn_id)
                for element_id in current_bg_elements: canvas.delete(element_id)
                return "infinite"
        
        time.sleep(BACKGROUND_CHANGE_DELAY)


def draw_restart_screen_elements(canvas, message, score):
    """
    Prepares the restart screen elements (messages and button) for dynamic drawing.
    It does NOT draw the background here, as that's handled by draw_dynamic_background.
    Returns the content and positional data for these elements.
    """
    # Define positions for message and score
    message_y = CANVAS_HEIGHT / 2 - 80
    score_y = CANVAS_HEIGHT / 2 - 40

    # Define button properties
    button_width = 200
    button_height = 70
    button_x = (CANVAS_WIDTH - button_width) / 2
    button_y = (CANVAS_HEIGHT - button_height) / 2 + 50
    font_size = 24
    button_text = " 🔄 Restart Game "
    text_y = button_y + button_height / 2 - font_size / 2

    # Return all necessary content and positional data
    return (message, score, message_y, score_y,
            button_x, button_y, button_width, button_height, button_text, font_size, text_y)


def wait_for_restart_button_click(canvas, restart_screen_data):
    """
    Waits for the user to click the 'Restart Game' button on the game over/win screen.
    Includes hover and click effects and cycles through restart screen backgrounds.
    """
    message_content, score_content, message_y, score_y, \
    button_x, button_y, button_width, button_height, button_text, font_size, text_y = restart_screen_data

    is_hovering = False
    current_bg_elements = []
    palette_index = 0

    # Initialize element IDs for the first draw in the loop
    message_text_id = None
    score_text_id = None
    button_rect_id = None
    button_label_id = None
    shadow_rect_id = None
    highlight_rect_id = None

    while True:
        # Delete old background elements and foreground elements from previous iteration
        for element_id in current_bg_elements:
            canvas.delete(element_id)
        if message_text_id: canvas.delete(message_text_id)
        if score_text_id: canvas.delete(score_text_id)
        if button_rect_id: canvas.delete(button_rect_id)
        if button_label_id: canvas.delete(button_label_id)
        if shadow_rect_id: canvas.delete(shadow_rect_id)
        if highlight_rect_id: canvas.delete(highlight_rect_id)
        
        # Draw new background
        current_bg_elements = draw_dynamic_background(canvas, RESTART_PALETTES[palette_index])
        palette_index = (palette_index + 1) % len(RESTART_PALETTES)

        # Recreate message and score
        message_text_id = draw_centered_text(canvas, CANVAS_WIDTH / 2, message_y, message_content, 28, 'white', font='Impact', multiplier=0.35)
        score_text_id = draw_centered_text(canvas, CANVAS_WIDTH / 2, score_y, f"FINAL SCORE: {score_content}", 20, 'white', multiplier=0.5)

        # Recreate button elements
        shadow_rect_id = canvas.create_rectangle(
            button_x + 5, button_y + 5,
            button_x + button_width + 5, button_y + button_height + 5,
            RESTART_BUTTON_SHADOW_COLOR, RESTART_BUTTON_SHADOW_COLOR
        )
        button_rect_id = canvas.create_rectangle(
            button_x, button_y,
            button_x + button_width, button_y + button_height,
            RESTART_BUTTON_COLOR, RESTART_BUTTON_SHADOW_COLOR
        )
        highlight_rect_id = canvas.create_rectangle(
            button_x + 3, button_y + 3,
            button_x + button_width - 3, button_y + 20,
            RESTART_BUTTON_HIGHLIGHT_COLOR, RESTART_BUTTON_HIGHLIGHT_COLOR
        )
        button_label_id = draw_centered_text(canvas, button_x + button_width / 2, text_y, button_text, font_size, RESTART_BUTTON_TEXT_COLOR, multiplier=0.55)


        mouse_x = canvas.get_mouse_x()
        mouse_y = canvas.get_mouse_y()
        current_hovering = (button_x <= mouse_x <= button_x + button_width and
                            button_y <= mouse_y <= button_y + button_height)

        if current_hovering and not is_hovering:
            canvas.set_color(button_rect_id, RESTART_BUTTON_HOVER_COLOR)
            canvas.set_color(highlight_rect_id, RESTART_BUTTON_HIGHLIGHT_COLOR)
            is_hovering = True
        elif not current_hovering and is_hovering:
            canvas.set_color(button_rect_id, RESTART_BUTTON_COLOR)
            canvas.set_color(highlight_rect_id, RESTART_BUTTON_HIGHLIGHT_COLOR)
            is_hovering = False

        click = canvas.get_last_click()
        if click is not None:
            click_x, click_y = click
            if current_hovering:
                canvas.set_color(button_rect_id, RESTART_BUTTON_HOVER_COLOR)
                canvas.set_color(highlight_rect_id, RESTART_BUTTON_HIGHLIGHT_COLOR)
                time.sleep(0.1)

                # Clear all restart screen elements (including background)
                canvas.delete(button_rect_id)
                canvas.delete(button_label_id)
                canvas.delete(shadow_rect_id)
                canvas.delete(highlight_rect_id)
                canvas.delete(message_text_id)
                canvas.delete(score_text_id)
                for element_id in current_bg_elements:
                    canvas.delete(element_id)
                
                return # Exit loop, game restarts

        time.sleep(BACKGROUND_CHANGE_DELAY)


def run_karol_game(canvas, game_mode):
    """
    Contains the main game logic for Karol's Quest.
    Behavior (lives, wall collision) changes based on the selected game_mode.
    Returns the final message and score when the game ends.
    """
    # Clear anything remaining from the previous screen
    canvas.clear() 

    # Define Karol's size
    KAROL_SIZE = GRID_SIZE * 3 # Karol is 3x the GRID_SIZE

    # Initial position for Karol
    player_x, player_y = 0, 0
    player = canvas.create_image_with_size(player_x, player_y, KAROL_SIZE, KAROL_SIZE, KAROL_IMAGE)
    if player is None:
        print("Error: Failed to load Karol image. Ensure 'Karol.png' is in your project.")
        return "Error loading game!", 0

    score = 0
    lives = 3 if game_mode == 'classic' else -1 # -1 for infinite lives

    # Display score and lives (if classic mode)
    score_lives_text = None
    if game_mode == 'classic':
        score_lives_text = draw_centered_text(canvas, CANVAS_WIDTH / 2, 15, f"SCORE: {score} | LIVES: {lives}", 15, 'black', multiplier=0.5)
    else: # Infinite mode
        score_lives_text = draw_centered_text(canvas, CANVAS_WIDTH / 2, 15, f"SCORE: {score}", 15, 'black', multiplier=0.5)


    goal = place_goal(canvas)
    delay = INITIAL_DELAY
    direction = 'Right' # Initial direction for continuous movement

    while True:
        # Handle key presses to change direction
        key = canvas.get_last_key_press()
        if key == 'ArrowLeft' and direction != 'Right':
            direction = 'Left'
        elif key == 'ArrowRight' and direction != 'Left':
            direction = 'Right'
        elif key == 'ArrowUp' and direction != 'Down':
            direction = 'Up'
        elif key == 'ArrowDown' and direction != 'Up':
            direction = 'Down'
        
        # Calculate movement based on current direction
        dx, dy = 0, 0
        if direction == 'Left':
            dx = -GRID_SIZE
        elif direction == 'Right':
            dx = GRID_SIZE
        elif direction == 'Up':
            dy = -GRID_SIZE
        elif direction == 'Down':
            dy = GRID_SIZE

        # Move Karol
        canvas.move(player, dx, dy)
        player_x, player_y = get_position(canvas, player)

        # --- Game Mode Specific Wall Collision Logic ---
        if game_mode == 'classic':
            if is_out_of_bounds(player_x, player_y, KAROL_SIZE, KAROL_SIZE):
                lives -= 1 # Lose a life
                if lives == 0:
                    canvas.delete(player) # Remove Karol
                    canvas.delete(score_lives_text) # Remove score/lives display
                    return 'Karol has lost', score # Game Over message
                else:
                    # Reset Karol's position
                    player_x, player_y = 0, 0
                    canvas.moveto(player, player_x, player_y)
                    # Update score/lives display
                    canvas.change_text(score_lives_text, f"SCORE: {score} | LIVES: {lives}")
                    time.sleep(1) # Pause briefly
        elif game_mode == 'infinite':
            new_player_x, new_player_y = player_x, player_y

            if player_x < -KAROL_SIZE: # Went too far left
                new_player_x = CANVAS_WIDTH
            elif player_x > CANVAS_WIDTH: # Went too far right
                new_player_x = -KAROL_SIZE
            
            if player_y < -KAROL_SIZE: # Went too far up
                new_player_y = CANVAS_HEIGHT
            elif player_y > CANVAS_HEIGHT: # Went too far down
                new_player_y = -KAROL_SIZE
            
            # If Karol went out of bounds, move him to the new calculated position
            if new_player_x != player_x or new_player_y != player_y:
                canvas.moveto(player, new_player_x, new_player_y)
                player_x, player_y = new_player_x, new_player_y # Update current position


        # Get goal position (it might have been deleted and recreated by place_goal)
        goal_x, goal_y = get_position(canvas, goal)
        if goal_x == -1 or goal_y == -1: # If goal disappeared (e.g., eaten)
            goal = place_goal(canvas)
            goal_x, goal_y = get_position(canvas, goal)

        # Check if Karol reached the goal (adjusted for larger Karol)
        # Collision detection: Check if Karol's bounding box overlaps with the goal's bounding box
        player_right = player_x + KAROL_SIZE
        player_bottom = player_y + KAROL_SIZE
        goal_right = goal_x + GRID_SIZE
        goal_bottom = goal_y + GRID_SIZE

        if not (player_right <= goal_x or player_x >= goal_right or
                player_bottom <= goal_y or player_y >= goal_bottom):
            # Collision detected
            canvas.delete(goal) # Delete the old goal
            score += 1
            # Update score display
            if game_mode == 'classic':
                canvas.change_text(score_lives_text, f"SCORE: {score} | LIVES: {lives}")
            else:
                canvas.change_text(score_lives_text, f"SCORE: {score}")
            
            if score >= MAX_SCORE:
                canvas.delete(player) # Remove Karol
                canvas.delete(score_lives_text) # Remove score/lives display
                return " Karol Reached the Max  ", score # Win message
            goal = place_goal(canvas) # Place a new goal
            delay = max(0.02, delay * 0.9) # Speed up the game

        time.sleep(delay)

def main():
    """
    Main function to initialize the canvas and manage the game flow, including start and end screens.
    """
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    # Outer loop to allow restarting the game
    while True:
        # Initial draw of title and button for the first iteration of the start screen
        game_title_text = draw_centered_text(canvas, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 100, "🤖 Karol's Quest 🤖", 36, "white", font='Impact', multiplier=0.5)
        button_rect, button_label, shadow_rect, highlight_rect, button_bounds = draw_start_button(canvas)
        
        # Wait for the button to be clicked, passing initial elements to be managed
        wait_for_start_button_click(canvas, button_rect, shadow_rect, highlight_rect, button_label, button_bounds, game_title_text)

        # After start button, show mode selection screen
        mode_buttons_data = draw_mode_selection_screen(canvas)
        selected_mode = wait_for_mode_selection(canvas, mode_buttons_data)

        # Once a mode is selected, the game starts
        final_message, final_score = run_karol_game(canvas, selected_mode) # Pass the selected mode

        # After the game ends, prepare restart screen data
        restart_screen_data = draw_restart_screen_elements(canvas, final_message, final_score)
        
        # Wait for restart button click, passing the data to redraw elements
        wait_for_restart_button_click(canvas, restart_screen_data)
        
        # The loop will continue, drawing the start screen again for a new game
        # The canvas is cleared by the restart button click handler before returning here.

if __name__ == '__main__':
    main()
