from graphics import Canvas
import time
import random

# --- Canvas and Game Constants ---
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600
PADDLE_Y = CANVAS_HEIGHT - 30
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
BRICK_GAP = 5
BRICK_ROWS = 10
BRICKS_PER_ROW = 10
BRICK_WIDTH = (CANVAS_WIDTH - BRICK_GAP * (BRICKS_PER_ROW - 1)) / BRICKS_PER_ROW
BRICK_HEIGHT = 10
INITIAL_BALL_SPEED = 10
GAME_DELAY = 0.01 # Base delay for game loop, adjusted for speed
BACKGROUND_CHANGE_DELAY = 0.5 # Delay for background cycling

# --- Color Palettes ---
# Start Screen Color Palettes
START_PALETTES = [
    {
        "bg": ["#1A0033", "#330066", "#4D0099", "#6600CC", "#8000FF"], # Deep Purple
        "shimmer": ["#FFFFFF", "#E0E0E0", "#FFD700"]
    },
    {
        "bg": ["#001F3F", "#003366", "#004080", "#0059B3", "#007FFF"], # Deep Ocean Blue
        "shimmer": ["#ADD8E6", "#B0E0E6", "#87CEEB"]
    },
    {
        "bg": ["#36013F", "#54015F", "#72017F", "#90019F", "#AE01AF"], # Dark Rose
        "shimmer": ["#F0F8FF", "#FFE4E1", "#FFC0CB"]
    },
    {
        "bg": ["#000000", "#1A1A1A", "#333333", "#4D4D4D", "#666666"], # Grayscale
        "shimmer": ["#FFFFFF", "#CCCCCC", "#999999"]
    },
    {
        "bg": ["#2F4F4F", "#4682B4", "#5F9EA0", "#6A5ACD", "#7B68EE"], # Muted Forest Green to Lavender
        "shimmer": ["#F5F5DC", "#FFF8DC", "#FAFAD2"]
    }
]

# Button Colors (for Start Screen)
BUTTON_COLOR = "#6A0DAD"        # Amethyst
BUTTON_HOVER_COLOR = "#8A2BE2"  # Blue Violet
BUTTON_SHADOW_COLOR = "#330066" # Dark purple for shadow
BUTTON_HIGHLIGHT_COLOR = "#E6E6FA" # Lavender Blush for highlight
BUTTON_TEXT_COLOR = "white"

# Game Element Colors
PADDLE_COLOR = "black"
BALL_COLOR = "blue"
BRICK_COLORS = ["red", "orange", "yellow", "green", "blue"] # Top to bottom

# Restart Screen Color Palettes
RESTART_PALETTES = [
    {
        "bg": ["#0A192F", "#0B2240", "#112A4A", "#1C3D63", "#2D5079"], # Original Restart Blue
        "shimmer": ["#ADD8E6", "#B0E0E6", "#87CEEB"]
    },
    {
        "bg": ["#8B0000", "#A52A2A", "#CD5C5C", "#DC143C", "#FF6347"], # Fiery Red
        "shimmer": ["#FFD700", "#FFA500", "#FF4500"]
    },
    {
        "bg": ["#004d40", "#00695c", "#00897b", "#00a69a", "#00c8b6"], # Teal Green
        "shimmer": ["#e0f2f1", "#b2dfdb", "#80cbc4"]
    },
    {
        "bg": ["#424242", "#616161", "#757575", "#9e9e9e", "#bdbdbd"], # Dark Gray to Light Gray
        "shimmer": ["#FFFFFF", "#E0E0E0", "#BDBDBD"]
    }
]

# Restart Button Colors
RESTART_BUTTON_COLOR = "#4CAF50"        # Green
RESTART_BUTTON_HOVER_COLOR = "#66BB6A"  # Lighter Green
RESTART_BUTTON_SHADOW_COLOR = "#2E7D32" # Dark Green
RESTART_BUTTON_HIGHLIGHT_COLOR = "#A5D6A7" # Pale Green
RESTART_BUTTON_TEXT_COLOR = "white"


# --- Helper Functions ---

def estimate_text_width(text, font_size):
    """
    Estimates the pixel width of text for centering purposes.
    This is a heuristic and may not be perfectly accurate for all fonts/sizes.
    """
    return font_size * 0.59 * len(text) # Updated multiplier to 0.59

def draw_centered_text(canvas, center_x, y, text, font_size, color, font='Arial'):
    """
    Draws text horizontally centered on the canvas.
    Returns the ID of the created text object.
    """
    text_width = estimate_text_width(text, font_size)
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
    button_text = "🚀 Start Game"

    # Shadow
    shadow_offset = 5
    shadow_rect = canvas.create_rectangle(
        button_x + shadow_offset, button_y + shadow_offset,
        button_x + button_width + shadow_offset, button_y + button_height + shadow_offset,
        BUTTON_SHADOW_COLOR, BUTTON_SHADOW_COLOR
    )

    # Button body
    button_rect = canvas.create_rectangle(
        button_x, button_y,
        button_x + button_width, button_y + button_height,
        BUTTON_COLOR, BUTTON_SHADOW_COLOR # Fill and outline
    )

    # Highlight
    highlight_rect = canvas.create_rectangle(
        button_x + 3, button_y + 3,
        button_x + button_width - 3, button_y + 20,
        BUTTON_HIGHLIGHT_COLOR, BUTTON_HIGHLIGHT_COLOR
    )

    # Button text
    text_y = button_y + button_height / 2 - font_size / 2
    button_label = draw_centered_text(canvas, button_x + button_width / 2, text_y, button_text, font_size, BUTTON_TEXT_COLOR)

    return button_rect, button_label, shadow_rect, highlight_rect, (button_x, button_y, button_width, button_height)

def draw_restart_screen_and_button(canvas, message, score):
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
    button_text = "🔄 Restart Game"
    text_y = button_y + button_height / 2 - font_size / 2

    # Return all necessary content and positional data
    return (message, score, message_y, score_y,
            button_x, button_y, button_width, button_height, button_text, font_size, text_y)


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
        game_title_id = draw_centered_text(canvas, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 100, "🌌 Cosmic Breakout 🌌", 36, "white", font='Impact')
        
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
        button_label_id = draw_centered_text(canvas, button_x + button_width / 2, button_y + button_height / 2 - 24 / 2, "🚀 Start Game 🚀", 24, BUTTON_TEXT_COLOR)


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
        message_text_id = draw_centered_text(canvas, CANVAS_WIDTH / 2, message_y, message_content, 28, 'white', font='Impact')
        score_text_id = draw_centered_text(canvas, CANVAS_WIDTH / 2, score_y, f"FINAL SCORE: {score_content}", 20, 'white')

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
        button_label_id = draw_centered_text(canvas, button_x + button_width / 2, text_y, button_text, font_size, RESTART_BUTTON_TEXT_COLOR)


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


def create_bricks(canvas):
    """
    Creates the rows of bricks for the game.
    Returns a list of brick object IDs.
    """
    bricks = []
    
    # Define brick colors for each row
    # This ensures a consistent color pattern across rows
    row_colors = [
        BRICK_COLORS[0], BRICK_COLORS[0], # Red
        BRICK_COLORS[1], BRICK_COLORS[1], # Orange
        BRICK_COLORS[2], BRICK_COLORS[2], # Yellow
        BRICK_COLORS[3], BRICK_COLORS[3], # Green
        BRICK_COLORS[4], BRICK_COLORS[4]  # Blue
    ]

    for row in range(BRICK_ROWS):
        start_y = 50 + row * (BRICK_HEIGHT + BRICK_GAP)
        brick_color = row_colors[row % len(row_colors)] # Use modulo to cycle through colors if more rows than colors

        for col in range(BRICKS_PER_ROW):
            start_x = col * (BRICK_WIDTH + BRICK_GAP)
            brick = canvas.create_rectangle(
                start_x, start_y,
                start_x + BRICK_WIDTH, start_y + BRICK_HEIGHT,
                brick_color, brick_color # Fill and outline
            )
            bricks.append(brick)
    return bricks

def bouncing(canvas, ball_x, ball_y, change_x, change_y):
    """
    Handles ball bouncing off canvas walls.
    """
    if ball_x <= 0 or ball_x + BALL_RADIUS * 2 >= CANVAS_WIDTH:
        change_x = -change_x
    if ball_y <= 0:
        change_y = -change_y
    return change_x, change_y

def run_game(canvas):
    """
    Contains the main game logic for Breakout.
    Returns the final message and score when the game ends.
    """
    # Create bricks
    bricks = create_bricks(canvas)
    total_bricks = len(bricks)

    # Create paddle
    paddle_x = CANVAS_WIDTH / 2 - PADDLE_WIDTH / 2
    paddle = canvas.create_rectangle(paddle_x, PADDLE_Y, paddle_x + PADDLE_WIDTH, PADDLE_Y + PADDLE_HEIGHT, PADDLE_COLOR)

    # Create ball
    ball_x = CANVAS_WIDTH / 2 - BALL_RADIUS
    ball_y = CANVAS_HEIGHT / 2 - BALL_RADIUS
    ball = canvas.create_oval(ball_x, ball_y, ball_x + BALL_RADIUS * 2, ball_y + BALL_RADIUS * 2, BALL_COLOR)

    # Ball movement variables
    change_x = INITIAL_BALL_SPEED
    change_y = INITIAL_BALL_SPEED

    # Game state variables
    lives = 3
    points = 0
    points_text = draw_centered_text(canvas, CANVAS_WIDTH / 2, 15, f"{points} POINTS | LIVES: {lives}", 15, 'black')

    # Game loop
    while True:
        # Move ball
        ball_x += change_x
        ball_y += change_y
        canvas.moveto(ball, ball_x, ball_y)

        # Handle ball hitting bottom wall (lose a life)
        if ball_y + BALL_RADIUS * 2 >= CANVAS_HEIGHT:
            lives -= 1
            if lives == 0:
                # Game Over
                canvas.clear() # Clear all game elements
                return "GAME OVER!", points # Return message and score to main loop
            else:
                # Reset ball position
                ball_x = CANVAS_WIDTH / 2 - BALL_RADIUS
                ball_y = CANVAS_HEIGHT / 2 - BALL_RADIUS
                canvas.moveto(ball, ball_x, ball_y)
                # Update lives display
                canvas.change_text(points_text, f"{points} POINTS | LIVES: {lives}")
                time.sleep(1) # Pause briefly before next life

        # Handle ball bouncing off walls
        change_x, change_y = bouncing(canvas, ball_x, ball_y, change_x, change_y)

        # Move paddle with mouse
        mouse_x = canvas.get_mouse_x()
        # Clamp paddle to canvas bounds
        new_paddle_x = max(0, min(mouse_x - PADDLE_WIDTH / 2, CANVAS_WIDTH - PADDLE_WIDTH))
        canvas.moveto(paddle, new_paddle_x, PADDLE_Y)

        # Collision detection
        # Get all objects overlapping with the ball's current position
        colliding_list = canvas.find_overlapping(ball_x, ball_y, ball_x + BALL_RADIUS * 2, ball_y + BALL_RADIUS * 2)

        # Check for paddle collision
        if paddle in colliding_list:
            # Ensure ball is moving downwards before bouncing off paddle
            if change_y > 0:
                change_y = -change_y
                # Adjust ball position slightly to prevent sticking
                ball_y = PADDLE_Y - BALL_RADIUS * 2 - 1
                canvas.moveto(ball, ball_x, ball_y)

        # Check for brick collision
        hit_brick = False
        for obj_id in colliding_list:
            # Check if the object is a brick (not the paddle or ball itself)
            if obj_id != ball and obj_id != paddle and obj_id in bricks:
                canvas.delete(obj_id)
                bricks.remove(obj_id) # Remove from our list of active bricks
                points += 20
                total_bricks -= 1
                canvas.change_text(points_text, f"{points} POINTS | LIVES: {lives}")
                hit_brick = True
                break # Only hit one brick per collision for simplicity

        if hit_brick:
            change_y = -change_y # Bounce off the brick

            # Increase speed based on remaining bricks
            if total_bricks <= 80 and total_bricks > 60:
                change_x = (1.2 * INITIAL_BALL_SPEED) * (1 if change_x > 0 else -1)
                change_y = (1.2 * INITIAL_BALL_SPEED) * (1 if change_y > 0 else -1)
            elif total_bricks <= 60 and total_bricks > 40:
                change_x = (1.4 * INITIAL_BALL_SPEED) * (1 if change_x > 0 else -1)
                change_y = (1.4 * INITIAL_BALL_SPEED) * (1 if change_y > 0 else -1)
            elif total_bricks <= 40:
                change_x = (1.6 * INITIAL_BALL_SPEED) * (1 if change_x > 0 else -1)
                change_y = (1.6 * INITIAL_BALL_SPEED) * (1 if change_y > 0 else -1)

            if total_bricks == 0:
                # All bricks cleared - Player Wins!
                canvas.clear() # Clear all game elements
                return "CONGRATULATIONS! YOU WON!", points # Return message and score

        time.sleep(GAME_DELAY)

def main():
    """
    Main function to initialize the canvas and manage the game flow.
    """
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    # Outer loop to allow restarting the game
    while True:
        # Initial draw of title and button for the first iteration
        game_title_text = draw_centered_text(canvas, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 100, "🌌 Cosmic Breakout 🌌", 36, "white", font='Impact')
        button_rect, button_label, shadow_rect, highlight_rect, button_bounds = draw_start_button(canvas)
        
        # Wait for the button to be clicked, passing initial elements to be managed
        wait_for_start_button_click(canvas, button_rect, shadow_rect, highlight_rect, button_label, button_bounds, game_title_text)

        # Once the button is clicked, the game starts
        final_message, final_score = run_game(canvas)

        # After the game ends, prepare restart screen data
        restart_screen_data = draw_restart_screen_and_button(canvas, final_message, final_score)
        
        # Wait for restart button click, passing the data to redraw elements
        wait_for_restart_button_click(canvas, restart_screen_data)
        
        # The loop will continue, drawing the start screen again for a new game
        # The canvas is cleared by the restart button click handler before returning here.

if __name__ == '__main__':
    main()
