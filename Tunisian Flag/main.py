from graphics import Canvas
import math
import time

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

FLAG_WIDTH = 270
FLAG_HEIGHT = 180
WAVE_AMPLITUDE = 8
WAVE_FREQUENCY = 0.25
FRAME_DELAY = 0.03  # in seconds

def draw_star(canvas, cx, cy, outer_radius, color):
    """Draw a 5-pointed star centered at (cx, cy)."""
    points = []
    for i in range(10):
        angle_deg = i * 36 - 90
        radius = outer_radius if i % 2 == 0 else outer_radius * 0.4
        angle_rad = math.radians(angle_deg)
        x = cx + radius * math.cos(angle_rad)
        y = cy + radius * math.sin(angle_rad)
        points.extend([x, y])
    canvas.create_polygon(*points, color=color)

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    n_rows = 12
    n_cols = 20
    cell_w = FLAG_WIDTH / n_cols
    cell_h = FLAG_HEIGHT / n_rows
    flag_top = 60
    flag_left = 100

    t = 0
    while True:
        canvas.clear()

        # Ground
        canvas.create_rectangle(0, CANVAS_HEIGHT - 40, CANVAS_WIDTH, CANVAS_HEIGHT, "green")

        # Flagpole
        canvas.create_rectangle(80, 50, 100, CANVAS_HEIGHT - 40, "gray")

        # Flag waving with rectangles
        for r in range(n_rows):
            for c in range(n_cols):
                dx = WAVE_AMPLITUDE * math.sin(WAVE_FREQUENCY * r + t)
                x = flag_left + c * cell_w + dx
                y = flag_top + r * cell_h
                canvas.create_rectangle(
                    x, y,
                    x + cell_w, y + cell_h,
                    "red", "red"
                )

        # Draw crescent and star centered on the flag
        cx = flag_left + FLAG_WIDTH / 2
        cy = flag_top + FLAG_HEIGHT / 2

        # White circle
        circle_radius = 45
        canvas.create_oval(cx - circle_radius, cy - circle_radius,
                           cx + circle_radius, cy + circle_radius,
                           "white")

        # Crescent
        crescent_outer = 24
        crescent_inner = 18
        crescent_offset = 10
        canvas.create_oval(cx - crescent_outer - crescent_offset, cy - crescent_outer,
                           cx + crescent_outer - crescent_offset, cy + crescent_outer,
                           "red")
        canvas.create_oval(cx - crescent_inner, cy - crescent_inner,
                           cx + crescent_inner, cy + crescent_inner,
                           "white")

        # Star
        draw_star(canvas, cx + 12, cy, 12, "red")

        time.sleep(FRAME_DELAY)
        t += 10

if __name__ == '__main__':
    main()
