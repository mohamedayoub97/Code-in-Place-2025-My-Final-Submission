from graphics import Canvas
import random
import math
import time

# Constants
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 300
BRICK_WIDTH = 30
BRICK_HEIGHT = 12
BRICKS_IN_BASE = 14
GROUND_Y = CANVAS_HEIGHT - (BRICKS_IN_BASE * BRICK_HEIGHT)

# Character physics
MOVE_SPEED = 1
JUMP_VELOCITY = 10
GRAVITY = 100

def random_color():
    r = random.randint(120, 255)
    g = random.randint(120, 255)
    b = random.randint(120, 255)
    return f"#{r:02x}{g:02x}{b:02x}"

def draw_gradient_sky(canvas):
    top_color = (25, 25, 112)
    bottom_color = (255, 140, 0)
    for i in range(CANVAS_HEIGHT):
        ratio = i / CANVAS_HEIGHT
        r = int(top_color[0] + ratio * (bottom_color[0] - top_color[0]))
        g = int(top_color[1] + ratio * (bottom_color[1] - top_color[1]))
        b = int(top_color[2] + ratio * (bottom_color[2] - top_color[2]))
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, CANVAS_WIDTH, i, color)

def draw_sun_with_rays(canvas):
    cx, cy = 80, 80
    radius = 30
    for i in range(10, 0, -1):
        glow_radius = radius + i * 8
        ratio = i / 10
        r = 255
        g = int(255 * ratio)
        b = int(100 * ratio)
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_oval(cx - glow_radius, cy - glow_radius, cx + glow_radius, cy + glow_radius, color)
    canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, "#ffff00")
    for i in range(48):
        angle = math.radians(i * (360 / 48))
        x1 = cx + (radius + 5) * math.cos(angle)
        y1 = cy + (radius + 5) * math.sin(angle)
        x2 = cx + (radius + 50 + random.randint(-10, 10)) * math.cos(angle)
        y2 = cy + (radius + 50 + random.randint(-10, 10)) * math.sin(angle)
        canvas.create_line(x1, y1, x2, y2, "#ffff9966")

def draw_cloud(canvas, x, y):
    canvas.create_oval(x, y, x+60, y+30, "white")
    canvas.create_oval(x+20, y-10, x+70, y+20, "white")
    canvas.create_oval(x+40, y, x+90, y+30, "white")

def draw_brick_pyramid(canvas):
    for row in range(BRICKS_IN_BASE):
        count = BRICKS_IN_BASE - row
        start_x = (CANVAS_WIDTH - count * BRICK_WIDTH) / 2
        y = CANVAS_HEIGHT - (row + 1) * BRICK_HEIGHT
        for b in range(count):
            x = start_x + b * BRICK_WIDTH
            canvas.create_rectangle(x, y, x + BRICK_WIDTH, y + BRICK_HEIGHT, random_color())

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    draw_gradient_sky(canvas)
    draw_sun_with_rays(canvas)
    draw_cloud(canvas, 150, 50)
    draw_cloud(canvas, 400, 80)
    draw_brick_pyramid(canvas)

    # Character (placed at bottom-left and scaled down smaller than bricks)
    CHAR_WIDTH = 100
    CHAR_HEIGHT = 100
    x = 0
    y = GROUND_Y - CHAR_HEIGHT
    karol = canvas.create_image_with_size(x, y, CHAR_WIDTH, CHAR_HEIGHT, "Karol.png")
    vy = 0
    on_ground = True


    while True:
        # Handle input
        keys = canvas.get_new_key_presses()
        dx = 0
        for key in keys:
            if key == "Left":
                dx -= MOVE_SPEED
            elif key == "Right":
                dx += MOVE_SPEED
            elif key == "space" and on_ground:
                vy = JUMP_VELOCITY
                on_ground = False

        # Update position
        x += dx
        vy += GRAVITY
        y += vy

        # Clamp to ground
        if y >= GROUND_Y - 60:
            y = GROUND_Y - 60
            vy = 0
            on_ground = True

        # Move character
        canvas.moveto(karol, x, y)

       
        time.sleep(1/60)

if __name__ == "__main__":
    main()
