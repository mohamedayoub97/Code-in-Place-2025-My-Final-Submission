from graphics import Canvas
import random
import time

# MockCanvas class is used as a fallback if the real graphics.Canvas
# is not available or fails to initialize. It simulates Canvas behavior
# without actual graphical output, allowing the game logic to run for testing.
class MockCanvas:
    def __init__(self, width, height):
        print(f"WARNING: Initializing MockCanvas (width={width}, height={height}). No graphical output will be displayed.")
        self._objects = {}
        self._next_id = 0
        self._mouse_clicks = []
        self._key_presses = []

    def _get_new_id(self):
        self._next_id += 1
        return self._next_id

    def create_rectangle(self, x1, y1, x2, y2, color=None, outline=None):
        obj_id = self._get_new_id()
        self._objects[obj_id] = {'type': 'rectangle', 'coords': [x1, y1, x2, y2], 'color': color, 'outline': outline, 'hidden': False}
        return obj_id

    def create_oval(self, x1, y1, x2, y2, color=None, outline=None):
        obj_id = self._get_new_id()
        self._objects[obj_id] = {'type': 'oval', 'coords': [x1, y1, x2, y2], 'color': color, 'outline': outline, 'hidden': False}
        return obj_id

    def create_line(self, x1, y1, x2, y2, color=None):
        obj_id = self._get_new_id()
        self._objects[obj_id] = {'type': 'line', 'coords': [x1, y1, x2, y2], 'color': color, 'hidden': False}
        return obj_id

    # MockCanvas.create_text matches graphics.Canvas positional arguments
    def create_text(self, x, y, text, font, font_size, color):
        obj_id = self._get_new_id()
        self._objects[obj_id] = {'type': 'text', 'coords': [x, y], 'text': text, 'font': font, 'font_size': font_size, 'color': color, 'hidden': False}
        return obj_id

    def create_image(self, x, y, filename):
        obj_id = self._get_new_id()
        self._objects[obj_id] = {'type': 'image', 'coords': [x, y], 'filename': filename, 'hidden': False}
        return obj_id

    def create_image_with_size(self, x, y, width, height, filename):
        obj_id = self._get_new_id()
        self._objects[obj_id] = {'type': 'image_sized', 'coords': [x, y], 'width': width, 'height': height, 'filename': filename, 'hidden': False}
        return obj_id

    def create_polygon(self, *args, color=None, outline=None):
        coords = list(args)
        obj_id = self._get_new_id()
        self._objects[obj_id] = {'type': 'polygon', 'coords': coords, 'color': color, 'outline': outline, 'hidden': False}
        return obj_id

    def move(self, objectId, dx, dy):
        if objectId in self._objects:
            obj = self._objects[objectId]
            if 'coords' in obj and len(obj['coords']) >= 2:
                obj['coords'][0] += dx
                obj['coords'][1] += dy
                if obj['type'] in ['rectangle', 'oval', 'line', 'image_sized']:
                    for i in range(2, len(obj['coords']), 2):
                        obj['coords'][i] += dx
                        obj['coords'][i+1] += dy

    def moveto(self, objectId, new_x, new_y):
        if objectId in self._objects:
            obj = self._objects[objectId]
            if 'coords' in obj and len(obj['coords']) >= 2:
                dx = new_x - obj['coords'][0]
                dy = new_y - obj['coords'][1]
                obj['coords'][0] = new_x
                obj['coords'][1] = new_y
                if obj['type'] in ['rectangle', 'oval', 'line', 'image_sized']:
                    for i in range(2, len(obj['coords']), 2):
                        obj['coords'][i] += dx
                        obj['coords'][i+1] += dy

    def delete(self, objectId):
        if objectId in self._objects:
            del self._objects[objectId]

    def change_text(self, objectId, new_text):
        if objectId in self._objects and self._objects[objectId]['type'] == 'text':
            self._objects[objectId]['text'] = new_text

    def get_mouse_x(self):
        return 0

    def get_mouse_y(self):
        return 0

    def get_last_click(self):
        return None

    def get_new_mouse_clicks(self):
        # In MockCanvas, return a list of dictionaries mirroring the expected behavior of real Canvas clicks.
        # This can be expanded to allow external tests to inject clicks into _mouse_clicks.
        clicks = self._mouse_clicks
        self._mouse_clicks = []
        return clicks

    def get_last_key_press(self):
        return None

    def get_new_key_presses(self):
        keys = self._key_presses
        self._key_presses = []
        return keys

    def find_overlapping(self, x1, y1, x2, y2):
        return []

    def clear(self):
        self._objects = {}
        self._next_id = 0

    def get_left_x(self, obj_id):
        if obj_id in self._objects and 'coords' in self._objects[obj_id]:
            return self._objects[obj_id]['coords'][0]
        return 0

    def get_top_y(self, obj_id):
        if obj_id in self._objects and 'coords' in self._objects[obj_id]:
            return self._objects[obj_id]['coords'][1]
        return 0

    def get_object_width(self, obj_id):
        if obj_id in self._objects and 'width' in self._objects[obj_id]:
            return self._objects[obj_id]['width']
        if obj_id in self._objects and 'coords' in self._objects[obj_id] and len(self._objects[obj_id]['coords']) >= 4:
            return self._objects[obj_id]['coords'][2] - self._objects[obj_id]['coords'][0]
        return 0

    def get_object_height(self, obj_id):
        if obj_id in self._objects and 'height' in self._objects[obj_id]:
            return self._objects[obj_id]['height']
        if obj_id in self._objects and 'coords' in self._objects[obj_id] and len(self._objects[obj_id]['coords']) >= 4:
            return self._objects[obj_id]['coords'][3] - self._objects[obj_id]['coords'][1]
        return 0

    def set_color(self, objectId, color):
        if objectId in self._objects:
            self._objects[objectId]['color'] = color

    def set_outline_color(self, objectId, color):
        if objectId in self._objects:
            self._objects[objectId]['outline'] = color

    def wait_for_click(self):
        # Mocking a click event as a dictionary (or list) for testing purposes
        return {'x': 0, 'y': 0}

    def coords(self, objectId):
        if objectId in self._objects and 'coords' in self._objects[objectId]:
            return self._objects[objectId]['coords']
        return []

    def update(self):
        pass

# Function to estimate text width for proper centering
def estimate_text_width(text, font_size):
    return font_size * 0.5 * len(text)

# Function to draw centered text
def draw_centered_text(canvas, center_x, y, text, font, font_size, color):
    text_width = estimate_text_width(text, font_size)
    true_x = center_x - text_width / 2
    return canvas.create_text(
        true_x, y,
        text,
        font=font,
        font_size=font_size,
        color=color
    )

def main():
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 600

    canvas = None
    try:
        # Attempt to initialize the real Canvas
        canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        print("Canvas initialized successfully.")
    except Exception as e:
        # Fallback to MockCanvas if real Canvas fails
        print(f"ERROR: Could not initialize graphics.Canvas. Details: {e}")
        print("Attempting to run game with MockCanvas. No visual output will be available.")
        canvas = MockCanvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        
    # If canvas is still None after attempts, exit.
    if canvas is None:
        print("FATAL ERROR: No canvas object could be initialized. Game cannot run.")
        return

    # Game state and UI elements will be stored in a dictionary
    game_state = {
        'total_score': 0,
        'current_round_points': 5,
        'hints_used': 0,
        'max_hints': 3,
        'current_animal': "",
        'current_guess': "",
        'game_state_status': "starting_screen", # Initial state is starting screen
        'animals': {
            "LIZARD": {
                "image": "Lizard.jpg",
                "hint": "Lizards vary widely in size, color, and species variety."
            },
            "ELEPHANT": {
                "image": "Elephant.jpg",
                "hint": "The largest land mammal with a long trunk and big ears."
            },
            "TIGER": {
                "image": "Tiger.jpg",
                "hint": "A large striped wild cat that is also an excellent hunter."
            },
            "DOLPHIN": {
                "image": "Dolphin.jpg",
                "hint": "An intelligent marine mammal that lives in the ocean."
            },
            "PENGUIN": {
                "image": "Penguin.jpg",
                "hint": "A flightless bird known for living in cold climates and waddling."
            },
            "GIRAFFE": {
                "image": "Giraffe.jpg",
                "hint": "The tallest mammal, known for its long neck and spotted coat."
            },
            "ZEBRA": {
                "image": "Zebra.jpg",
                "hint": "An African equidae known for its distinctive black and white striped coats."
            },
            "KANGAROO": {
                "image": "Kangaroo.jpg",
                "hint": "A large marsupial native to Australia, known for hopping."
            },
            "BEAR": {
                "image": "Bear.jpg",
                "hint": "A large, furry mammal, some species hibernate in winter."
            },
            "SNAKE": {
                "image": "Snake.jpg",
                "hint": "A legless reptile, some are venomous, others constrict their prey."
            },
            "OWL": {
                "image": "Owl.jpg",
                "hint": "A nocturnal bird of prey with excellent eyesight and hearing."
            },
            "MONKEY": {
                "image": "Monkey.jpg",
                "hint": "A primate known for swinging through trees and its playful nature."
            },
            "SHARK": {
                "image": "Shark.jpg",
                "hint": "A powerful fish with a cartilaginous skeleton, found in oceans worldwide."
            },
            "FOX": {
                "image": "Fox.jpg",
                "hint": "A small to medium-sized omnivorous mammal belonging to the Canidae family, known for its bushy tail."
            },
            "CROCODILE": {
                "image": "Crocodile.jpg",
                "hint": "A large predatory amphibious reptile with powerful jaws, found in tropical regions."
            },
            "KOALA": {
                "image": "Koala.jpg",
                "hint": "A small, tree-dwelling marsupial native to Australia, known for eating eucalyptus leaves."
            },
            "HIPPOPOTAMUS": {
                "image": "Hippopotamus.jpg",
                "hint": "A large, semi-aquatic mammal native to Africa, known for its enormous mouth."
            }
        },
        'ui_elements': {},
        'keyboard_buttons': {},
        'grid_squares': [],
        'background_rect_ids': [], # Store IDs of background rectangles
        'background_oval_ids': [], # Store IDs of background ovals
        'last_color_rotate_time': time.time() # Track time for rotation
    }

    def create_game_ui(canvas_obj, game_state_dict):
        """Creates all the main game UI elements."""
        game_state_dict['ui_elements']['container'] = canvas_obj.create_rectangle(
            10, 10, CANVAS_WIDTH-10, CANVAS_HEIGHT-10, "white", "lightgray"
        )
        
        game_state_dict['ui_elements']['title'] = draw_centered_text(
            canvas_obj, CANVAS_WIDTH//2, 30, "Animal Guessing Game",
            "Arial", 20, "black"
        )
        game_state_dict['ui_elements']['total_score'] = draw_centered_text(
            canvas_obj, CANVAS_WIDTH//2, 60, f"Total Score: {game_state['total_score']}",
            "Arial", 14, "black"
        )
        game_state_dict['ui_elements']['round_points'] = draw_centered_text(
            canvas_obj, CANVAS_WIDTH//2, 82, f"Current Round Points: {game_state['current_round_points']}",
            "Arial", 12, "black"
        )
        game_state_dict['ui_elements']['image_area'] = canvas_obj.create_rectangle(
            30, 105, CANVAS_WIDTH-30, 225, "lightblue"
        )

        # Initialize animal image (will be replaced by start_new_round)
        try:
            animal_data = game_state_dict['animals']["LIZARD"] # Placeholder animal
            game_state_dict['ui_elements']['animal_image'] = canvas_obj.create_image_with_size(
                30, 105, CANVAS_WIDTH-60, 120, animal_data['image']
            )
        except Exception:
            game_state_dict['ui_elements']['animal_image'] = canvas_obj.create_rectangle(
                30, 105, CANVAS_WIDTH-30, 225, "lightgray"
            )
            draw_centered_text(
                canvas_obj, CANVAS_WIDTH//2, 165, f"[IMAGE PLACEHOLDER]",
                "Arial", 14, "black"
            )

        create_image_grid(canvas_obj, game_state_dict) # Create the initial multicolor grid

        game_state_dict['ui_elements']['guess_area'] = canvas_obj.create_rectangle(
            30, 235, CANVAS_WIDTH-30, 265, "lightyellow"
        )
        game_state_dict['ui_elements']['guess_text'] = draw_centered_text(
            canvas_obj, CANVAS_WIDTH//2-10, 240, "- - - - -",
            "Arial", 18, "black"
        )
        game_state_dict['ui_elements']['instruction'] = draw_centered_text(
            canvas_obj, CANVAS_WIDTH//2+5, 275, "Guess the animal",
            "Arialbold", 14, "black"
        )
        game_state_dict['ui_elements']['input_area'] = canvas_obj.create_rectangle(
            30, 295, CANVAS_WIDTH-30, 320, "white", "gray"
        )
        game_state_dict['ui_elements']['input_text'] = draw_centered_text(
            canvas_obj, CANVAS_WIDTH//2+12, 303, "Type your full guess here",
            "Arialbold", 11, "gray"
        )
        canvas_obj.create_rectangle(
            53, 333, CANVAS_WIDTH-47, 358, "#333333", "#333333"
        )
        game_state_dict['ui_elements']['guess_button'] = canvas_obj.create_rectangle(
            50, 330, CANVAS_WIDTH-50, 355, "#4A90E2", "#2C5282"
        )
        game_state_dict['ui_elements']['guess_button_text'] = draw_centered_text(
            canvas_obj, CANVAS_WIDTH//2, 337, "Guess Word",
            "Arialbold", 14, "white"
        )

        create_keyboard(canvas_obj, game_state_dict)

        canvas_obj.create_rectangle(
            53, 523, 153, 548, "#333333", "#333333"
        )
        game_state_dict['ui_elements']['hint_button'] = canvas_obj.create_rectangle(
            50, 520, 150, 545, "green", "darkgreen"
        )
        game_state_dict['ui_elements']['hint_button_text'] = draw_centered_text(
            canvas_obj, 112, 528, f"Get Hint ({game_state['max_hints'] - game_state['hints_used']} left)",
            "Arialbold", 12, "white"
        )

        canvas_obj.create_rectangle(
            253, 523, 353, 548, "#333333", "#333333"
        )
        game_state_dict['ui_elements']['give_up_button'] = canvas_obj.create_rectangle(
            250, 520, 350, 545, "red", "darkred"
        )
        game_state_dict['ui_elements']['give_up_button_text'] = draw_centered_text(
            canvas_obj, 300, 528, "Give Up",
            "Arialbold", 12, "white"
        )
        # The standalone delete button creation was removed from here.

    def create_image_grid(canvas_obj, game_state_dict):
        """Create a 3x3 grid to cover the image with multicolor boxes."""
        game_state_dict['grid_squares'] = []
        grid_width = (CANVAS_WIDTH - 60) // 3
        grid_height = 120 // 3

        # Define a list of vibrant colors for the grid squares
        colors = [
            "red", "orange", "yellow", "green", "blue", "purple", "pink",
            "brown", "cyan", "magenta", "lime", "gold", "teal", "indigo"
        ]

        for row in range(3):
            for col in range(3):
                x1 = 30 + col * grid_width
                y1 = 105 + row * grid_height
                x2 = x1 + grid_width
                y2 = y1 + grid_height

                # Choose a random color for each square
                fill_color = random.choice(colors)
                outline_color = "darkgray" # A consistent outline for contrast

                square = canvas_obj.create_rectangle(
                    x1, y1, x2, y2, fill_color, outline_color
                )
                game_state_dict['grid_squares'].append(square)

    def create_keyboard(canvas_obj, game_state_dict):
        """Create virtual keyboard with proper centering"""
        keys = [
            ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            ['H', 'I', 'J', 'K', 'L', 'M', 'N'],
            ['O', 'P', 'Q', 'R', 'S', 'T', 'U'],
            ['V', 'W', 'X', 'Y', 'Z', '🗑️'] # Changed 'DEL' to '🗑️'
        ]

        button_width = 35
        button_height = 25
        start_y = 365

        for row_idx, row in enumerate(keys):
            row_width = len(row) * button_width
            start_x = (CANVAS_WIDTH - row_width) // 2

            for col_idx, key in enumerate(row):
                x1 = start_x + col_idx * button_width
                y1 = start_y + row_idx * 28
                x2 = x1 + button_width - 2
                y2 = y1 + button_height

                shadow = canvas_obj.create_rectangle(
                    x1 + 2, y1 + 2, x2 + 2, y2 + 2, "#333333", "#333333"
                )
                
                # Special color for trash can emoji key
                if key == '🗑️':
                    button = canvas_obj.create_rectangle(x1, y1, x2, y2, "red", "darkred")
                else:
                    button = canvas_obj.create_rectangle(x1, y1, x2, y2, "blue", "darkblue")
                
                text = canvas_obj.create_text(
                    (x1 + x2) // 2 - 5, (y1 + y2) // 2 - 5, key, # Adjust positioning if emoji looks off
                    "Arial", 12, "white"
                )

                game_state_dict['keyboard_buttons'][key] = {
                    'button': button,
                    'text': text,
                    'shadow': shadow,
                    'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2
                }

    def update_guess_display(canvas_obj, game_state_dict):
        """Update the guess display with current progress (blanks/revealed letters)"""
        display_text = ""
        for i, letter in enumerate(game_state_dict['current_animal']):
            if i < len(game_state_dict['current_guess']) and game_state_dict['current_guess'][i].upper() == letter:
                display_text += letter + " "
            else:
                display_text += "- "
        canvas_obj.change_text(game_state_dict['ui_elements']['guess_text'], display_text.strip())

    def update_input_display(canvas_obj, game_state_dict):
        """Updates the text in the 'Type your full guess here' box."""
        if game_state_dict['current_guess']:
            canvas_obj.change_text(game_state_dict['ui_elements']['input_text'], game_state_dict['current_guess'])
            canvas_obj.set_color(game_state_dict['ui_elements']['input_text'], "black") # Change color to black when typing
        else:
            canvas_obj.change_text(game_state_dict['ui_elements']['input_text'], "Type your full guess here")
            canvas_obj.set_color(game_state_dict['ui_elements']['input_text'], "gray") # Keep placeholder gray

    def update_score_display(canvas_obj, game_state_dict):
        """Update score displays"""
        canvas_obj.change_text(
            game_state_dict['ui_elements']['total_score'],
            f"Total Score: {game_state['total_score']}"
        )
        canvas_obj.change_text(
            game_state_dict['ui_elements']['round_points'],
            f"Current Round Points: {game_state['current_round_points']}"
        )
        canvas_obj.change_text(
            game_state_dict['ui_elements']['hint_button_text'],
            f"Get Hint ({game_state['max_hints'] - game_state['hints_used']} left)"
        )

    def reveal_grid_square(canvas_obj, game_state_dict):
        """Reveal one random grid square by deleting it"""
        if game_state_dict['grid_squares']: # Check if there are any squares left
            square_to_reveal = random.choice(game_state_dict['grid_squares'])
            canvas_obj.delete(square_to_reveal) # Delete the graphical object
            game_state_dict['grid_squares'].remove(square_to_reveal) # Remove from our tracking list
        else:
            pass # No squares left to reveal

    def show_correct_answer(canvas_obj, game_state_dict):
        """Show the correct answer screen"""
        # Delete all remaining grid squares
        # Iterate over a copy because we're modifying the list during iteration
        for square in list(game_state_dict['grid_squares']):
            canvas_obj.delete(square)
        game_state_dict['grid_squares'] = [] # Ensure the list is empty after all are deleted

        canvas_obj.change_text(game_state_dict['ui_elements']['guess_text'], game_state_dict['current_animal'])
        
        # Check game_state_status to adjust instruction text
        if game_state_dict['game_state_status'] == "correct":
            canvas_obj.change_text(
                game_state_dict['ui_elements']['instruction'],
                f"Correct 🥳 You guessed: {game_state_dict['current_animal']}. You earned {game_state_dict['current_round_points']} points!"
            )
        else: # This handles the 'give up' scenario or incorrect full guess if we re-add that logic
            canvas_obj.change_text(
                game_state_dict['ui_elements']['instruction'],
                f"The correct answer was: {game_state_dict['current_animal']}."
            )
            
        # Create detail text centered horizontally
        game_state_dict['ui_elements']['detail_text'] = draw_centered_text(
            canvas_obj, CANVAS_WIDTH//2+25, 295, f"Detail: {game_state_dict['animals'][game_state_dict['current_animal']]['hint']}",
            "Arialbolditalic", 10, "red"
        )

        # Ensure any old play_again elements are deleted from canvas and dict before creating new ones
        if 'play_again_shadow' in game_state_dict['ui_elements'] and game_state_dict['ui_elements']['play_again_shadow'] is not None:
            canvas_obj.delete(game_state_dict['ui_elements']['play_again_shadow'])
            game_state_dict['ui_elements']['play_again_shadow'] = None
        if 'play_again' in game_state_dict['ui_elements'] and game_state_dict['ui_elements']['play_again'] is not None:
            canvas_obj.delete(game_state_dict['ui_elements']['play_again'])
            game_state_dict['ui_elements']['play_again'] = None
        if 'play_again_text' in game_state_dict['ui_elements'] and game_state_dict['ui_elements']['play_again_text'] is not None:
            canvas_obj.delete(game_state_dict['ui_elements']['play_again_text'])
            game_state_dict['ui_elements']['play_again_text'] = None

        # Create play again button with shadow - centered horizontally
        button_width = 100
        button_height = 25
        button_x1 = (CANVAS_WIDTH - button_width) // 2
        button_y1 = 315
        button_x2 = button_x1 + button_width
        button_y2 = button_y1 + button_height

        # Create shadow
        game_state_dict['ui_elements']['play_again_shadow'] = canvas_obj.create_rectangle(
            button_x1 + 3, button_y1 + 3, button_x2 + 3, button_y2 + 3, "#333333", "#333333"
        )
        
        # Create button
        game_state_dict['ui_elements']['play_again'] = canvas_obj.create_rectangle(
            button_x1, button_y1, button_x2, button_y2, "purple", "darkmagenta"
        )
        
        # Create button text centered in the button
        game_state_dict['ui_elements']['play_again_text'] = draw_centered_text(
            canvas_obj, CANVAS_WIDTH//2, button_y1 + button_height//2-5, "Play Again",
            "Arial", 12, "white"
        )

        update_score_display(canvas_obj, game_state_dict)

    def give_hint(canvas_obj, game_state_dict):
        """Provide a hint by revealing a grid square"""
        if game_state_dict['hints_used'] < game_state_dict['max_hints'] and game_state_dict['game_state_status'] == "playing":
            game_state_dict['hints_used'] += 1
            game_state_dict['current_round_points'] = max(1, game_state_dict['current_round_points'] - 1)
            reveal_grid_square(canvas_obj, game_state_dict)
            update_score_display(canvas_obj, game_state_dict)

    def give_up(canvas_obj, game_state_dict):
        """Give up the current round"""
        game_state_dict['current_round_points'] = 0
        game_state_dict['game_state_status'] = "given_up" # New status for explicit give up
        show_correct_answer(canvas_obj, game_state_dict)

    def add_letter_to_guess(canvas_obj, game_state_dict, letter):
        """Add a letter to the current guess"""
        # Allow adding letters only up to the length of the current animal name
        if len(game_state_dict['current_guess']) < len(game_state_dict['current_animal']):
            game_state_dict['current_guess'] += letter
            update_guess_display(canvas_obj, game_state_dict)
            update_input_display(canvas_obj, game_state_dict) # Update the input box

            # Change keyboard button color to indicate it's used for the current guess
            if letter in game_state_dict['keyboard_buttons']:
                canvas_obj.set_color(game_state_dict['keyboard_buttons'][letter]['button'], "gray")

    def remove_last_letter_from_guess(canvas_obj, game_state_dict):
        """Removes the last letter from the current guess."""
        if game_state_dict['current_guess']:
            last_letter_removed = game_state_dict['current_guess'][-1]
            game_state_dict['current_guess'] = game_state_dict['current_guess'][:-1]
            update_guess_display(canvas_obj, game_state_dict)
            update_input_display(canvas_obj, game_state_dict)
            # Reset color of the key button if it was the last one removed
            if last_letter_removed in game_state_dict['keyboard_buttons']:
                # The '🗑️' key should retain its red color.
                if last_letter_removed == '🗑️':
                    canvas_obj.set_color(game_state_dict['keyboard_buttons']['🗑️']['button'], "red")
                else:
                    canvas_obj.set_color(game_state_dict['keyboard_buttons'][last_letter_removed]['button'], "blue")


    def cleanup_correct_screen(canvas_obj, game_state_dict):
        """Clean up the correct answer screen elements"""
        if 'detail_text' in game_state_dict['ui_elements'] and game_state_dict['ui_elements']['detail_text'] is not None:
            canvas_obj.delete(game_state_dict['ui_elements']['detail_text'])
            game_state_dict['ui_elements']['detail_text'] = None # Set to None after deletion

        if 'play_again_shadow' in game_state_dict['ui_elements'] and game_state_dict['ui_elements']['play_again_shadow'] is not None:
            canvas_obj.delete(game_state_dict['ui_elements']['play_again_shadow'])
            game_state_dict['ui_elements']['play_again_shadow'] = None # Set to None after deletion

        if 'play_again' in game_state_dict['ui_elements'] and game_state_dict['ui_elements']['play_again'] is not None:
            canvas_obj.delete(game_state_dict['ui_elements']['play_again'])
            game_state_dict['ui_elements']['play_again'] = None # Set to None after deletion

        if 'play_again_text' in game_state_dict['ui_elements'] and game_state_dict['ui_elements']['play_again_text'] is not None:
            canvas_obj.delete(game_state_dict['ui_elements']['play_again_text'])
            game_state_dict['ui_elements']['play_again_text'] = None # Set to None after deletion

        canvas_obj.change_text(game_state_dict['ui_elements']['instruction'], "Guess the animal")

    def start_new_round(canvas_obj, game_state_dict):
        """Start a new round with a random animal"""
        game_state_dict['current_animal'] = random.choice(list(game_state_dict['animals'].keys()))
        game_state_dict['current_guess'] = ""
        game_state_dict['current_round_points'] = 5
        game_state_dict['hints_used'] = 0
        game_state_dict['game_state_status'] = "playing"

        # Delete existing image and recreate it for the new animal
        if 'animal_image' in game_state_dict['ui_elements']:
            canvas_obj.delete(game_state_dict['ui_elements']['animal_image'])

        try:
            animal_data = game_state_dict['animals'][game_state_dict['current_animal']]
            game_state_dict['ui_elements']['animal_image'] = canvas_obj.create_image_with_size(
                30, 105, CANVAS_WIDTH-60, 120, animal_data['image']
            )
        except Exception:
            # Fallback if image file is not found or graphics.Canvas doesn't support images
            game_state_dict['ui_elements']['animal_image'] = canvas_obj.create_rectangle(
                30, 105, CANVAS_WIDTH-30, 225, "lightgray"
            )
            draw_centered_text(
                canvas_obj, CANVAS_WIDTH//2, 165, f"[{game_state_dict['current_animal']} IMAGE]",
                "Arial", 14, "black"
            )

        # Recreate the grid squares with new random colors
        for square_id in list(game_state_dict['grid_squares']): # Iterate over a copy
            canvas_obj.delete(square_id) # Delete old squares
        game_state_dict['grid_squares'] = [] # Ensure list is empty before recreating
        create_image_grid(canvas_obj, game_state_dict) # Create new ones

        update_guess_display(canvas_obj, game_state_dict)
        update_input_display(canvas_obj, game_state_dict) # Reset input box for new round
        update_score_display(canvas_obj, game_state_dict)

        # Reset keyboard button colors
        for key_data in game_state_dict['keyboard_buttons'].values():
            canvas_obj.set_color(key_data['button'], "blue")
        # Ensure '🗑️' key also resets to red
        if '🗑️' in game_state_dict['keyboard_buttons']:
            canvas_obj.set_color(game_state_dict['keyboard_buttons']['🗑️']['button'], "red")


    def handle_guess(canvas_obj, game_state_dict, guess):
        """Handle a full word guess - check for correctness"""
        if guess.upper() == game_state_dict['current_animal']:
            game_state_dict['total_score'] += game_state_dict['current_round_points']
            game_state_dict['game_state_status'] = "correct"
            show_correct_answer(canvas_obj, game_state_dict)
        else:
            game_state_dict['current_round_points'] = max(0, game_state_dict['current_round_points'] - 1) # Deduct points for incorrect guess
            game_state_dict['current_guess'] = "" # Clear guess for incorrect attempt
            canvas_obj.change_text(game_state_dict['ui_elements']['instruction'], "Incorrect guess! Try again or get a hint.")
            update_input_display(canvas_obj, game_state_dict) # Reset input box
            update_score_display(canvas_obj, game_state_dict)
            # Reset keyboard button colors to allow re-typing
            for key_data in game_state_dict['keyboard_buttons'].values():
                canvas_obj.set_color(key_data['button'], "blue")
            # Ensure '🗑️' key resets its color too
            if '🗑️' in game_state_dict['keyboard_buttons']:
                canvas_obj.set_color(game_state_dict['keyboard_buttons']['🗑️']['button'], "red")


    def handle_key_press(canvas_obj, game_state_dict, key):
        """Handle keyboard input"""
        if game_state_dict['game_state_status'] == "playing":
            if key.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                add_letter_to_guess(canvas_obj, game_state_dict, key.upper())
            elif key == 'BackSpace' or key == 'DEL': # 'DEL' key support for physical keyboard
                # Map physical 'DEL' key to the virtual '🗑️' action
                remove_last_letter_from_guess(canvas_obj, game_state_dict)
            elif key == 'Return' and game_state_dict['current_guess']:
                handle_guess(canvas_obj, game_state_dict, game_state_dict['current_guess'])

    def check_keyboard_click(canvas_obj, game_state_dict, x, y):
        """Check if a keyboard button was clicked"""
        for key, key_data in game_state_dict['keyboard_buttons'].items():
            if (key_data['x1'] <= x <= key_data['x2'] and
                key_data['y1'] <= y <= key_data['y2']):
                # Visual feedback for click
                canvas_obj.set_color(key_data['button'], "darkblue" if key != '🗑️' else "darkred")
                time.sleep(0.1)  # Brief delay for visual feedback
                canvas_obj.set_color(key_data['button'], "blue" if key != '🗑️' else "red")

                if key == '🗑️':
                    remove_last_letter_from_guess(canvas_obj, game_state_dict)
                else:
                    add_letter_to_guess(canvas_obj, game_state_dict, key)
                return True
        return False

    def check_button_click(canvas_obj, game_state_dict, x, y):
        """Check if any button was clicked and handle the interaction"""
        # Check guess button
        if (game_state_dict['game_state_status'] == "playing" and 
            50 <= x <= CANVAS_WIDTH-50 and 330 <= y <= 355): # Ensure playing state
            if game_state_dict['current_guess']:
                canvas_obj.set_color(game_state_dict['ui_elements']['guess_button'], "#357ABD")
                handle_guess(canvas_obj, game_state_dict, game_state_dict['current_guess'])
                time.sleep(0.1)
                canvas_obj.set_color(game_state_dict['ui_elements']['guess_button'], "#4A90E2")
                return True

        # Check hint button
        elif (game_state_dict['game_state_status'] == "playing" and
              50 <= x <= 150 and 520 <= y <= 545): # Ensure playing state
            canvas_obj.set_color(game_state_dict['ui_elements']['hint_button'], "darkgreen")
            give_hint(canvas_obj, game_state_dict)
            time.sleep(0.1)
            canvas_obj.set_color(game_state_dict['ui_elements']['hint_button'], "green")
            return True

        # Check give up button
        elif (game_state_dict['game_state_status'] == "playing" and
              250 <= x <= 350 and 520 <= y <= 545): # Ensure playing state
            canvas_obj.set_color(game_state_dict['ui_elements']['give_up_button'], "darkred")
            give_up(canvas_obj, game_state_dict)
            time.sleep(0.1)
            canvas_obj.set_color(game_state_dict['ui_elements']['give_up_button'], "red")
            return True
            
        # Check Play Again button
        elif (game_state_dict['game_state_status'] in ["correct", "given_up"]):
            
            button_x1 = (CANVAS_WIDTH - 100) // 2
            button_y1 = 315
            button_x2 = button_x1 + 100
            button_y2 = button_y1 + 25
            
            if (button_x1 <= x <= button_x2 and button_y1 <= y <= button_y2):
                # FIX: Add check for 'play_again' existence before attempting to set color
                if 'play_again' in game_state_dict['ui_elements'] and game_state_dict['ui_elements']['play_again'] is not None:
                    canvas_obj.set_color(game_state_dict['ui_elements']['play_again'], "darkmagenta")
                    
                cleanup_correct_screen(canvas_obj, game_state_dict)
                start_new_round(canvas_obj, game_state_dict)
                time.sleep(0.1)
                # FIX: Removed the second set_color here as the button is now deleted by cleanup_correct_screen
                return True

        # Check keyboard buttons (only if in playing state)
        elif game_state_dict['game_state_status'] == "playing":
            return check_keyboard_click(canvas_obj, game_state_dict, x, y)
        
        # Handle start button click (only if in starting_screen state)
        elif game_state_dict['game_state_status'] == "starting_screen":
            # Button properties
            button_x = 125
            button_y = 270 # Adjusted Y for better centering
            button_width = 150
            button_height = 60

            if (button_x <= x <= button_x + button_width and 
                button_y <= y <= button_y + button_height):
                
                # Delete start screen elements
                canvas_obj.delete(game_state_dict['ui_elements']['start_title'])
                canvas_obj.delete(game_state_dict['ui_elements']['start_subtitle'])
                canvas_obj.delete(game_state_dict['ui_elements']['start_shadow'])
                canvas_obj.delete(game_state_dict['ui_elements']['start_button_rect'])
                canvas_obj.delete(game_state_dict['ui_elements']['start_highlight_rect'])
                canvas_obj.delete(game_state_dict['ui_elements']['start_button_label'])
                
                # Create main game UI
                create_game_ui(canvas_obj, game_state_dict)
                start_new_round(canvas_obj, game_state_dict)
                game_state_dict['game_state_status'] = "playing"
                return True

        return False

    # Initial setup calls (formerly setup_game method)
    # Define a rich, elegant color palette for the background
    elegant_colors = [
        "#F0F8FF", "#E0FFFF", "#ADD8E6", "#B0E0E6", "#AFEEEE", "#87CEEB",
        "#6495ED", "#4682B4", "#5F9EA0", "#778899", "#B0C4DE", "#C0C0C0",
        "#FFB6C1", "#FFDAB9", "#FFE4B5", "#E6E6FA", "#DDA0DD", "#BA55D3",
        "#9370DB", "#6A5ACD", "#483D8B", "#98FB98", "#8FBC8F", "#20B2AA",
        "#00CED1", "#40E0D0", "#7B68EE", "#EE82EE", "#D8BFD8", "#DA70D6",
        "#FF69B4", "#FF1493", "#DB7093", "#C71585",
        "#FF00FF", "#00FFFF", "#FFFF00", "#FF4500", "#ADFF2F" # Added more vibrant colors
    ]

    # Create layered rectangles for a subtle vertical gradient effect
    num_bands = len(elegant_colors)
    band_height = CANVAS_HEIGHT / num_bands 

    for i in range(num_bands):
        y_start = i * band_height
        y_end = (i + 1) * band_height
        rect_id = canvas.create_rectangle( # Store the ID
            0, y_start, CANVAS_WIDTH, y_end,
            elegant_colors[i], # Passed as positional argument
            "" # Passed as positional argument
        )
        game_state['background_rect_ids'].append(rect_id) # Add to list

    # Expanded subtle_colors to include more vibrant and elegant hues for ovals
    oval_colors = [
        "#FFD700", "#FFA500", "#FF4500", "#FF6347", # Gold, Orange, Red-Orange, Tomato
        "#7FFF00", "#ADFF2F", "#00FF7F", "#3CB371", # Chartreuse, GreenYellow, SpringGreen, MediumSeaGreen
        "#00BFFF", "#1E90FF", "#4169E1", "#6A5ACD", # DeepSkyBlue, DodgerBlue, RoyalBlue, SlateBlue
        "#FF69B4", "#FF1493", "#C71585", "#DA70D6", # HotPink, DeepPink, MediumVioletRed, Orchid
        "#9400D3", "#8A2BE2", "#9932CC", "#BA55D3"  # DarkViolet, BlueViolet, DarkOrchid, MediumOrchid
    ]

    num_subtle_shapes = 150 # Increased number of subtle shapes for more density
    for _ in range(num_subtle_shapes):
        x = random.randint(0, CANVAS_WIDTH)
        y = random.randint(0, CANVAS_HEIGHT)
        size = random.randint(10, 35) # Slightly larger range for variety and visibility
        
        # Choose a random color for both outline and fill to make them more prominent
        fill_color = random.choice(oval_colors)
        outline_color = random.choice(oval_colors) # Can be different from fill for effect

        oval_id = canvas.create_oval( # Store the ID
            x - size, y - size, x + size, y + size,
            fill_color, # Passed as positional argument
            outline_color # Passed as positional argument
        )
        game_state['background_oval_ids'].append(oval_id) # Add to list

    # --- Start Screen Elements ---
    start_button_x = 125
    start_button_y = 270 # Adjusted Y for better centering
    start_button_width = 150
    start_button_height = 60
    start_button_color = "#4A90E2"
    start_button_hover_color = "#357ABD" # Not directly used in current click logic, but good to have
    start_button_text = "✨ Start Game ✨"
    start_font_size = 16 # Not directly used, but for context
    start_shadow_offset = 3

    game_state['ui_elements']['start_title'] = draw_centered_text(
        canvas, CANVAS_WIDTH / 2-12, 100, "🌟 Animal Guessing Game 🌟", "Arialbold", 30, "#FFFFFF"
    )
    game_state['ui_elements']['start_subtitle'] = draw_centered_text(
        canvas, CANVAS_WIDTH / 2, 135, "Can you guess the animal ?", "Arial", 16, "#4A5568"
    )

    # Shadow for start button
    game_state['ui_elements']['start_shadow'] = canvas.create_rectangle(
        start_button_x + start_shadow_offset, start_button_y + start_shadow_offset, 
        start_button_x + start_button_width + start_shadow_offset, start_button_y + start_button_height + start_shadow_offset,
        "#333333", "#333333"
    )
    
    # Start Button body
    game_state['ui_elements']['start_button_rect'] = canvas.create_rectangle(
        start_button_x, start_button_y, 
        start_button_x + start_button_width, start_button_y + start_button_height,
        start_button_color, "#2C5282"
    )
    
    # Highlight for start button
    game_state['ui_elements']['start_highlight_rect'] = canvas.create_rectangle(
        start_button_x + 2, start_button_y + 2, 
        start_button_x + start_button_width - 2, start_button_y + 15,
        "#87CEEB", "#87CEEB"
    )
    
    # Start Button text
    start_text_y = start_button_y + start_button_height / 2 - 18 / 2 # Using explicit font size for text centering
    game_state['ui_elements']['start_button_label'] = draw_centered_text(
        canvas, start_button_x + start_button_width / 2-5, start_text_y+5, 
        start_button_text, "Arialbold", 18, "white"
    )
    # --- End Start Screen Elements ---


    # Main game loop
    while True:
        #canvas.update() # Important to update the canvas to show changes
        time.sleep(0.01) # Small delay to prevent busy-waiting

        clicks = canvas.get_new_mouse_clicks()
        for click in clicks:
            # check_button_click handles both playing and starting_screen states
            # and internally checks for keyboard clicks if in playing state.
            check_button_click(canvas, game_state, click[0], click[1]) # Using integer indices for clicks

        key_presses = canvas.get_new_key_presses()
        for key_event in key_presses:
            # Only process key presses if game is playing
            if game_state['game_state_status'] == "playing":
                handle_key_press(canvas, game_state, key_event)
        
        # Continuously rotate grid colors (only if playing)
        current_time = time.time()
        if game_state['game_state_status'] != "starting_screen" and \
           current_time - game_state['last_color_rotate_time'] > 0.5:
            # Rotate elegant_colors list for background rectangles
            first_color = elegant_colors.pop(0)
            elegant_colors.append(first_color)

            # Apply new colors to background rectangles
            for i, rect_id in enumerate(game_state['background_rect_ids']):
                canvas.set_color(rect_id, elegant_colors[i % len(elegant_colors)]) # Use modulo operator
            
            # Rotate oval_colors and apply to background ovals
            first_oval_color = oval_colors.pop(0)
            oval_colors.append(first_oval_color)
            for i, oval_id in enumerate(game_state['background_oval_ids']):
                canvas.set_color(oval_id, oval_colors[i % len(oval_colors)]) # Set fill color using modulo
                canvas.set_outline_color(oval_id, oval_colors[(i + 1) % len(oval_colors)]) # Set outline with a shifted color for effect using modulo

            game_state['last_color_rotate_time'] = current_time # Update last rotate time

if __name__ == '__main__':
    main()
