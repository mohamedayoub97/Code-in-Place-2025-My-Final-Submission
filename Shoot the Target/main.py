from graphics import Canvas
import random
import time

# --- CONSTANTS FOR GAME DESIGN ---
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
BULLSEYE_SIZE = 25
SHOT_SIZE = 8
CENTER_SCORE = 10
MIDDLE_SCORE = 5
OUTER_SCORE = 2
TIME_LIMIT = 35
TARGETS_START_MOVE = 3
INITIAL_SPEED = 7
MAX_SPEED = 35
SPEED_UP = 2

# --- UPDATED COLOR PALETTE FOR WHITE BACKGROUND ---
CANVAS_COLOR = "#FFFFFF" # White Background

# Premium Color Palette
COLOR_PALETTE = [ # Vibrant and premium colors for rotating bullseye
    "#E63946", # Imperial Red
    "#F4A261", # Sandy Brown
    "#2A9D8F", # Persian Green
    "#264653", # Charcoa
    "#FFBE0B", # Selective Yellow
    "#FB5607", # Orange Red
    "#FF006E", # Rose Red
    "#8338EC", # Blue Violet
    "#3A86FF", # Azure Blue
    "#C1121C", # Chilli Red
    "#0077B6", # Cerulean Blue
    "#00B4D8", # Pacific Blue
    "#90E0EF", # Sky Blue
    "#CAF0F8", # Light Cyan
    "#7B2CBF", # Amethyst
    "#6D6875", # Grape
    "#B5838D", # Old Rose
    "#E5989B", # Pastel Pink
    "#FFCDB2", # Peach
    "#A8DADC", # Powder Blue
    "#457B9D", # Steel Blue
    "#1D3557"  # Prussian Blue
]
SHOT_COLOR = "#4A4E69" # Darker Slate Gray for the shot, visible on white
HIT_FLASH_COLOR = "#E63946" # Bright Red flash on hit (Imperial Red from palette)
SCORE_TEXT_COLOR = "#2C3E50" # Dark Teal for score text
TIME_TEXT_COLOR = "#C0392B" # Dark Red for time warning
GAME_OVER_COLOR = "#C0392B" # Dark Red for Game Over message
SCORE_BOOST_COLOR = "#2ECC71" # Emerald Green for +score text

# --- ANIMATION AND FEEDBACK CONSTANTS ---
ANIMATION_DELAY = 0.05
FLASH_DURATION = 0.1
COLOR_ROTATION_SPEED = 5 # How many animation frames until colors change

# --- STAR CONSTANTS ---
NUM_STARS = 150
STAR_SIZE_MIN = 1
STAR_SIZE_MAX = 3
STAR_COLORS = ["#FFD700", "#FFFFFF", "#ADD8E6", "#FFC0CB", "#98FB98"] # Gold, White, Light Blue, Pink, Pale Green

# --- BUTTON CONSTANTS ---
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 70
BUTTON_TEXT_COLOR = "#FFFFFF" # White

# Specific color themes for buttons
START_BUTTON_COLORS = {
    'base': "#1abc9c",  # Emerald Green
    'outline': "#16a085", # Darker Emerald
    'shadow': "#0e665d", # Even Darker Emerald
    'highlight': "#48c9b0", # Lighter Emerald
    'pressed': "#16a085" # Color when clicked
}

RESTART_BUTTON_COLORS = {
    'base': "#9b59b6",  # Amethyst
    'outline': "#8e44ad", # Darker Amethyst
    'shadow': "#5e2d7a", # Even Darker Amethyst
    'highlight': "#b072da", # Lighter Amethyst
    'pressed': "#8e44ad" # Color when clicked
}


class BullseyeGame:
    def __init__(self):
        self.current_color_index = 0
        self.canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.game_state = "INITIALIZING" # New state to handle initial persistent background draw
        self.game_elements = {} # Dictionary to store game elements for easy clearing/deletion
        self.score = 0
        self.targets_hit = 0
        self.x_speed = INITIAL_SPEED
        self.y_speed = INITIAL_SPEED
        self.time_text = None
        self.score_text = None
        self.outer_circle = None
        self.middle_circle = None
        self.bullseye = None
        self.background_rect = None # Will store the persistent background rectangle

    def estimate_text_width(self, text, font_size):
        """Estimates the width of text for centering purposes."""
        return font_size * 0.5 * len(text) # Approximation

    def draw_centered_text(self, center_x, y, text, font_size, color):
        """Draws text centered horizontally on the canvas."""
        text_width = self.estimate_text_width(text, font_size)
        true_x = center_x - text_width / 2
        text_obj = self.canvas.create_text(
            true_x, y,
            text,
            font='Arial',
            font_size=font_size,
            color=color
        )
        return text_obj

    def draw_button(self, x, y, width, height, text, id_prefix, colors):
        """Draws a styled button with shadow, outline, and highlight."""
        shadow_offset = 5

        # Shadow (darker version of base color)
        shadow_rect = self.canvas.create_rectangle(
            x + shadow_offset, y + shadow_offset,
            x + width + shadow_offset, y + height + shadow_offset,
            colors['shadow'], colors['shadow']
        )

        # Button body (with outline)
        button_rect = self.canvas.create_rectangle(
            x, y,
            x + width, y + height,
            colors['base'], colors['outline'] # Fill, then border
        )

        # Highlight (top part for shine)
        highlight_rect = self.canvas.create_rectangle(
            x + 2, y + 2,
            x + width - 2, y + 15,
            colors['highlight'], colors['highlight']
        )

        # Button text - centered manually
        text_y = y + height / 2 - 0.5 * 16 # Approx font_size / 2 for vertical centering
        button_label = self.draw_centered_text(x + width / 2, text_y, text, 20, BUTTON_TEXT_COLOR) # Larger font for buttons

        # Store button elements for easy removal/color change
        self.game_elements[f"{id_prefix}_shadow"] = shadow_rect
        self.game_elements[f"{id_prefix}_rect"] = button_rect
        self.game_elements[f"{id_prefix}_highlight"] = highlight_rect # Store highlight
        self.game_elements[f"{id_prefix}_label"] = button_label
        self.game_elements[f"{id_prefix}_colors"] = colors # Store original colors

        return {
            'rect': button_rect,
            'label': button_label,
            'highlight': highlight_rect, # Return highlight too
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'colors': colors # Include colors in returned dict
        }

    def is_point_in_rect(self, point_x, point_y, rect_x, rect_y, rect_width, rect_height):
        """Checks if a point is within the bounds of a rectangle."""
        return (rect_x <= point_x <= rect_x + rect_width and
                rect_y <= point_y <= rect_y + rect_height)

    def draw_persistent_background(self):
        """Draws the background rectangle and stars once at the very beginning."""
        if self.background_rect is None: # Only draw if not already drawn
            self.background_rect = self.canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, color=CANVAS_COLOR)
            self.game_elements['background_rect'] = self.background_rect
            self.create_stars() # Stars are now part of the persistent background

    def draw_start_screen_elements(self):
        """Draws the title and start button on top of the persistent background."""
        # Game Title
        title = self.draw_centered_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 4, "🎯 Bullseye Blast 🎯", 48, SCORE_TEXT_COLOR)
        self.game_elements['title'] = title

        # Start Button
        start_button_x = (CANVAS_WIDTH - BUTTON_WIDTH) / 2
        start_button_y = CANVAS_HEIGHT / 2 - BUTTON_HEIGHT / 2
        self.game_elements['start_button'] = self.draw_button(
            start_button_x, start_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "🎮START GAME     ", "start", START_BUTTON_COLORS
        )

    def clear_start_screen_elements(self):
        """Clears ONLY the elements specific to the start screen (title and button)."""
        for key_suffix in ['title', 'shadow', 'rect', 'highlight', 'label', 'colors']: # Iterate over all parts of start button
            full_key = f"start_{key_suffix}" if key_suffix not in ['title'] else key_suffix
            if full_key in self.game_elements:
                if key_suffix != 'colors': # Don't try to delete the colors dict itself
                    self.canvas.delete(self.game_elements[full_key])
                del self.game_elements[full_key]

    def draw_playing_elements(self):
        """Draws the target, score, and time text for the playing state."""
        self.score = 0
        self.targets_hit = 0
        self.x_speed = INITIAL_SPEED
        self.y_speed = INITIAL_SPEED
        self.outer_circle, self.middle_circle, self.bullseye = self.create_target() # Creates and draws target
        self.game_elements['outer_circle'] = self.outer_circle # Store target elements
        self.game_elements['middle_circle'] = self.middle_circle
        self.game_elements['bullseye'] = self.bullseye

        self.time_text = self.canvas.create_text(15, 15, text='', color=TIME_TEXT_COLOR, font_size=20)
        self.score_text = self.canvas.create_text(CANVAS_WIDTH - 150, 15, text='Score: ' + str(self.score) + ' points', color=SCORE_TEXT_COLOR, font_size=20)
        self.game_elements['time_text'] = self.time_text # Store text elements
        self.game_elements['score_text'] = self.score_text

    def clear_playing_elements(self):
        """Clears elements specific to the playing screen (target, score/time text)."""
        for key in ['outer_circle', 'middle_circle', 'bullseye', 'time_text', 'score_text']:
            if key in self.game_elements and self.game_elements[key] is not None:
                self.canvas.delete(self.game_elements[key])
                del self.game_elements[key]

    def draw_game_over_screen_elements(self):
        """Draws game over elements (text and restart button) on top of persistent background."""
        game_over_title = self.draw_centered_text(
            CANVAS_WIDTH / 2-25, CANVAS_HEIGHT / 2 - 80,
            text='GAME OVER!',
            font_size=40,
            color=GAME_OVER_COLOR
        )
        final_score_text = self.draw_centered_text(
            CANVAS_WIDTH / 2+20, CANVAS_HEIGHT / 2 - 30,
            text='Final Score: ' + str(self.score) + ' points',
            font_size=30,
            color=SCORE_TEXT_COLOR
        )
        self.game_elements['game_over_title'] = game_over_title
        self.game_elements['final_score_text'] = final_score_text

        # Restart Button
        restart_button_x = (CANVAS_WIDTH - BUTTON_WIDTH) / 2
        restart_button_y = CANVAS_HEIGHT / 2 + 50
        self.game_elements['restart_button'] = self.draw_button(
            restart_button_x, restart_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, " 🔄RESTART     ", "restart", RESTART_BUTTON_COLORS
        )

    def clear_game_over_screen_elements(self):
        """Clears elements specific to the game over screen."""
        for key_suffix in ['title', 'text', 'shadow', 'rect', 'highlight', 'label', 'colors']:
            for prefix in ['game_over_', 'final_score_', 'restart_']: # Check prefixes for game over elements
                full_key = f"{prefix}{key_suffix}"
                if full_key in self.game_elements:
                    if key_suffix != 'colors':
                        self.canvas.delete(self.game_elements[full_key])
                    del self.game_elements[full_key]

    def main(self):
        # Initial setup: Draw persistent background and stars once
        self.draw_persistent_background()
        self.draw_start_screen_elements() # Draw start screen UI immediately
        self.game_state = "START_SCREEN"

        # Outer loop to manage game states (Start, Playing, Game Over)
        while True:
            click = self.canvas.get_last_click()

            if self.game_state == "START_SCREEN":
                if click:
                    start_button_info = self.game_elements.get('start_button')
                    if start_button_info and self.is_point_in_rect(click[0], click[1], start_button_info['x'], start_button_info['y'], start_button_info['width'], start_button_info['height']):
                        # Button press feedback
                        self.canvas.set_color(start_button_info['rect'], start_button_info['colors']['pressed'])
                        self.canvas.set_color(start_button_info['highlight'], start_button_info['colors']['pressed'])
                        time.sleep(0.1) # Brief visual feedback
                        self.clear_start_screen_elements() # Clear start screen elements
                        self.draw_playing_elements() # Draw playing elements
                        self.game_state = "PLAYING"
                time.sleep(ANIMATION_DELAY)

            elif self.game_state == "PLAYING":
                game_time_counter = TIME_LIMIT * (1 / ANIMATION_DELAY)

                while game_time_counter >= 0:
                    shot_object = None
                    temp_score_display = None
                    hit_result = 0

                    # Animate target movement
                    if self.targets_hit >= TARGETS_START_MOVE:
                        self.x_speed, self.y_speed = self.animate_target(self.outer_circle, self.middle_circle, self.bullseye, self.x_speed, self.y_speed)

                    self.current_color_index += 1
                    if self.current_color_index % COLOR_ROTATION_SPEED == 0:
                         self.rotate_target_colors(self.outer_circle, self.middle_circle, self.bullseye)

                    click = self.canvas.get_last_click()

                    if click:
                        shot_object, hit_result = self.shoot(click, self.outer_circle, self.middle_circle, self.bullseye)

                        if hit_result > 0:
                            self.score += hit_result
                            self.canvas.change_text(self.score_text, 'Score: ' + str(self.score) + ' points')

                            temp_score_display = self.canvas.create_text(
                                click[0], click[1] - 20,
                                text='+' + str(hit_result),
                                color=SCORE_BOOST_COLOR,
                                font_size=25
                            )
                            self.flash_target(self.outer_circle, self.middle_circle, self.bullseye, HIT_FLASH_COLOR)

                            if self.targets_hit >= TARGETS_START_MOVE:
                                self.x_speed = self.update_speed(self.x_speed)
                                self.y_speed = self.update_speed(self.y_speed)
                            self.targets_hit += 1

                    time.sleep(ANIMATION_DELAY)

                    remaining_seconds = int(game_time_counter * ANIMATION_DELAY)
                    self.canvas.change_text(self.time_text, 'Time: ' + str(remaining_seconds) + 's')

                    if remaining_seconds <= 10:
                        self.canvas.set_color(self.time_text, TIME_TEXT_COLOR)
                    else:
                        self.canvas.set_color(self.time_text, SCORE_TEXT_COLOR)

                    game_time_counter -= 1

                    if shot_object:
                        self.canvas.delete(shot_object)
                        if temp_score_display:
                            self.canvas.delete(temp_score_display)

                        if hit_result > 0:
                            # Delete old target and create new one
                            self.delete_target(self.outer_circle, self.middle_circle, self.bullseye)
                            self.outer_circle, self.middle_circle, self.bullseye = self.create_target()
                            # Update stored references for the new target
                            self.game_elements['outer_circle'] = self.outer_circle
                            self.game_elements['middle_circle'] = self.middle_circle
                            self.game_elements['bullseye'] = self.bullseye

                # Game over transition
                self.clear_playing_elements() # Clear playing elements before drawing game over screen
                self.draw_game_over_screen_elements() # Draw game over screen elements
                self.game_state = "GAME_OVER"


            elif self.game_state == "GAME_OVER":
                while True:
                    click = self.canvas.get_last_click()
                    if click:
                        restart_button_info = self.game_elements.get('restart_button')
                        if restart_button_info and self.is_point_in_rect(click[0], click[1], restart_button_info['x'], restart_button_info['y'], restart_button_info['width'], restart_button_info['height']):
                            # Button press feedback
                            self.canvas.set_color(restart_button_info['rect'], restart_button_info['colors']['pressed'])
                            self.canvas.set_color(restart_button_info['highlight'], restart_button_info['colors']['pressed'])
                            time.sleep(0.1)
                            self.clear_game_over_screen_elements() # Clear game over elements
                            self.draw_start_screen_elements() # Draw start screen elements again
                            self.game_state = "START_SCREEN" # Set state back to start screen
                            break # Exit the game over loop to restart main loop
                    time.sleep(ANIMATION_DELAY)


    # Creates a target in a random position, returns the three parts of the target.
    def create_target(self):
        # Use colors from the palette based on the current index
        c1 = COLOR_PALETTE[self.current_color_index % len(COLOR_PALETTE)]
        c2 = COLOR_PALETTE[(self.current_color_index + 1) % len(COLOR_PALETTE)]
        c3 = COLOR_PALETTE[(self.current_color_index + 2) % len(COLOR_PALETTE)]

        padding = 20
        target_x = random.randint(padding, CANVAS_WIDTH - BULLSEYE_SIZE * 5 - padding)
        target_y = random.randint(padding, CANVAS_HEIGHT - BULLSEYE_SIZE * 5 - padding)

        outer_circle = self.canvas.create_oval(target_x, target_y, target_x + BULLSEYE_SIZE * 5, target_y + BULLSEYE_SIZE * 5, c1)
        middle_circle = self.canvas.create_oval(target_x + BULLSEYE_SIZE, target_y + BULLSEYE_SIZE, target_x + BULLSEYE_SIZE * 4, target_y + BULLSEYE_SIZE * 4, c2)
        bullseye = self.canvas.create_oval(target_x + BULLSEYE_SIZE * 2, target_y + BULLSEYE_SIZE * 2, target_x + BULLSEYE_SIZE * 3, target_y + BULLSEYE_SIZE * 3, c3)
        return outer_circle, middle_circle, bullseye

    # Function to rotate the colors of the target rings
    def rotate_target_colors(self, outer_circle, middle_circle, bullseye):
        # Assign new colors to the existing target circles
        c1 = COLOR_PALETTE[self.current_color_index % len(COLOR_PALETTE)]
        c2 = COLOR_PALETTE[(self.current_color_index + 1) % len(COLOR_PALETTE)]
        c3 = COLOR_PALETTE[(self.current_color_index + 2) % len(COLOR_PALETTE)]

        self.canvas.set_color(outer_circle, c1)
        self.canvas.set_color(middle_circle, c2)
        self.canvas.set_color(bullseye, c3)
        # self.canvas.update() # Update is handled by main loop's self.canvas.update()

    # Creates tiny colorful stars on the canvas
    def create_stars(self):
        for _ in range(NUM_STARS):
            x = random.randint(0, CANVAS_WIDTH)
            y = random.randint(0, CANVAS_HEIGHT)
            size = random.randint(STAR_SIZE_MIN, STAR_SIZE_MAX)
            color = random.choice(STAR_COLORS)
            # Create a small oval for the star
            star = self.canvas.create_oval(x, y, x + size, y + size, color)
            self.game_elements[f'star_{_}'] = star # Store star objects for potential clearing

    def shoot(self, click, outer_circle, middle_circle, bullseye):
        result = 0
        shot = self.canvas.create_oval(click[0] - SHOT_SIZE / 2, click[1] - SHOT_SIZE / 2, click[0] + SHOT_SIZE / 2, click[1] + SHOT_SIZE / 2, color=SHOT_COLOR)

        overlapping_objects = self.canvas.find_overlapping(click[0], click[1], click[0], click[1])

        if bullseye in overlapping_objects:
            result = CENTER_SCORE
        elif middle_circle in overlapping_objects:
            result = MIDDLE_SCORE
        elif outer_circle in overlapping_objects:
            result = OUTER_SCORE

        return shot, result

    def animate_target(self, outer_circle, middle_circle, bullseye, x_speed, y_speed):
        target_x = self.canvas.get_left_x(outer_circle)
        target_y = self.canvas.get_top_y(outer_circle)

        buffer = 5
        if (target_x <= buffer) or (target_x + BULLSEYE_SIZE * 5 >= CANVAS_WIDTH - buffer):
            x_speed = -x_speed
        if (target_y <= buffer) or (target_y + BULLSEYE_SIZE * 5 >= CANVAS_HEIGHT - buffer):
            y_speed = -y_speed

        target_x += x_speed
        target_y += y_speed

        self.canvas.moveto(outer_circle, target_x, target_y)
        self.canvas.moveto(middle_circle, target_x + BULLSEYE_SIZE, target_y + BULLSEYE_SIZE)
        self.canvas.moveto(bullseye, target_x + BULLSEYE_SIZE * 2, target_y + BULLSEYE_SIZE * 2)
        return x_speed, y_speed

    def update_speed(self, speed):
        speed = abs(speed)
        if speed < MAX_SPEED:
            speed = speed + SPEED_UP
        speed = speed * random.choice([-1, 1])
        return speed

    def delete_target(self, outer_circle, middle_circle, bullseye):
        self.canvas.delete(outer_circle)
        self.canvas.delete(middle_circle)
        self.canvas.delete(bullseye)

    def flash_target(self, outer_circle, middle_circle, bullseye, flash_color):
        # Temporarily change colors to flash_color
        self.canvas.set_color(outer_circle, flash_color)
        self.canvas.set_color(middle_circle, flash_color)
        self.canvas.set_color(bullseye, flash_color)
        # self.canvas.update() # Re-enabled for immediate visual feedback of the flash
        time.sleep(FLASH_DURATION)

        # Restore the original colors using the instance variable
        self.canvas.set_color(outer_circle, COLOR_PALETTE[self.current_color_index % len(COLOR_PALETTE)])
        self.canvas.set_color(middle_circle, COLOR_PALETTE[(self.current_color_index + 1) % len(COLOR_PALETTE)])
        self.canvas.set_color(bullseye, COLOR_PALETTE[(self.current_color_index + 2) % len(COLOR_PALETTE)])
        # self.canvas.update() # Re-enabled for immediate visual feedback after flash

def main():
    game = BullseyeGame()
    game.main()

if __name__ == '__main__':
    main()
