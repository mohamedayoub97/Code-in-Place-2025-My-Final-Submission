from graphics import Canvas
import random
import time

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
CHOICES = ["rock", "paper", "scissors"]
EMOJIS = {"rock": "✊🏽", "paper": "🖐🏽", "scissors": "✌🏽"}

gradient_sets = [ 
    ["#FFF7FA", "#FDF0FF", "#EEF8FF", "#EFFFF9", "#FFFAF0"],  # Set 1: Blushes and creams
    ["#F0FFF4", "#E0F7FA", "#E3F2FD", "#F3E5F5", "#FFFDE7"],  # Set 2: Whisper pastels
    ["#FAF0E6", "#F5F5F5", "#F0F8FF", "#F8F8FF", "#FDFEFE"],  # Set 3: Almost invisible soft hues
    ["#FFF0F5", "#F0FFFF", "#F5FFFA", "#FFFFF0", "#FFFAFA"],  # Set 4: Lightest tints of common pastel families
    ["#EBF5FB", "#E8F8F5", "#FEF9E7", "#FDEDEC", "#F9EBEA"],  # Set 5: Harmonious soft blends
]


def draw_background(canvas, gradient_index):
    canvas.clear()
    colors = gradient_sets[gradient_index]
    steps = 100
    step_height = CANVAS_HEIGHT // steps
    for i in range(steps):
        band_index = int(i / steps * (len(colors) - 1))
        color = colors[band_index]
        canvas.create_rectangle(
            0, i * step_height,
            CANVAS_WIDTH, (i + 1) * step_height,
            color, color
        )
    shimmer_y = CANVAS_HEIGHT // 2
    canvas.create_rectangle(0, shimmer_y, CANVAS_WIDTH, shimmer_y + 1, "#FFDDEE", "#FFDDEE")

def estimate_text_width(text, font_size):
    return font_size * 0.6 * len(text)

def draw_centered_text(canvas, center_x, center_y, text, font_size, color):
    text_width = estimate_text_width(text, font_size)
    return canvas.create_text(center_x - text_width / 2, center_y, text, font='Chalkboardbold', font_size=font_size, color=color)

def draw_button(canvas, text, x=125, y=170, w=150, h=60):
    canvas.create_rectangle(x + 3, y + 3, x + w + 3, y + h + 3, "#222", "#222")
    rect = canvas.create_rectangle(x, y, x + w, y + h, "#4CAF50", "#388E3C")
    canvas.create_rectangle(x + 2, y + 2, x + w - 2, y + 15, "#A5D6A7", "#A5D6A7")
    draw_centered_text(canvas, x + w / 2 + 6, y + h / 2 - 5, text, 18, "white")
    return rect, (x, y, w, h)

def is_click_inside(click, bounds):
    x, y = click
    bx, by, bw, bh = bounds
    return bx <= x <= bx + bw and by <= y <= by + bh

def draw_start_screen(canvas, gradient_index):
    draw_background(canvas, gradient_index)
    draw_centered_text(canvas, CANVAS_WIDTH / 2 + 35, 50, "🎯 Rock Paper Scissors 🎯", 30, "#2C3E50")
    draw_centered_text(canvas, CANVAS_WIDTH / 2 + 25, 100, "Click to Start", 15, "#34495E")
    draw_centered_text(canvas, CANVAS_WIDTH - 185, CANVAS_HEIGHT - 50, "© 2025 Mohamed Ayoub Essalami", 10, "black")
    return draw_button(canvas, "🌈 Start Game 🌈")

def draw_game_ui(canvas, player_pts, comp_pts, gradient_index):
    draw_background(canvas, gradient_index)
    draw_centered_text(canvas, CANVAS_WIDTH / 2 + 48, 30, "🌟 Rock, Paper, Scissors 🌟", 30, "black")
    draw_centered_text(canvas, CANVAS_WIDTH / 2 - 100, 80, "Computer", 15, "#444")
    draw_centered_text(canvas, CANVAS_WIDTH / 2 + 100, 80, "You", 15, "#444")
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 140, "VS", 20, "#222")

    player_score_text = draw_centered_text(canvas, CANVAS_WIDTH / 2 + 100, 100, str(player_pts), 18, "red")
    comp_score_text = draw_centered_text(canvas, CANVAS_WIDTH / 2 - 100, 100, str(comp_pts), 18, "red")

    positions = {
        "rock": CANVAS_WIDTH / 2 - 100,
        "paper": CANVAS_WIDTH / 2,
        "scissors": CANVAS_WIDTH / 2 + 100
    }

    emoji_objs = {}
    y = 240
    for choice, x in positions.items():
        emoji_objs[choice] = draw_centered_text(canvas, x, y, EMOJIS[choice], 38, "#111")

    return {
        "player_score": player_score_text,
        "comp_score": comp_score_text,
        "positions": positions,
        "emoji_objs": emoji_objs,
    }

def animate_emoji(canvas, x, y, emoji, color):
    obj = None
    for size in range(60, 81, 3):
        if obj:
            canvas.delete(obj)
        obj = draw_centered_text(canvas, x, y, emoji, size, color)
        time.sleep(0.01)
    for size in range(80, 59, -3):
        canvas.delete(obj)
        obj = draw_centered_text(canvas, x, y, emoji, size, color)
        time.sleep(0.01)
    return obj

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    current_gradient_index = 0
    last_background_change = time.time()

    button_rect, button_bounds = draw_start_screen(canvas, current_gradient_index)

    while True:
        click = canvas.get_last_click()
        now = time.time()
        if now - last_background_change > 3:
            current_gradient_index = (current_gradient_index + 1) % len(gradient_sets)
            draw_start_screen(canvas, current_gradient_index)
            last_background_change = now

        if click and is_click_inside(click, button_bounds):
            break
        time.sleep(0.01)

    player_pts = 0
    comp_pts = 0
    ui = draw_game_ui(canvas, player_pts, comp_pts, current_gradient_index)
    last_background_change = time.time()

    while player_pts < 3 and comp_pts < 3:
        click = canvas.get_last_click()
        now = time.time()

        if now - last_background_change > 3:
            current_gradient_index = (current_gradient_index + 1) % len(gradient_sets)
            ui = draw_game_ui(canvas, player_pts, comp_pts, current_gradient_index)
            last_background_change = now

        if click:
            for choice, x_pos in ui["positions"].items():
                if abs(click[0] - x_pos) < 40 and abs(click[1] - 240) < 40:
                    player_choice = choice
                    comp_choice = random.choice(CHOICES)

                    animate_emoji(canvas, CANVAS_WIDTH / 2 + 100, 140, EMOJIS[player_choice], "#000")
                    animate_emoji(canvas, CANVAS_WIDTH / 2 - 100, 140, EMOJIS[comp_choice], "#000")

                    if player_choice == comp_choice:
                        pass
                    elif (player_choice == "rock" and comp_choice == "scissors") or \
                         (player_choice == "paper" and comp_choice == "rock") or \
                         (player_choice == "scissors" and comp_choice == "paper"):
                        player_pts += 1
                    else:
                        comp_pts += 1

                    canvas.change_text(ui["player_score"], str(player_pts))
                    canvas.change_text(ui["comp_score"], str(comp_pts))

        time.sleep(0.01)

    canvas.clear()
    draw_background(canvas, current_gradient_index)
    result = "🎉 You Win! 🎉" if player_pts == 3 else "💀 Computer Wins 💀"
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 140, result, 30, "#000")
    _, restart_bounds = draw_button(canvas, "🔄 Play Again 🔄", 125, 200,)

    while True:
        click = canvas.get_last_click()
        if click and is_click_inside(click, restart_bounds):
            main()
        time.sleep(0.05)

if __name__ == "__main__":
    main() 