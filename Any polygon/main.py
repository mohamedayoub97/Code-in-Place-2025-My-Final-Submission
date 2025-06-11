import math 
import time 
from graphics import Canvas 

CANVAS_WIDTH = 400 
CANVAS_HEIGHT = 400 

def rgb_to_hex(r, g, b): 
    return f"#{r:02x}{g:02x}{b:02x}" 

def estimate_text_width(text, font_size): 
    return font_size * 0.5 * len(text) 

def draw_centered_text(canvas, center_x, y, text, font_size, color): 
    text_width = estimate_text_width(text, font_size) 
    true_x = center_x - text_width / 2 
    return canvas.create_text( 
        true_x, y, 
        text, 
        font='Arial', 
        font_size=font_size, 
        color=color 
    ) 

def hsv_to_rgb(h, s, v): 
    """Convert HSV (all 0-1 floats) to RGB (0-255 ints).""" 
    if s == 0.0: 
        r = g = b = int(v * 255) 
        return r, g, b 
    i = int(h * 6)  # sector 0 to 5 
    f = (h * 6) - i 
    p = v * (1 - s) 
    q = v * (1 - s * f) 
    t = v * (1 - s * (1 - f)) 
    i = i % 6 
    if i == 0: 
        r, g, b = v, t, p 
    elif i == 1: 
        r, g, b = q, v, p 
    elif i == 2: 
        r, g, b = p, v, t 
    elif i == 3: 
        r, g, b = p, q, v 
    elif i == 4: 
        r, g, b = t, p, v 
    else:  # i == 5 
        r, g, b = v, p, q 
    return int(r * 255), int(g * 255), int(b * 255) 

def draw_colorful_polygon(canvas, num_sides, radius=100, rotation_offset=0): 
    cx = CANVAS_WIDTH / 2 
    cy = CANVAS_HEIGHT / 2 
    base_points = [] 
    for n in range(num_sides): 
        angle = 2 * math.pi * n / num_sides + rotation_offset 
        x = cx + radius * math.sin(angle) 
        y = cy - radius * math.cos(angle) 
        base_points.append((x, y)) 

    layers = 12  # more layers for richer gradients 
    for i in range(layers): 
        factor = i / layers 
        points = [] 
        for x, y in base_points: 
            new_x = cx + (x - cx) * (1 - factor * 0.9) 
            new_y = cy + (y - cy) * (1 - factor * 0.9) 
            points.extend([new_x, new_y]) 

        # Use HSV for sharp full saturation rainbow colors 
        # Hue cycles through 0-1 as factor changes, Saturation=1 (full), Value=1 (bright) 
        h = (factor + 0.1) % 1.0  # shift hue slightly for variation 
        s = 1.0 
        v = 1.0 
        r, g, b = hsv_to_rgb(h, s, v) 

        color = rgb_to_hex(r, g, b) 
        polygon_id = canvas.create_polygon(*points) 
        canvas.set_color(polygon_id, color) 

def draw_background(canvas): 
    # Soft pastel vertical stripes as background 
    for i in range(20): 
        r = int(245 + 10 * math.sin(i)) 
        g = int(245 + 10 * math.sin(i + 2)) 
        b = int(245 + 10 * math.sin(i + 4)) 
        color = rgb_to_hex(r, g, b) 
        canvas.create_rectangle( 
            i * 20, 0, (i + 1) * 20, CANVAS_HEIGHT, 
            color, color 
        ) 

def main(): 
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT) 
    draw_background(canvas) 

    # Button properties 
    button_x = 125 
    button_y = 170 
    button_width = 150 
    button_height = 60 
    button_color = "#EAF6FF" 
    button_hover_color = "#DDEEFF" 
    button_text = "🎨 Start Drawing" 
    font_size = 16 

    shadow_offset = 3 
    canvas.create_rectangle( 
        button_x + shadow_offset, button_y + shadow_offset, 
        button_x + button_width + shadow_offset, button_y + button_height + shadow_offset, 
        "#DDDDDD", "#DDDDDD" 
    ) 

    button_rect = canvas.create_rectangle( 
        button_x, button_y, 
        button_x + button_width, button_y + button_height, 
        button_color, "#F7FBFF" 
    ) 

    highlight_rect = canvas.create_rectangle( 
        button_x + 2, button_y + 2, 
        button_x + button_width - 2, button_y + 15, 
        "#F0FAFF", "#F0FAFF" 
    ) 

    text_y = button_y + button_height / 2 - font_size / 2 
    button_label = draw_centered_text(canvas, button_x + button_width / 2, text_y, button_text, font_size, "#2D3748") 

    draw_centered_text(canvas, CANVAS_WIDTH / 2, 50, "🌈 Polygon Painter 🌈", 18, "#2D3748") 
    draw_centered_text(canvas, CANVAS_WIDTH / 2 + 15, 80, "Click the button to begin drawing", 12, "#4A5568") 

    while True: 
        click = canvas.get_last_click() 
        if click is not None: 
            click_x, click_y = click 
            if (button_x <= click_x <= button_x + button_width and 
                button_y <= click_y <= button_y + button_height): 
                # Button pressed animation 
                canvas.set_color(button_rect, button_hover_color) 
                canvas.set_color(highlight_rect, "#D5EFFF") 
                canvas.change_text(button_label, "⏳ Starting...") 
                time.sleep(1.5)  # simulate loading 

                # Ask for user input once 
                try: 
                    num_sides = int(input("Enter number of sides (>=3): ")) 
                    if num_sides < 3: 
                        print("Invalid: number of sides must be >= 3.") 
                        return 
                    degrees = float(input("Enter rotation in degrees (0 to 360): ")) 
                    rotation_offset = math.radians(degrees) 
                except ValueError: 
                    print("Invalid input. Exiting.") 
                    return 

                canvas.clear() 
                draw_background(canvas) 
                draw_colorful_polygon(canvas, num_sides, radius=100, rotation_offset=rotation_offset) 
                break 
        time.sleep(0.01) 

if __name__ == '__main__': 
    main()