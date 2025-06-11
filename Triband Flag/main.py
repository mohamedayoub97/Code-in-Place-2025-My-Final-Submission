from graphics import Canvas

CANVAS_WIDTH = 450
CANVAS_HEIGHT = 300

def parse_color(color_input):
    color_input = color_input.strip()
    if color_input.startswith("(") and color_input.endswith(")"):
        # Parse RGB tuple
        try:
            parts = color_input[1:-1].split(",")
            r, g, b = [int(p.strip()) for p in parts]
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            print(f"Invalid RGB value: {color_input}")
            return "black"
    elif color_input.startswith("#"):
        return color_input.lower()
    else:
        return color_input.lower()

def draw_triband_flag(canvas, color_a, color_b, color_c, orientation="vertical"):
    if orientation == "vertical":
        band_width = CANVAS_WIDTH / 3
        canvas.create_rectangle(0, 0, band_width, CANVAS_HEIGHT, color=color_a)
        canvas.create_rectangle(band_width, 0, 2 * band_width, CANVAS_HEIGHT, color=color_b)
        canvas.create_rectangle(2 * band_width, 0, CANVAS_WIDTH, CANVAS_HEIGHT, color=color_c)
    elif orientation == "horizontal":
        band_height = CANVAS_HEIGHT / 3
        canvas.create_rectangle(0, 0, CANVAS_WIDTH, band_height, color=color_a)
        canvas.create_rectangle(0, band_height, CANVAS_WIDTH, 2 * band_height, color=color_b)
        canvas.create_rectangle(0, 2 * band_height, CANVAS_WIDTH, CANVAS_HEIGHT, color=color_c)
    else:
        print("Invalid orientation. Use 'vertical' or 'horizontal'.")

def main():
    orientation = input("Enter flag orientation ('vertical' or 'horizontal'): ").strip().lower()

    print("Enter three colors for the flag (can be named, hex like #008000, or RGB like (255,255,255)):")
    color_a = parse_color(input("Color 1: "))
    color_b = parse_color(input("Color 2: "))
    color_c = parse_color(input("Color 3: "))

    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    draw_triband_flag(canvas, color_a, color_b, color_c, orientation)

main()
