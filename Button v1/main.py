from graphics import Canvas

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

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

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    # Button properties
    button_x = 125
    button_y = 170
    button_width = 150
    button_height = 60
    button_color = "#4A90E2"
    button_hover_color = "#357ABD"
    button_text = "✨ Click Me! ✨"
    font_size = 16
    
    # Shadow
    shadow_offset = 3
    canvas.create_rectangle(
        button_x + shadow_offset, button_y + shadow_offset, 
        button_x + button_width + shadow_offset, button_y + button_height + shadow_offset,
        "#333333", "#333333"
    )
    
    # Button body
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
    
    # Button text - centered manually
    text_y = button_y + button_height / 2 - font_size / 2
    button_label = draw_centered_text(canvas, button_x + button_width / 2, text_y, button_text, font_size, "white")
    
    # Header text
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 50, "🎯 Interactive Button Demo 🎯", 18, "#2D3748")
    draw_centered_text(canvas, CANVAS_WIDTH / 2 + 18, 80, "Click the beautiful button below!", 12, "#4A5568")
    
    button_clicked = False
    feedback_text = None
    feedback_subtitle = None

    import time
    while True:
        click = canvas.get_last_click()
        if click is not None:
            click_x, click_y = click
            if (button_x <= click_x <= button_x + button_width and 
                button_y <= click_y <= button_y + button_height):
                if not button_clicked:
                    canvas.set_color(button_rect, button_hover_color)
                    canvas.set_color(highlight_rect, "#5A9BD4")
                    feedback_text = draw_centered_text(canvas, CANVAS_WIDTH / 2, button_y + 100, "🎉 Button Activated! 🎉", 16, "#38A169")
                    feedback_subtitle = draw_centered_text(canvas, CANVAS_WIDTH / 2 + 10, button_y + 120, "Click again to reset", 12, "#4A5568")
                    button_clicked = True
                else:
                    canvas.set_color(button_rect, button_color)
                    canvas.set_color(highlight_rect, "#87CEEB")
                    if feedback_text:
                        canvas.delete(feedback_text)
                        canvas.delete(feedback_subtitle)
                        feedback_text = None
                        feedback_subtitle = None
                    button_clicked = False
        time.sleep(0.01)

if __name__ == '__main__':
    main()
