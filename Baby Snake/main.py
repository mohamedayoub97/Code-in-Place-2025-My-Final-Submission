from graphics import Canvas
import time
import random

# Constants
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
GRID_SIZE = 20
INITIAL_DELAY = 0.1
PLAYER_COLOR = "blue"
GOAL_COLOR = "red"
FONT_SIZE = 20
CIRCLE_SIZE = 20
N_CIRCLES = 20

def place_goal(canvas):
    """Place the goal at a random grid-aligned position."""
    cols = CANVAS_WIDTH // GRID_SIZE
    rows = CANVAS_HEIGHT // GRID_SIZE
    x = random.randint(0, cols - 1) * GRID_SIZE
    y = random.randint(0, rows - 1) * GRID_SIZE
    return canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, GOAL_COLOR)

def move_player(canvas, player, direction):
    """Move the player in the specified direction."""
    moves = {
        'ArrowLeft': (-GRID_SIZE, 0),
        'ArrowRight': (GRID_SIZE, 0),
        'ArrowUp': (0, -GRID_SIZE),
        'ArrowDown': (0, GRID_SIZE)
    }
    dx, dy = moves.get(direction, (0, 0))
    canvas.move(player, dx, dy)

def get_position(canvas, obj):
    """Get the (x, y) of the top-left corner of an object."""
    return int(canvas.get_left_x(obj)), int(canvas.get_top_y(obj))

def is_out_of_bounds(x, y):
    """Check if the position is outside the canvas."""
    return x < 0 or x >= CANVAS_WIDTH or y < 0 or y >= CANVAS_HEIGHT

def update_score_display(canvas, score_text_id, score):
    """Update the score text."""
    canvas.change_text(score_text_id, f"Score: {score}")

def draw_random_circles(canvas, n=N_CIRCLES):
    """Draw pastel-colored circles to simulate transparency."""
    for _ in range(n):
        x = random.randint(0, CANVAS_WIDTH - CIRCLE_SIZE)
        y = random.randint(0, CANVAS_HEIGHT - CIRCLE_SIZE)
        color = random_color()
        canvas.create_oval(x, y, x + CIRCLE_SIZE, y + CIRCLE_SIZE, color)

def random_color():
    """Return a soft pastel color."""
    colors = [
        '#AEC6CF',  # pastel blue
        '#FFB347',  # pastel orange
        '#B39EB5',  # pastel purple
        '#77DD77',  # pastel green
        '#F49AC2',  # pastel pink
        '#CFCFC4',  # light gray
        '#FDFD96',  # pastel yellow
    ]
    return random.choice(colors)

def fade_canvas(canvas):
    """Simulate transparency by overlaying a soft white rectangle."""
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, '#FFFFFF') 
def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    player = canvas.create_rectangle(0, 0, GRID_SIZE, GRID_SIZE, PLAYER_COLOR)
    goal = place_goal(canvas)
    score_text = canvas.create_text(10, 10, anchor="nw", text="Score: 0", font_size=FONT_SIZE)
    
    direction = 'ArrowRight'
    score = 0
    delay = INITIAL_DELAY
    
    draw_random_circles(canvas)  # Initial background

    while True:
        key = canvas.get_last_key_press()
        if key in ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown']:
            direction = key

        move_player(canvas, player, direction)
        player_x, player_y = get_position(canvas, player)

        if is_out_of_bounds(player_x, player_y):
            canvas.clear()
            canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2,
                               text=f'You died!\nFinal Score: {score}',
                               font_size=30, anchor='center')
            break

        goal_x, goal_y = get_position(canvas, goal)
        if (player_x, player_y) == (goal_x, goal_y):
            canvas.delete(goal)
            goal = place_goal(canvas)
            score += 1
            update_score_display(canvas, score_text, score)
            delay = max(0.02, delay * 0.9)

            draw_random_circles(canvas)  # Visual feedback
            if score % 3 == 0:
                fade_canvas(canvas)  # Soft fade effect every few points

        time.sleep(delay)

if __name__ == '__main__':
    main()
