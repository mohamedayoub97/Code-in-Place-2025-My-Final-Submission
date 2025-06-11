import math
import time
import random
from graphics import Canvas

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def estimate_text_width(text, font_size):
    return font_size * 0.6 * len(text)

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
    if s == 0.0:
        r = g = b = int(v * 255)
        return r, g, b
    i = int(h * 6)
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
    else:
        r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)

def draw_star(canvas, num_points, outer_radius=80, inner_radius=40, rotation_offset=0, color='yellow'):
    cx = CANVAS_WIDTH / 2
    cy = CANVAS_HEIGHT / 2
    points = []
    total_points = num_points * 2

    for i in range(total_points):
        angle = 2 * math.pi * i / total_points + rotation_offset
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = cx + radius * math.sin(angle)
        y = cy - radius * math.cos(angle)
        points.extend([x, y])

    star_id = canvas.create_polygon(*points)
    canvas.set_color(star_id, color)
    return star_id

def draw_cosmic_star(canvas, num_points, outer_radius=80, inner_radius=40, rotation_offset=0):
    cx = CANVAS_WIDTH / 2
    cy = CANVAS_HEIGHT / 2
    
    # Create cosmic effect with multiple layers
    layers = 15
    for i in range(layers):
        factor = i / layers
        current_outer = outer_radius * (1 - factor * 0.9)
        current_inner = inner_radius * (1 - factor * 0.9)
        
        # Create space-like colors
        h = (factor * 0.7 + 0.6) % 1.0  # Blues and purples
        s = 0.8 + factor * 0.2
        v = 0.9 - factor * 0.4
        r, g, b = hsv_to_rgb(h, s, v)
        
        # Add some sparkle
        r = min(255, r + random.randint(-20, 40))
        g = min(255, g + random.randint(-20, 40))
        b = min(255, b + random.randint(-10, 50))
        
        color = rgb_to_hex(r, g, b)
        draw_star(canvas, num_points, current_outer, current_inner, rotation_offset, color)

def draw_fire_star(canvas, num_points, outer_radius=80, inner_radius=40, rotation_offset=0):
    cx = CANVAS_WIDTH / 2
    cy = CANVAS_HEIGHT / 2
    
    layers = 12
    for i in range(layers):
        factor = i / layers
        current_outer = outer_radius * (1 - factor * 0.85)
        current_inner = inner_radius * (1 - factor * 0.85)
        
        # Fire colors: red, orange, yellow
        if factor < 0.3:
            r, g, b = 255, int(255 * factor * 3), 0  # Red to orange
        elif factor < 0.7:
            r, g, b = 255, 255, int(255 * (factor - 0.3) * 2.5)  # Orange to yellow
        else:
            r, g, b = 255, 255, 200 + int(55 * (factor - 0.7) * 3.33)  # Yellow to white
        
        color = rgb_to_hex(r, g, b)
        draw_star(canvas, num_points, current_outer, current_inner, rotation_offset, color)

def draw_ocean_star(canvas, num_points, outer_radius=80, inner_radius=40, rotation_offset=0):
    cx = CANVAS_WIDTH / 2
    cy = CANVAS_HEIGHT / 2
    
    layers = 10
    for i in range(layers):
        factor = i / layers
        current_outer = outer_radius * (1 - factor * 0.8)
        current_inner = inner_radius * (1 - factor * 0.8)
        
        # Ocean colors: deep blue to aqua
        h = 0.5 + factor * 0.15  # Cyan to blue range
        s = 0.9 - factor * 0.3
        v = 0.4 + factor * 0.5
        r, g, b = hsv_to_rgb(h, s, v)
        
        color = rgb_to_hex(r, g, b)
        draw_star(canvas, num_points, current_outer, current_inner, rotation_offset, color)

def draw_dynamic_background(canvas, theme="cosmic"):
    if theme == "cosmic":
        # Dark space background with stars
        canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, "#0a0a2e", "#0a0a2e")
        # Add sparkles
        for _ in range(50):
            x = random.randint(0, CANVAS_WIDTH)
            y = random.randint(0, CANVAS_HEIGHT)
            size = random.randint(1, 3)
            canvas.create_oval(x, y, x+size, y+size, "#ffffff", "#ffffff")
    elif theme == "fire":
        # Gradient fire background
        for i in range(20):
            factor = i / 20
            r = int(20 + factor * 40)
            g = int(10 + factor * 20)
            b = int(5 + factor * 10)
            color = rgb_to_hex(r, g, b)
            stripe_width = CANVAS_WIDTH // 20
            canvas.create_rectangle(i * stripe_width, 0, (i + 1) * stripe_width, CANVAS_HEIGHT, color, color)
    elif theme == "ocean":
        # Ocean wave background
        for i in range(25):
            factor = i / 25
            wave_offset = int(20 * math.sin(factor * math.pi * 4))
            r = int(10 + factor * 30)
            g = int(50 + factor * 80)
            b = int(80 + factor * 100)
            color = rgb_to_hex(r, g, b)
            stripe_width = CANVAS_WIDTH // 25
            canvas.create_rectangle(i * stripe_width, wave_offset, (i + 1) * stripe_width, CANVAS_HEIGHT, color, color)
    else:
        # Default gradient
        for i in range(20):
            base_color = 230 + random.randint(-20, 20)
            r = min(255, max(0, base_color + random.randint(-15, 15)))
            g = min(255, max(0, base_color + random.randint(-15, 15)))
            b = min(255, max(0, base_color + random.randint(-10, 20)))
            color = rgb_to_hex(r, g, b)
            stripe_width = CANVAS_WIDTH // 20
            canvas.create_rectangle(i * stripe_width, 0, (i + 1) * stripe_width, CANVAS_HEIGHT, color, color)

def create_volume_style_button(canvas, x, y, width, height, text, is_selected=False, color_theme="blue"):
    """Create a button with volume control styling"""
    # Color themes
    themes = {
        "blue": {"base": "#4A90E2", "light": "#6BB6FF", "dark": "#357ABD", "text": "#FFFFFF"},
        "green": {"base": "#7ED321", "light": "#A8E6CF", "dark": "#5CB85C", "text": "#FFFFFF"},
        "red": {"base": "#D0021B", "light": "#FF6B6B", "dark": "#C9302C", "text": "#FFFFFF"},
        "purple": {"base": "#9013FE", "light": "#B368FC", "dark": "#7B1FA2", "text": "#FFFFFF"},
        "orange": {"base": "#FF9500", "light": "#FFB74D", "dark": "#F57C00", "text": "#FFFFFF"},
        "cosmic": {"base": "#2E1065", "light": "#5B21B6", "dark": "#1E1B4B", "text": "#E0E7FF"},
        "fire": {"base": "#DC2626", "light": "#EF4444", "dark": "#B91C1C", "text": "#FEF2F2"},
        "ocean": {"base": "#0891B2", "light": "#22D3EE", "dark": "#0E7490", "text": "#F0F9FF"}
    }
    
    theme = themes.get(color_theme, themes["blue"])
    
    # Outer shadow
    shadow = canvas.create_rectangle(
        x + 2, y + 2, x + width + 2, y + height + 2,
        "#00000030", "#00000030"
    )
    
    # Main button body
    if is_selected:
        button_rect = canvas.create_rectangle(
            x, y, x + width, y + height,
            theme["light"], theme["dark"]
        )
    else:
        button_rect = canvas.create_rectangle(
            x, y, x + width, y + height,
            theme["base"], theme["dark"]
        )
    
    # Inner highlight
    highlight = canvas.create_rectangle(
        x + 2, y + 2, x + width - 2, y + height // 3,
        theme["light"] + "80", theme["light"] + "80"
    )
    
    # Button text
    text_y = y + height // 2 - 6
    text_obj = draw_centered_text(canvas, x + width // 2, text_y, text, 12, theme["text"])
    
    return {
        'shadow': shadow,
        'rect': button_rect,
        'highlight': highlight,
        'text': text_obj,
        'x': x, 'y': y, 'width': width, 'height': height,
        'theme': theme
    }

def create_slider_control(canvas, x, y, width, height, min_val, max_val, current_val, label):
    """Create a volume-style slider control"""
    # Background track
    track_y = y + height // 2 - 3
    track = canvas.create_rectangle(x, track_y, x + width, track_y + 6, "#E5E7EB", "#D1D5DB")
    
    # Progress fill
    progress_width = int(width * (current_val - min_val) / (max_val - min_val))
    progress = canvas.create_rectangle(x, track_y, x + progress_width, track_y + 6, "#4A90E2", "#357ABD")
    
    # Knob
    knob_x = x + progress_width - 8
    knob_y = track_y - 4
    knob_shadow = canvas.create_oval(knob_x + 2, knob_y + 2, knob_x + 18, knob_y + 18, "#00000020", "#00000020")
    knob = canvas.create_oval(knob_x, knob_y, knob_x + 16, knob_y + 16, "#FFFFFF", "#E5E7EB")
    knob_highlight = canvas.create_oval(knob_x + 2, knob_y + 2, knob_x + 10, knob_y + 8, "#F9FAFB", "#F9FAFB")
    
    # Label and value
    label_text = draw_centered_text(canvas, x + width // 2, y - 20, label, 12, "#374151")
    value_text = draw_centered_text(canvas, x + width // 2, y + height + 15, str(current_val), 14, "#1F2937")
    
    return {
        'track': track,
        'progress': progress,
        'knob': knob,
        'knob_shadow': knob_shadow,
        'knob_highlight': knob_highlight,
        'label': label_text,
        'value': value_text,
        'x': x, 'y': y, 'width': width, 'height': height,
        'min_val': min_val, 'max_val': max_val, 'current_val': current_val
    }

def update_slider(canvas, slider, new_val):
    """Update slider position and value"""
    slider['current_val'] = max(slider['min_val'], min(slider['max_val'], new_val))
    
    # Update progress
    progress_width = int(slider['width'] * (slider['current_val'] - slider['min_val']) / (slider['max_val'] - slider['min_val']))
    canvas.delete(slider['progress'])
    track_y = slider['y'] + slider['height'] // 2 - 3
    slider['progress'] = canvas.create_rectangle(slider['x'], track_y, slider['x'] + progress_width, track_y + 6, "#4A90E2", "#357ABD")
    
    # Update knob position
    knob_x = slider['x'] + progress_width - 8
    knob_y = track_y - 4
    canvas.delete(slider['knob_shadow'])
    canvas.delete(slider['knob'])
    canvas.delete(slider['knob_highlight'])
    
    slider['knob_shadow'] = canvas.create_oval(knob_x + 2, knob_y + 2, knob_x + 18, knob_y + 18, "#00000020", "#00000020")
    slider['knob'] = canvas.create_oval(knob_x, knob_y, knob_x + 16, knob_y + 16, "#FFFFFF", "#E5E7EB")
    slider['knob_highlight'] = canvas.create_oval(knob_x + 2, knob_y + 2, knob_x + 10, knob_y + 8, "#F9FAFB", "#F9FAFB")
    
    # Update value text
    canvas.change_text(slider['value'], str(slider['current_val']))

def is_button_clicked(button, click_x, click_y):
    return (button['x'] <= click_x <= button['x'] + button['width'] and
            button['y'] <= click_y <= button['y'] + button['height'])

def is_slider_clicked(slider, click_x, click_y):
    return (slider['x'] <= click_x <= slider['x'] + slider['width'] and
            slider['y'] <= click_y <= slider['y'] + slider['height'])

def get_slider_value_from_click(slider, click_x):
    relative_x = click_x - slider['x']
    relative_x = max(0, min(slider['width'], relative_x))
    ratio = relative_x / slider['width']
    return int(slider['min_val'] + ratio * (slider['max_val'] - slider['min_val']))

def draw_points_screen(canvas, star_points):
    """Draw the points selection screen"""
    canvas.clear()
    draw_dynamic_background(canvas, "default")
    
    # Header
    draw_centered_text(canvas, CANVAS_WIDTH//2+5, 50, "STAR POINTS SELECTOR", 20, "#1F2937")
    draw_centered_text(canvas, CANVAS_WIDTH//2+35, 80, "Choose the complexity of your star", 12, "#6B7280")
    
    # Current selection display
    draw_centered_text(canvas, CANVAS_WIDTH//2+30, 110, f"Selected: {star_points} Points", 16, "#059669")
    
    # Slider for points
    points_slider = create_slider_control(canvas, 120, 155, 300, 20, 3, 20, star_points, "Number of Points")
    
    # Quick select buttons
    quick_buttons = []
    quick_values = [5, 6, 8, 12, 16]
    button_width = 50
    start_x = (CANVAS_WIDTH - (len(quick_values) * button_width + (len(quick_values)-1) * 10)) // 2
    
    for i, val in enumerate(quick_values):
        x = start_x + i * (button_width + 10)
        is_selected = (val == star_points)
        button = create_volume_style_button(canvas, x, 220, button_width, 35, str(val), is_selected, "blue")
        button['value'] = val
        quick_buttons.append(button)
    
    # Navigation
    next_button = create_volume_style_button(canvas, 200, 300, 100, 45, "NEXT →", False, "green")
    
    return points_slider, quick_buttons, next_button

def draw_rotation_screen(canvas, rotation_angle):
    """Draw the rotation selection screen"""
    canvas.clear()
    draw_dynamic_background(canvas, "default")
    
    # Header
    draw_centered_text(canvas, CANVAS_WIDTH//2, 50, "ROTATION CONTROL", 20, "#1F2937")
    draw_centered_text(canvas, CANVAS_WIDTH//2+35, 80, "Set the orientation of your star", 12, "#6B7280")
    
    # Current selection
    draw_centered_text(canvas, CANVAS_WIDTH//2+25, 110, f"Rotation: {rotation_angle}°", 16, "#DC2626")
    
    # Rotation slider
    rotation_slider = create_slider_control(canvas, 120, 155, 300, 20, 0, 360, rotation_angle, "Rotation (Degrees)")
    
    # Preset buttons
    preset_buttons = []
    presets = [0, 45, 90, 135, 180, 225, 270, 315]
    cols = 4
    button_width = 60
    start_x = (CANVAS_WIDTH - (cols * button_width + (cols-1) * 10)) // 2
    
    for i, angle in enumerate(presets):
        row = i // cols
        col = i % cols
        x = start_x + col * (button_width + 10)
        y = 220 + row * 45
        is_selected = (angle == rotation_angle)
        button = create_volume_style_button(canvas, x, y, button_width, 35, f"{angle}°", is_selected, "red")
        button['value'] = angle
        preset_buttons.append(button)
    
    # Navigation
    back_button = create_volume_style_button(canvas, 150, 350, 80, 40, "← BACK", False, "orange")
    next_button = create_volume_style_button(canvas, 270, 350, 80, 40, "NEXT →", False, "green")
    
    return rotation_slider, preset_buttons, back_button, next_button

def draw_style_screen(canvas, style_choice):
    """Draw the style selection screen"""
    canvas.clear()
    draw_dynamic_background(canvas, "default")
    
    # Header
    draw_centered_text(canvas, CANVAS_WIDTH//2, 50, "STYLE SELECTION", 20, "#1F2937")
    draw_centered_text(canvas, CANVAS_WIDTH//2+27.5, 80, "Choose your star's visual theme", 12, "#6B7280")
    
    # Style options with previews
    styles = [
        {"name": "🌌 Cosmic", "value": "cosmic", "theme": "cosmic", "desc": "Deep space magic"},
        {"name": "🔥 Fire", "value": "fire", "theme": "fire", "desc": "Blazing intensity"},
        {"name": "🌊 Ocean", "value": "ocean", "theme": "ocean", "desc": "Aquatic serenity"},
        {"name": "💎 Solid", "value": "solid", "theme": "blue", "desc": "Classic elegance"}
    ]
    
    style_buttons = []
    for i, style in enumerate(styles):
        row = i // 2
        col = i % 2
        x = 75 + col * 180
        y = 150 + row * 100
        
        is_selected = (style["value"] == style_choice)
        button = create_volume_style_button(canvas, x, y, 150, 70, style["name"], is_selected, style["theme"])
        button['value'] = style["value"]
        
        # Description
        draw_centered_text(canvas, x + 75, y + 80, style["desc"], 10, "#6B7280")
        
        style_buttons.append(button)
    
    # Navigation
    back_button = create_volume_style_button(canvas, 150, 400, 80, 40, "← BACK", False, "orange")
    create_btn = create_volume_style_button(canvas, 270, 400, 80, 40, "CREATE!", False, "purple")
    
    return style_buttons, back_button, create_btn

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    # State variables
    star_points = 5
    rotation_angle = 0
    style_choice = "cosmic"  # cosmic, fire, ocean, solid
    current_screen = "start"
    
    while True:
        if current_screen == "start":
            canvas.clear()
            draw_dynamic_background(canvas, "default")
            
            # Welcome screen with animated title
            draw_centered_text(canvas, CANVAS_WIDTH//2-22, 120, "✨ STELLAR FORGE ✨", 30, "#2D1B69")
            draw_centered_text(canvas, CANVAS_WIDTH//2+30, 170, "Craft Your Perfect Star", 16, "#4B5563")
            draw_centered_text(canvas, CANVAS_WIDTH//2+30, 200, "Professional Star Creation Studio", 12, "#6B7280")
            
            # Animated decorative elements
            for i in range(8):
                angle = i * math.pi / 4
                x = CANVAS_WIDTH//2 + 80 * math.cos(angle)
                y = 140 + 30 * math.sin(angle)
                canvas.create_oval(x-2, y-2, x+2, y+2, "#8B5CF6", "#8B5CF6")
            
            start_button = create_volume_style_button(canvas, 175, 250, 150, 60, "🚀 START CRAFTING", False, "purple")
            
            while current_screen == "start":
                click = canvas.get_last_click()
                if click and is_button_clicked(start_button, click[0], click[1]):
                    current_screen = "points"
                    break
                time.sleep(0.01)
            
        elif current_screen == "points":
            # Draw the screen and get UI elements
            points_slider, quick_buttons, next_button = draw_points_screen(canvas, star_points)
            
            while current_screen == "points":
                click = canvas.get_last_click()
                if click:
                    click_x, click_y = click
                    
                    # Check slider
                    if is_slider_clicked(points_slider, click_x, click_y):
                        new_val = get_slider_value_from_click(points_slider, click_x)
                        star_points = new_val
                        update_slider(canvas, points_slider, new_val)
                        # Redraw the selection display
                        #draw_centered_text(canvas, CANVAS_WIDTH//2, 110, f"Selected: {star_points} Points        ", 16, "#059669")
                    
                    # Check quick buttons
                    button_clicked = False
                    for button in quick_buttons:
                        if is_button_clicked(button, click_x, click_y):
                            star_points = button['value']
                            button_clicked = True
                            break
                    
                    if button_clicked:
                        # Redraw the entire screen to update button selection states
                        points_slider, quick_buttons, next_button = draw_points_screen(canvas, star_points)
                    
                    # Check next button
                    if is_button_clicked(next_button, click_x, click_y):
                        current_screen = "rotation"
                        break
                
                time.sleep(0.01)
            
        elif current_screen == "rotation":
            # Draw the screen and get UI elements
            rotation_slider, preset_buttons, back_button, next_button = draw_rotation_screen(canvas, rotation_angle)
            
            while current_screen == "rotation":
                click = canvas.get_last_click()
                if click:
                    click_x, click_y = click
                    
                    # Check slider
                    if is_slider_clicked(rotation_slider, click_x, click_y):
                        new_val = get_slider_value_from_click(rotation_slider, click_x)
                        rotation_angle = new_val
                        update_slider(canvas, rotation_slider, new_val)
                        # Redraw the selection display
                        #draw_centered_text(canvas, CANVAS_WIDTH//2, 110, f"Rotation: {rotation_angle}°        ", 16, "#DC2626")
                    
                    # Check preset buttons
                    button_clicked = False
                    for button in preset_buttons:
                        if is_button_clicked(button, click_x, click_y):
                            rotation_angle = button['value']
                            button_clicked = True
                            break
                    
                    if button_clicked:
                        # Redraw the entire screen to update button selection states
                        rotation_slider, preset_buttons, back_button, next_button = draw_rotation_screen(canvas, rotation_angle)
                    
                    # Check navigation
                    if is_button_clicked(back_button, click_x, click_y):
                        current_screen = "points"
                        break
                    elif is_button_clicked(next_button, click_x, click_y):
                        current_screen = "style"
                        break
                
                time.sleep(0.01)
            
        elif current_screen == "style":
            # Draw the screen and get UI elements
            style_buttons, back_button, create_btn = draw_style_screen(canvas, style_choice)
            
            while current_screen == "style":
                click = canvas.get_last_click()
                if click:
                    click_x, click_y = click
                    
                    # Check style buttons
                    button_clicked = False
                    for button in style_buttons:
                        if is_button_clicked(button, click_x, click_y):
                            style_choice = button['value']
                            button_clicked = True
                            break
                    
                    if button_clicked:
                        # Redraw the entire screen to update button selection states
                        style_buttons, back_button, create_btn = draw_style_screen(canvas, style_choice)
                    
                    # Check navigation
                    if is_button_clicked(back_button, click_x, click_y):
                        current_screen = "rotation"
                        break
                    elif is_button_clicked(create_btn, click_x, click_y):
                        current_screen = "final"
                        break
                
                time.sleep(0.01)
            
        elif current_screen == "final":
            canvas.clear()
            draw_dynamic_background(canvas, style_choice)
            
            # Create the star
            rotation_radians = math.radians(rotation_angle)
            
            if style_choice == "cosmic":
                draw_cosmic_star(canvas, star_points, outer_radius=120, inner_radius=60, rotation_offset=rotation_radians)
            elif style_choice == "fire":
                draw_fire_star(canvas, star_points, outer_radius=120, inner_radius=60, rotation_offset=rotation_radians)
            elif style_choice == "ocean":
                draw_ocean_star(canvas, star_points, outer_radius=120, inner_radius=60, rotation_offset=rotation_radians)
            else:
                # Solid colors
                colors = ['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
                color = random.choice(colors)
                draw_star(canvas, star_points, outer_radius=120, inner_radius=60, rotation_offset=rotation_radians, color=color)
            
            # Info display
            draw_centered_text(canvas, CANVAS_WIDTH//2-21, 50, "✨ STELLAR MASTERPIECE ✨", 25, "#FFFFFF")
            
            # Specs panel
            specs_y = 420
            draw_centered_text(canvas, CANVAS_WIDTH//2+35, specs_y, 
                               f"Points: {star_points} | Rotation: {rotation_angle}° | Style: {style_choice.title()}", 
                               11, "#E5E7EB")
            
            # Action buttons
            new_button = create_volume_style_button(canvas, 120, 450, 100, 40, "NEW STAR", False, "green")
            save_button = create_volume_style_button(canvas, 230, 450, 70, 40, "SAVE", False, "blue")
            exit_button = create_volume_style_button(canvas, 310, 450, 70, 40, "EXIT", False, "red")
            
            while current_screen == "final":
                click = canvas.get_last_click()
                if click:
                    click_x, click_y = click
                    if is_button_clicked(new_button, click_x, click_y):
                        current_screen = "start"  # Go back to the start to create a new star
                        break
                    elif is_button_clicked(save_button, click_x, click_y):
                        print("SAVE button clicked! (Implement save functionality here)")
                        # You would typically implement saving the star's image here.
                        # For example: canvas.save_to_file("my_star.png")
                        pass 
                    elif is_button_clicked(exit_button, click_x, click_y):
                        #canvas.close() # Close the canvas
                        return # Exit the main loop and the program
                time.sleep(0.01)

if __name__ == '__main__':
    main()