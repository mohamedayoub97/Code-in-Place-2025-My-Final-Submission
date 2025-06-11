import os
import json
import random
import time
import math
from graphics import Canvas

# Constants
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
GRID_SIZE = 5
MAX_TRIES = 6
TILE_SIZE = 60
PADDING = 10

# Background Images
BACKGROUND_IMAGES = [
    "bg.jpg", "bgl.jpg", "bg2.jpg", "bg3.jpg", "bg5.jpg", "bg6.jpg", "bg7.jpg", "bg8.jpg",
    "bg9.jpg", "bg10.jpg", "bg11.jpg", "bgl2.jpg", "bg13.jpg", "bg14.jpg", "bg15.jpg", 
    "bg16.jpg", "bgl7.jpg", "bg18.jpg", "bg19.jpg", "bg20.jpg", "bg21.jpg", "bg22.jpg", 
    "bg23.jpg", "bg24.jpg", "bg25.jpg", "bg26.jpg"
]

# Load only existing images
AVAILABLE_IMAGES = [img for img in BACKGROUND_IMAGES if os.path.exists(img)]
bg_image = random.choice(AVAILABLE_IMAGES) if AVAILABLE_IMAGES else None

def load_words_from_json(filename="words.txt"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return [entry["word"].lower() for entry in data if len(entry["word"]) == 5 and entry["word"].isalpha()]
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Error reading 'words.txt'. Falling back to default word list.")
        return ["apple", "grape", "silly", "crazy", "world", "brick", "flame", "spoon", "train", "lucky"]

WORDS = load_words_from_json()

class MuddleMouth:
    def __init__(self, canvas):
        self.canvas = canvas
        self.secret = random.choice(WORDS)
        self.guesses = []
        self.current_guess = ""
        self.row = 0

        self.total_width = (TILE_SIZE + PADDING) * GRID_SIZE - PADDING
        self.total_height = (TILE_SIZE + PADDING) * MAX_TRIES - PADDING
        self.offset_x = (CANVAS_WIDTH - self.total_width) // 2
        self.offset_y = (CANVAS_HEIGHT - self.total_height) // 2
        self.bg_image = bg_image

    def draw_background(self):
        if self.bg_image:
            self.canvas.create_image_with_size(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, self.bg_image)
        else:
            self.canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, color="lightgray")

    def draw_grid(self):
        for r in range(MAX_TRIES):
            for c in range(GRID_SIZE):
                x = self.offset_x + c * (TILE_SIZE + PADDING)
                y = self.offset_y + r * (TILE_SIZE + PADDING)
                self.canvas.create_rectangle(x, y, x + TILE_SIZE, y + TILE_SIZE, color="#87CEFA")

    def draw_guess(self, word, row):
        for i, char in enumerate(word):
            color = "#D3D3D3"
            if char == self.secret[i]:
                color = "#00FA9A"
            elif char in self.secret:
                color = "#FFD700"
            else:
                color = "#FF4500"

            x = self.offset_x + i * (TILE_SIZE + PADDING)
            y = self.offset_y + row * (TILE_SIZE + PADDING)
            self.canvas.create_rectangle(x, y, x + TILE_SIZE, y + TILE_SIZE, color=color)
            self.canvas.create_text(x + TILE_SIZE / 2, y + TILE_SIZE / 2, char.upper(), font="Comic Sans MS", font_size=20, color="white")

    def redraw_current_input(self):
        if self.row >= MAX_TRIES:
            return
        for i in range(GRID_SIZE):
            x = self.offset_x + i * (TILE_SIZE + PADDING)
            y = self.offset_y + self.row * (TILE_SIZE + PADDING)
            self.canvas.create_rectangle(x, y, x + TILE_SIZE, y + TILE_SIZE, color="#FFE4B5")
            if i < len(self.current_guess):
                self.canvas.create_text(x + TILE_SIZE / 2, y + TILE_SIZE / 2, self.current_guess[i].upper(), font="Comic Sans MS", font_size=20, color="black")

    def handle_guess(self, guess):
        if self.row >= MAX_TRIES:
            return
        self.current_guess = guess.lower()
        if len(self.current_guess) != GRID_SIZE or not self.current_guess.isalpha():
            print("Invalid input! Please enter exactly 5 letters.")
            return
        self.guesses.append(self.current_guess)
        self.draw_guess(self.current_guess, self.row)
        if self.current_guess == self.secret:
            self.win_animation()
        else:
            self.row += 1
            self.current_guess = ""
            self.redraw_current_input()

    def win_animation(self):
        self.canvas.clear()
        self.draw_background()
        message = "🎉 You won, MuddleMouth is proud 🎉"
        x = CANVAS_WIDTH // 2
        y = CANVAS_HEIGHT // 2
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        pulse_sizes = [24, 28, 32, 28]
        cycles = 10

        circle_colors = ["#FF6347", "#3CB371", "#1E90FF", "#FFD700", "#FF69B4"]
        circles = []
        for _ in range(15):
            circles.append({
                "x": random.randint(50, CANVAS_WIDTH - 50),
                "y": random.randint(50, CANVAS_HEIGHT - 50),
                "radius": random.randint(10, 30),
                "color": random.choice(circle_colors),
                "phase": random.uniform(0, 2 * math.pi),
                "speed": random.uniform(0.02, 0.05),
            })

        for cycle in range(cycles):
            for size in pulse_sizes:
                self.canvas.clear()
                self.draw_background()
                for circle in circles:
                    circle["phase"] += circle["speed"]
                    float_y = circle["y"] + 10 * math.sin(circle["phase"])
                    r = circle["radius"]
                    self.canvas.create_oval(circle["x"] - r, float_y - r, circle["x"] + r, float_y + r, color=circle["color"])
                color = colors[cycle % len(colors)]
                self.canvas.create_text(x, y, message, font="Comic Sans MS", font_size=size, color=color)
                time.sleep(0.15)

    def lose_message(self): 
     self.canvas.clear()
     self.draw_background()

     # Enhanced, elegant, and colorful text components
     base_text = "The hidden word was '"
     secret_text = self.secret.upper()
     end_text = "    so close!"

     font_size = 25
     approx_char_width = font_size * 0.5

     base_width = int(len(base_text) * approx_char_width)
     secret_width = int(len(secret_text) * approx_char_width)
     end_width = int(len(end_text) * approx_char_width)

     total_width = base_width + secret_width + end_width

     x_start = CANVAS_WIDTH // 2 - total_width // 2
     y = CANVAS_HEIGHT // 2 - 60

     # Base text - golden orange
     self.canvas.create_text(
        x_start, y,
        base_text,
        font="Comic Sans MS",
        font_size=font_size,
        color="#FF8C00",  # Dark orange
        anchor="w"
     )

     # Secret word - rich royal blue
     self.canvas.create_text(
        x_start + base_width, y,
        secret_text,
        font="Comic Sans MS bold",
        font_size=font_size,
        color="#4169E1",  # Royal Blue
        anchor="w"
     )

     # End text - deep pink
     self.canvas.create_text(
        x_start + base_width + secret_width, y,
        end_text,
        font="Comic Sans MS",
        font_size=font_size,
        color="#C71585",  # Medium Violet Red
        anchor="w"
     )

     # Second line - friendly purple with fun emoji
     self.canvas.create_text(
        CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 + 30,
        "MuddleMouth giggles in confusion 😵‍💫💬",
        font="Comic Sans MS italic",
        font_size=26,
        color="#800080",  # Purple
        anchor="center"
     )

     # Optional third line - encouragement
     self.canvas.create_text(
        CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 + 75,
        "Try again and outsmart the giggles! 🤓✨",
        font="Comic Sans MS",
        font_size=22,
        color="#228B22",  # Forest green
        anchor="center"
     )



def welcome_screen(canvas):
    canvas.clear()

    if bg_image:
        canvas.create_image_with_size(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, bg_image)
    else:
        canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, color="lightgray")

    center_x = CANVAS_WIDTH // 2
    center_y = CANVAS_HEIGHT // 2

    # Title and subtitle
    canvas.create_text(center_x, center_y - 100, "Welcome to MuddleMouth",
                       font="Comic Sans MS", font_size=28, color="darkblue", anchor='center')
    canvas.create_text(center_x, center_y - 60, "A colorful 5-letter guessing game",
                       font="Comic Sans MS", font_size=16, color="darkgreen", anchor='center')

    # Button setup
    button_width = 180
    button_height = 60
    button_x = center_x - button_width // 2
    button_y = center_y
    button_color = "#4A90E2"
    button_hover_color = "#357ABD"

    # Shadow layer
    canvas.create_rectangle(
        button_x + 3, button_y + 3,
        button_x + button_width + 3, button_y + button_height + 3,
        "#333333", "#333333"
    )

    # Button background
    button_rect = canvas.create_rectangle(
        button_x, button_y,
        button_x + button_width, button_y + button_height,
        button_color, "#2C5282"
    )

    # Highlight
    highlight_rect = canvas.create_rectangle(
        button_x + 2, button_y + 2,
        button_x + button_width - 2, button_y + 15,
        "#87CEEB", "#87CEEB"
    )

    # Button label
    label = canvas.create_text(
        center_x, button_y + button_height // 2,
        "START GAME",
        font="Comic Sans MS", font_size=18, color="white", anchor='center'
    )

    # Wait for a valid click
    while True:
        click = canvas.get_last_click()
        if click:
            x, y = click
            if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
                # Simulate click effect
                canvas.set_color(button_rect, button_hover_color)
                canvas.set_color(highlight_rect, "#5A9BD4")

                # Remove old label and show "STARTING..."
                canvas.delete(label)
                canvas.create_text(center_x, button_y + button_height // 2,
                                   "STARTING...", font="Comic Sans MS",
                                   font_size=18, color="white", anchor='center')

                time.sleep(0.5)
                break
        time.sleep(0.01)


def main():
    print("🎮 Welcome to MuddleMouth Wordle! Guess the 5-letter word. You have 6 tries. Good luck! 🍀")
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    welcome_screen(canvas)
    game = MuddleMouth(canvas)
    game.draw_background()
    game.draw_grid()
    game.redraw_current_input()

    while game.row < MAX_TRIES and (not game.guesses or game.guesses[-1] != game.secret):
        guess = input(f"Enter guess #{game.row + 1} (5-letter word): ").strip().lower()
        game.handle_guess(guess)

    if not game.guesses or game.guesses[-1] != game.secret:
        print(f"😢 Out of tries! The word was: {game.secret}")
        game.lose_message()


if __name__ == "__main__":
    main()