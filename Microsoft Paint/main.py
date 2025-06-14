from graphics import Canvas
import time
import math

# Canvas dimensions
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800

# UI Layout constants
TOOLBAR_HEIGHT = 80
COLOR_PANEL_WIDTH = 200
DRAWING_AREA_X = COLOR_PANEL_WIDTH + 20
DRAWING_AREA_Y = TOOLBAR_HEIGHT + 20
DRAWING_AREA_WIDTH = CANVAS_WIDTH - DRAWING_AREA_X - 20
DRAWING_AREA_HEIGHT = CANVAS_HEIGHT - DRAWING_AREA_Y - 20

# Colors
BACKGROUND_COLOR = "#F5F5F5"
TOOLBAR_COLOR = "#E8E8E8"
DRAWING_BG_COLOR = "white"
BUTTON_COLOR = "#4A90E2"
BUTTON_HOVER_COLOR = "#357ABD"
SELECTED_COLOR = "#38A169"

def estimate_text_width(text, font_size):
    """Estimate text width for centering"""
    return font_size * 0.6 * len(text)

def draw_centered_text(canvas, center_x, y, text, font_size, color):
    """Draw text centered at given coordinates"""
    text_width = estimate_text_width(text, font_size)
    true_x = center_x - text_width / 2
    return canvas.create_text(
        true_x, y, text,
        font='Arial', font_size=font_size, color=color
    )

def create_button(canvas, x, y, width, height, text, is_selected=False):
    """Create a styled button with shadow and highlight"""
    # Shadow
    shadow = canvas.create_rectangle(
        x + 2, y + 2, x + width + 2, y + height + 2,
        "#CCCCCC", "#CCCCCC"
    )
    
    # Button body
    color = SELECTED_COLOR if is_selected else BUTTON_COLOR
    button_rect = canvas.create_rectangle(
        x, y, x + width, y + height,
        color, "#2C5282"
    )
    
    # Highlight
    highlight_color = "#87CEEB" if not is_selected else "#68D391"
    highlight = canvas.create_rectangle(
        x + 2, y + 2, x + width - 2, y + 12,
        highlight_color, highlight_color
    )
    
    # Button text
    text_y = y + height / 2 - 8
    label = draw_centered_text(canvas, x + width / 2, text_y, text, 12, "white")
    
    return {
        'shadow': shadow,
        'rect': button_rect,
        'highlight': highlight,
        'label': label,
        'x': x, 'y': y, 'width': width, 'height': height,
        'text': text
    }

def create_color_button(canvas, x, y, size, color):
    """Create a color selection button"""
    # Shadow
    shadow = canvas.create_rectangle(
        x + 1, y + 1, x + size + 1, y + size + 1,
        "#999999", "#999999"
    )
    
    # Color square
    color_rect = canvas.create_rectangle(
        x, y, x + size, y + size,
        color, "black"
    )
    
    return {
        'shadow': shadow,
        'rect': color_rect,
        'x': x, 'y': y, 'size': size, 'color': color
    }

def point_in_rect(px, py, x, y, width, height):
    """Check if point is inside rectangle"""
    return x <= px <= x + width and y <= py <= y + height

def is_in_drawing_area(x, y):
    """Check if coordinates are in drawing area"""
    return (DRAWING_AREA_X <= x <= DRAWING_AREA_X + DRAWING_AREA_WIDTH and
            DRAWING_AREA_Y <= y <= DRAWING_AREA_Y + DRAWING_AREA_HEIGHT)

def main():
    # Initialize canvas
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    # Current state
    current_color = "black"
    current_tool = "brush"
    brush_size = 3 
    is_mouse_pressed = False 
    last_x = None
    last_y = None
    shape_start_x = None
    shape_start_y = None
    
    # Color palette
    colors = [
        "black", "white", "red", "darkred", "lightcoral", "crimson",
        "blue", "darkblue", "lightblue", "navy", "cyan", "darkcyan",
        "green", "darkgreen", "lightgreen", "lime", "yellow", "gold",
        "orange", "purple", "magenta", "pink", "brown", "gray"
    ]
    
    # UI elements storage
    tool_buttons = []
    color_buttons = []
    ui_elements = []
    drawing_objects = []
    
    # Setup UI
    print("🎨 Setting up Microsoft Paint Clone...")
    
    # Background
    bg = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, BACKGROUND_COLOR)
    ui_elements.append(bg)
    
    # Toolbar background
    toolbar_bg = canvas.create_rectangle(
        0, 0, CANVAS_WIDTH, TOOLBAR_HEIGHT, TOOLBAR_COLOR, "#CCCCCC"
    )
    ui_elements.append(toolbar_bg)
    
    # Title
    title = draw_centered_text(canvas, CANVAS_WIDTH // 2, 25, "🎨 Microsoft Paint Clone", 20, "#2D3748")
    ui_elements.append(title)
    
    subtitle = draw_centered_text(canvas, CANVAS_WIDTH // 2+30, 55, "Select tools and colors, then draw in the white area", 12, "#4A5568")
    ui_elements.append(subtitle)
    
    # Drawing area background with border
    drawing_bg = canvas.create_rectangle(
        DRAWING_AREA_X - 2, DRAWING_AREA_Y - 2,
        DRAWING_AREA_X + DRAWING_AREA_WIDTH + 2, DRAWING_AREA_Y + DRAWING_AREA_HEIGHT + 2,
        "#DDDDDD", "#DDDDDD"
    )
    ui_elements.append(drawing_bg)
    
    # White drawing surface
    drawing_surface = canvas.create_rectangle(
        DRAWING_AREA_X, DRAWING_AREA_Y,
        DRAWING_AREA_X + DRAWING_AREA_WIDTH, DRAWING_AREA_Y + DRAWING_AREA_HEIGHT,
        DRAWING_BG_COLOR, "#999999"
    )
    ui_elements.append(drawing_surface)
    
    # Create tool buttons
    tools = ["brush", "rectangle", "circle", "line", "eraser", "clear"]
    button_width = 80
    button_height = 30
    start_x = 20
    start_y = TOOLBAR_HEIGHT + 30
    
    for i, tool in enumerate(tools):
        y = start_y + i * (button_height + 10)
        is_selected = (tool == current_tool)
        
        button = create_button(
            canvas, start_x, y, button_width, button_height,
            tool.capitalize(), is_selected
        )
        button['tool'] = tool
        tool_buttons.append(button)
    
    # Create color palette
    color_size = 25
    colors_per_row = 6
    start_x = 20
    start_y = TOOLBAR_HEIGHT + 350
    
    for i, color in enumerate(colors):
        row = i // colors_per_row
        col = i % colors_per_row
        
        x = start_x + col * (color_size + 5)
        y = start_y + row * (color_size + 5)
        
        color_btn = create_color_button(canvas, x, y, color_size, color)
        color_buttons.append(color_btn)
    
    # Current color indicator
    indicator_x = 20
    indicator_y = TOOLBAR_HEIGHT + 300
    indicator_size = 40
    
    # Color indicator label
    label = canvas.create_text(
        indicator_x, indicator_y - 20, "Current Color :",
        font="Arialbolditalic", font_size=15, color="#2D3748"
    )
    ui_elements.append(label)
    
    # Color indicator
    color_indicator = canvas.create_rectangle(
        indicator_x, indicator_y, indicator_x + indicator_size, indicator_y + indicator_size,
        current_color, "black"
    )
    
    # Instructions
    instructions = [
        "🖱️ Instructions:",
        "• Select a tool from buttons",
        "• Pick a color from palette", 
        "• Draw in the white area",
        "• Brush: Click & drag to draw",
        "• Shapes: Click start, click end",
        "• Eraser: Drag to erase",
        "• Clear: Remove everything"
    ]
    
    start_y = TOOLBAR_HEIGHT + 500
    for i, instruction in enumerate(instructions):
        y = start_y + i * 15
        text = canvas.create_text(
            20, y, instruction,
            font="Arial", font_size=10, color="#4A5568"
        )
        ui_elements.append(text)
    
    def handle_tool_selection(click_x, click_y):
        """Handle tool button clicks"""
        nonlocal current_tool, shape_start_x, shape_start_y 
        
        for button in tool_buttons:
            if point_in_rect(click_x, click_y, 
                             button['x'], button['y'], 
                             button['width'], button['height']):
                
                if button['tool'] == 'clear':
                    for obj in drawing_objects:
                        canvas.delete(obj)
                    drawing_objects.clear()
                    shape_start_x = None 
                    shape_start_y = None
                else:
                    current_tool = button['tool']
                    shape_start_x = None 
                    shape_start_y = None
                    
                    for btn in tool_buttons:
                        is_selected = (btn['tool'] == current_tool)
                        color = SELECTED_COLOR if is_selected else BUTTON_COLOR
                        highlight_color = "#68D391" if is_selected else "#87CEEB"
                        
                        canvas.set_color(btn['rect'], color)
                        canvas.set_color(btn['highlight'], highlight_color)
                        
                return True
        return False
    
    def handle_color_selection(click_x, click_y):
        """Handle color button clicks"""
        nonlocal current_color
        
        for color_btn in color_buttons:
            if point_in_rect(click_x, click_y,
                             color_btn['x'], color_btn['y'],
                             color_btn['size'], color_btn['size']):
                current_color = color_btn['color']
                canvas.set_color(color_indicator, current_color)
                return True
        return False
    
    def draw_brush_stroke(x1, y1, x2, y2):
        """Draw smooth brush stroke"""
        
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if distance > 0:
            steps = max(1, int(distance / 2)) 
            for i in range(steps + 1):
                t = i / max(1, steps)
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                
                circle = canvas.create_oval(
                    x - brush_size, y - brush_size,
                    x + brush_size, y + brush_size,
                    current_color, current_color
                )
                drawing_objects.append(circle)
    
    def erase_at_position(x, y):
        """Erase objects at given position"""
        erase_size = 15
        overlapping = canvas.find_overlapping(
            x - erase_size, y - erase_size,
            x + erase_size, y + erase_size
        )
        
        for obj in list(drawing_objects): 
            if obj in overlapping: 
                canvas.delete(obj)
                drawing_objects.remove(obj)
    
    def handle_drawing_action(x, y):
        """Handle continuous drawing for brush/eraser"""
        nonlocal last_x, last_y
        if not is_in_drawing_area(x, y):
            return 
            
        if current_tool == "brush":
            if last_x is not None and last_y is not None:
                draw_brush_stroke(last_x, last_y, x, y)
            else: 
                circle = canvas.create_oval(
                    x - brush_size, y - brush_size,
                    x + brush_size, y + brush_size,
                    current_color, current_color
                )
                drawing_objects.append(circle)
            last_x = x
            last_y = y
        elif current_tool == "eraser":
            erase_at_position(x, y)
            last_x = x 
            last_y = y 


    def handle_shape_drawing(start_x, start_y, end_x, end_y):
        """Handle shape drawing"""
        if not (is_in_drawing_area(start_x, start_y) and 
                is_in_drawing_area(end_x, end_y)):
            return
            
        shape = None
        if current_tool == "rectangle":
            x1, y1 = min(start_x, end_x), min(start_y, end_y)
            x2, y2 = max(start_x, end_x), max(start_y, end_y)
            shape = canvas.create_rectangle(
                x1, y1, x2, y2,
                color=current_color, # Changed from None to current_color
                outline=current_color 
            )
        elif current_tool == "circle":
            x1, y1 = min(start_x, end_x), min(start_y, end_y)
            x2, y2 = max(start_x, end_x), max(start_y, end_y)
            shape = canvas.create_oval(
                x1, y1, x2, y2,
                color=current_color, # Changed from None to current_color
                outline=current_color 
            )
        elif current_tool == "line":
            shape = canvas.create_line(
                start_x, start_y, end_x, end_y,
                current_color 
            )
            
        if shape:
            drawing_objects.append(shape)
    
    print("✨ Microsoft Paint Clone Ready!")
    print("📝 Click tools and colors, then draw in the white area!")
    print("⌨️  Press 'q' to quit")
    
    # Main application loop
    while True:
        new_clicks = canvas.get_new_mouse_clicks()
        
        current_mouse_x = canvas.get_mouse_x()
        current_mouse_y = canvas.get_mouse_y()

        for click in new_clicks:
            click_x, click_y = click 

            is_mouse_pressed = False 
            
            if not (handle_tool_selection(click_x, click_y) or 
                    handle_color_selection(click_x, click_y)):
                
                if is_in_drawing_area(click_x, click_y):
                    if current_tool in ["brush", "eraser"]:
                        is_mouse_pressed = True 
                        last_x = click_x
                        last_y = click_y
                        handle_drawing_action(click_x, click_y) 
                    elif current_tool in ["rectangle", "circle", "line"]:
                        if shape_start_x is None:
                            shape_start_x = click_x
                            shape_start_y = click_y
                        else:
                            handle_shape_drawing(shape_start_x, shape_start_y, click_x, click_y)
                            shape_start_x = None
                            shape_start_y = None
                else:
                    shape_start_x = None
                    shape_start_y = None


        if is_mouse_pressed and current_tool in ["brush", "eraser"]:
            if current_mouse_x != last_x or current_mouse_y != last_y:
                handle_drawing_action(current_mouse_x, current_mouse_y)
        
        keys = canvas.get_new_key_presses()
        for key in keys:
            if key.lower() == 'q':
                print("👋 Paint application closed!")
                return
            elif key.lower() == 'c':
                for obj in drawing_objects:
                    canvas.delete(obj)
                drawing_objects.clear()
                
                shape_start_x = None 
                shape_start_y = None
                is_mouse_pressed = False 
                last_x = None
                last_y = None
                
        time.sleep(0.01) 

if __name__ == "__main__":
    main()