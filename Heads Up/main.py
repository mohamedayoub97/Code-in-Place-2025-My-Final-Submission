from graphics import Canvas
import random
import time

# --- Constants ---
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

BOX_WIDTH = 350
BOX_HEIGHT = 100
SHADOW_OFFSET = 6

FILE_NAME = 'cswords.txt'
DESCRIPTIONS_FILE = 'descriptions.txt' # This file is not directly read, descriptions are hardcoded

# Define elegant and chic color palettes for the creative background
# Updated palettes for more colorful and chic appearance
elegant_palettes = [
    # Palette 1: Soft Sunset Hues with a touch of deep blue
    ["#FAD0C4", "#FFD1DC", "#FFABAB", "#FFC3A0", "#FF677D", "#4B0082"], # Peach, Pink, Light Red, Orange, Deep Pink, Indigo
    # Palette 2: Emerald and Gold with Cream
    ["#FDFCDC", "#D1FFB0", "#8AE89C", "#4CAF50", "#2E8B57", "#B8860B"], # Cream, Light Green, Medium Green, Forest Green, Sea Green, Dark Goldenrod
    # Palette 3: Deep Ocean Blues and Teals with Coral
    ["#E0FFFF", "#AFEEEE", "#7FFFD4", "#40E0D0", "#20B2AA", "#FF7F50"], # Light Cyan, Pale Turquoise, Aquamarine, Turquoise, Light Sea Green, Coral
    # Palette 4: Berry and Plum with Silver Accents
    ["#F5F5DC", "#E6E6FA", "#DDA0DD", "#BA55D3", "#8A2BE2", "#C0C0C0"], # Beige, Lavender, Plum, Medium Orchid, Blue Violet, Silver
    # Palette 5: Earthy Terracotta and Sage with Cream
    ["#FDF5E6", "#FAEBD7", "#D2B48C", "#BDB76B", "#8FBC8F", "#CD853F"], # Old Lace, Antique White, Tan, Dark Khaki, Dark Sea Green, Peru
    # New Palettes added below for more variety and vibrancy
    # Palette 6: Vibrant Tropical Mix
    ["#F0F8FF", "#FFE4E1", "#FFD700", "#32CD32", "#1E90FF", "#FF4500"], # AliceBlue, MistyRose, Gold, LimeGreen, DodgerBlue, OrangeRed
    # Palette 7: Royal and Deep Jewels
    ["#F8F8FF", "#E6E6FA", "#8A2BE2", "#483D8B", "#8B008B", "#FFD700"], # GhostWhite, Lavender, BlueViolet, DarkSlateBlue, DarkMagenta, Gold
    # Palette 8: Soft Grays and Pinks for Modern Chic
    ["#F5F5F5", "#E0E0E0", "#C0C0C0", "#FFC0CB", "#FF69B4", "#708090"], # WhiteSmoke, Gainsboro, Silver, Pink, HotPink, SlateGray
    # Palette 9: Autumnal Warmth
    ["#FFF8DC", "#FAEBD7", "#FF8C00", "#DAA520", "#B22222", "#8B4513"], # Cornsilk, AntiqueWhite, DarkOrange, Goldenrod, FireBrick, SaddleBrown
    # Palette 10: Cool Ocean Depths
    ["#F0F8FF", "#ADD8E6", "#87CEEB", "#4682B4", "#191970", "#6A5ACD"], # AliceBlue, LightBlue, SkyBlue, SteelBlue, MidnightBlue, SlateBlue
    # Palette 11: Pastel Dreams
    ["#FDF0FF", "#F0FFF4", "#E3F2FD", "#F3E5F5", "#FFFDE7", "#FFFAF0"], # Lightest tints of various pastel families
    # Palette 12: Earthy Greens and Browns
    ["#F5F5DC", "#D2B48C", "#A0522D", "#8B4513", "#556B2F", "#6B8E23"], # Beige, Tan, Sienna, SaddleBrown, DarkOliveGreen, OliveDrab
    # Palette 13: Bright and Playful
    ["#FFFFF0", "#F0FFFF", "#F5FFFA", "#FFDAB9", "#FF6347", "#FF1493"], # Ivory, Azure, MintCream, PeachPuff, Tomato, DeepPink
    # Palette 14: Dark and Mysterious
    ["#2F4F4F", "#696969", "#708090", "#A9A9A9", "#B0C4DE", "#483D8B"], # DarkSlateGray, DimGray, SlateGray, DarkGray, LightSteelBlue, DarkSlateBlue
    # Palette 15: Sunny Citrus
    ["#FFFACD", "#FFEFD5", "#FFD700", "#FFA500", "#FF4500", "#FFDAB9"], # LemonChiffon, PapayaWhip, Gold, Orange, OrangeRed, PeachPuff
]

# --- Utility Functions for Graphics ---

def draw_creative_background(canvas, palette_index):
    """
    Draws a creative, elegant, and chic background using shapes and a selected palette.
    """
    canvas.clear() # Clear the canvas before drawing a new background
    colors = elegant_palettes[palette_index]

    # Base background color (lightest from the palette)
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, colors[0], colors[0])

    # Draw various abstract shapes for a layered effect
    num_large_shapes = 5 # Fewer large, subtle shapes
    for _ in range(num_large_shapes):
        shape_type = random.choice(['rectangle', 'oval'])
        color_choice = random.choice(colors[1:len(colors)//2]) # Use lighter accent colors for large shapes
        
        # Make large shapes span a significant portion of the canvas
        x1 = random.randint(-CANVAS_WIDTH // 2, CANVAS_WIDTH)
        y1 = random.randint(-CANVAS_HEIGHT // 2, CANVAS_HEIGHT)
        x2 = x1 + random.randint(CANVAS_WIDTH // 2, CANVAS_WIDTH * 1.5)
        y2 = y1 + random.randint(CANVAS_HEIGHT // 2, CANVAS_HEIGHT * 1.5)
        
        if shape_type == 'rectangle':
            canvas.create_rectangle(x1, y1, x2, y2, color_choice, color_choice)
        elif shape_type == 'oval':
            canvas.create_oval(x1, y1, x2, y2, color_choice, color_choice)

    num_small_shapes = 20 # More numerous, smaller, more colorful shapes
    for _ in range(num_small_shapes):
        shape_type = random.choice(['rectangle', 'oval', 'line'])
        color_choice = random.choice(colors[len(colors)//2:]) # Use darker, more vibrant accent colors

        if shape_type == 'rectangle':
            x1 = random.randint(0, CANVAS_WIDTH)
            y1 = random.randint(0, CANVAS_HEIGHT)
            x2 = random.randint(x1 + 20, x1 + 100) # Smaller rectangles
            y2 = random.randint(y1 + 20, y1 + 100)
            canvas.create_rectangle(x1, y1, x2, y2, color_choice, color_choice)
        elif shape_type == 'oval':
            x1 = random.randint(0, CANVAS_WIDTH)
            y1 = random.randint(0, CANVAS_HEIGHT)
            x2 = random.randint(x1 + 20, x1 + 100) # Smaller ovals
            y2 = random.randint(y1 + 20, y1 + 100)
            canvas.create_oval(x1, y1, x2, y2, color_choice, color_choice)
        elif shape_type == 'line':
            x1 = random.randint(0, CANVAS_WIDTH)
            y1 = random.randint(0, CANVAS_HEIGHT)
            x2 = random.randint(0, CANVAS_WIDTH)
            y2 = random.randint(0, CANVAS_HEIGHT)
            canvas.create_line(x1, y1, x2, y2, color_choice)

    # Add some very small, bright "sparkle" or "dot" elements
    num_sparkles = 15
    for _ in range(num_sparkles):
        sparkle_color = random.choice(colors[1:]) # Can be any accent color
        x = random.randint(0, CANVAS_WIDTH)
        y = random.randint(0, CANVAS_HEIGHT)
        size = random.randint(2, 5)
        canvas.create_oval(x, y, x + size, y + size, sparkle_color, sparkle_color)


def estimate_text_width(text, font_size):
    """
    Estimates the pixel width of text. This is a heuristic and may not be
    perfectly accurate for all fonts or text content.
    """
    # A rough estimate: font_size * 0.6 is a common multiplier for character width
    return font_size * 0.6 * len(text)

def draw_centered_text(canvas, center_x, center_y, text, font_size, color, font='Chalkboardbold'):
    """
    Draws text centered horizontally at a given (center_x, center_y) on the canvas.
    """
    text_width = estimate_text_width(text, font_size)
    # Adjust x to center the text
    return canvas.create_text(center_x - text_width / 2, center_y, text, font=font, font_size=font_size, color=color)

def draw_button(canvas, text, x, y, w, h, main_color="#4CAF50", outline_color="#388E3C"):
    """
    Draws a styled button with shadow and highlights.
    Returns the button's main rectangle object and its bounding box for click detection.
    """
    # Shadow
    canvas.create_rectangle(x + 3, y + 3, x + w + 3, y + h + 3, "#222", "#222")
    # Main button body
    rect = canvas.create_rectangle(x, y, x + w, y + h, main_color, outline_color) # Green button
    # Top highlight
    canvas.create_rectangle(x + 2, y + 2, x + w - 2, y + 15, "#A5D6A7", "#A5D6A7")
    # Button text, slightly offset for visual appeal
    draw_centered_text(canvas, x + w / 2 + 6, y + h / 2 - 5, text, 18, "white")
    return rect, (x, y, w, h)

def is_click_inside(click, bounds):
    """
    Checks if a given click (x, y) coordinate is within a rectangular bounds (bx, by, bw, bh).
    """
    x, y = click
    bx, by, bw, bh = bounds
    return bx <= x <= bx + bw and by <= y <= by + bh

def draw_start_screen(canvas, palette_index):
    """
    Draws the initial start screen with a title, instructions, copyright, and a start button.
    """
    draw_creative_background(canvas, palette_index) # Use the new creative background
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 80, "🧠 Heads Up! 🧠", 40, "#2C3E50")
    draw_centered_text(canvas, CANVAS_WIDTH / 1.75, 130, "Click to Start the Game", 20, "#34495E")
    draw_centered_text(canvas, CANVAS_WIDTH / 1.9, CANVAS_HEIGHT - 30, "© 2025 Mohamed Ayoub Essalami", 12, "black")
    # Position the start button in the center
    button_x = (CANVAS_WIDTH - 150) / 2
    button_y = CANVAS_HEIGHT / 2 - 30
    return draw_button(canvas, "🚀 Start Game 🚀", button_x, button_y, 150, 60)


# --- Game Data Functions ---

def get_words_from_file():
    """
    Reads words from the specified file.
    Includes basic error handling for FileNotFoundError.
    """
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {FILE_NAME} not found. Please ensure 'cswords.txt' exists.")
        return []
    except Exception as e:
        print(f"Error reading words file: {e}")
        return []

def get_descriptions_from_file():
    """
    Returns a hardcoded dictionary of words and their descriptions.
    This function currently does not read from DESCRIPTIONS_FILE.
    """
    descriptions = {
        "Spa M": "🧖‍♀️📚 Possibly a student or participant in the CS106A community!",
        "Jacob H": "👨‍💻🧠 A brilliant mind in the CS106A world!",
        "Piyush G": "🧑‍🏫💡 Always ready to learn and code!",
        "İbrahim A": "🌍💻 A global coder making waves in CS!",
        "Steve": "🧔📱 Could be Steve Jobs or a cool instructor!",
        "Ian M": "👨‍🎓✨ An awesome contributor to the CS106A class!",
        "Krishnendu K": "👨‍💻🔍 Loves solving tricky bugs!",
        "Ioana M": "👩‍💻🌟 A star coder from the CS106A community!",
        "Zara G": "👩‍🎓🚀 Sharp, smart, and coding ahead!",
        "Olivia C": "👩‍💻📘 A curious learner with a coding spark!",
        "Esha": "🌈💡 Bringing bright ideas into Python!",
        "Karel": "🤖🐶 The iconic robot that teaches coding basics!",
        "For Loop": "🔁🧮 A loop that repeats a task a set number of times!",
        "While Loop": "🔄⏳ Repeats as long as a condition is true!",
        "If Statement": "❓✅ Executes code if a condition is true!",
        "Else": "😕➡️ What happens when the 'if' isn't true!",
        "Function": "🔧📦 A reusable block of code that does something cool!",
        "Parameter": "📥🧾 Info you give to a function to work with!",
        "Return Value": "🎁📤 What a function gives back after it's done!",
        "CS106A": "🎓🐍 Stanford's amazing intro to Python class!",
        "Lists": "📋📦 A collection of items stored in one variable!",
        "File Reading": "📂👀 Reading data from a file to use in your program!",
        "Index": "🔢🧭 The position of an item in a list or string!",
        "Print": "🖨️📢 Used to show output on the screen!",
        "Beeper": "📟📍 Used by Karel to mark positions in the world!",
        "Main": "🎬🚀 Where your program starts running!",
        "Input": "⌨️📝 User types something in and your program uses it!",
        "Turn Right": "➡️🤖 Karel turns to the right!",
        "Khansole Academy": "🏫💻 A Khan Academy spin-off project with quizzes and fun!",
        "Diagnostic": "🧪🩺 A test to check your coding health!",
        "String": "🔤💬 A sequence of text characters!",
        "Integer": "🔢✴️ Whole numbers without decimals!",
        "Float": "🌊➗ Numbers with decimal points!",
        "Boolean": "✅❌ True or False values!",
        "Range": "📏📊 Used to generate a sequence of numbers!",
        "Style": "🎨🖌️ The way your code looks and reads!",
        "Graphics": "🖼️🎮 Drawing fun visuals with Python!",
        "Constant": "🔒📏 A value that doesn't change!",
        "Stanford": "🎓❤️ A top university where CS106A is taught!",
        "Code in Place": "🌍💻 A global free coding class from Stanford!",
        "Datascience": "📊🧠 Turning data into insights!",
        "Good Times": "🎉😁 Happy memories from learning to code!",
        "Chris Piech": "👨‍🏫🌟 The amazing professor behind Code in Place!",
        "Mehran Sahami": "👑🐍 A legend in teaching computer science at Stanford!",
        "Burrito": "🌯😋 The unofficial food of CS students!",
        "Toaster": "🍞🔥 Used in fun examples or metaphors!",
        "Suitcase": "🧳🧠 Pack your knowledge and go places!",
        "URL": "🌐🔗 A web address that links to cool content!",
        "Teaching Team": "👩‍🏫🧑‍🏫 The heroes who make learning possible!",
        "Section Leader": "🙋‍♂️🙋‍♀️ Guides you through small group sessions!",
        "Sections": "📚🧑‍🤝‍🧑 Small learning groups to ask questions!",
        "Scribble": "✏️🌀 A fun graphics exercise with randomness!",
        "Random Circles": "⚪🎲 Draw circles in random places and colors!",
        "Starter Code": "🚀💻 Pre-written code to help you begin your projects!",
        "Python": "🐍💡 A fun and powerful programming language!",
        "Bright Simons": "🧠🌍 A name that shines in knowledge and impact!",
        "Variable": "📦🔣 Stores information your program can use!",
        "For Each": "🔁📋 Looping through every item in a list!",
        "Random": "🎲🎯 Unpredictable values for creative code!"
    }
    return descriptions

def print_bubble_description(word, description):
    """
    Prints a formatted bubble description of the word and its clue to the console.
    """
    if not description:
        return
    
    bubble_width = min(80, len(description) + 10)
    top_border = "╭" + "─" * (bubble_width - 2) + "╮"
    bottom_border = "╰" + "─" * (bubble_width - 2) + "╯"
    
    print(f"\n{top_border}")
    print(f"│ 🔤 WORD: {word.upper()}")
    print(f"├{'─' * (bubble_width - 2)}┤")
    
    words = description.split()
    lines = []
    current_line = ""
    max_line_length = bubble_width - 6
    
    for word_desc in words:
        if len(current_line + " " + word_desc) <= max_line_length:
            current_line += " " + word_desc if current_line else word_desc
        else:
            if current_line:
                lines.append(current_line)
            current_line = word_desc
    
    if current_line:
        lines.append(current_line)
    
    for line in lines:
        padding = bubble_width - len(line) - 4
        print(f"│ {line}{' ' * padding} │")
    
    print(f"{bottom_border}")
    print("💭 Think about this clue and guess the word!")
    print("🖱️  Click to reveal the answer...\n")

# --- Main Game Logic ---

def main():
    """
    Main function to run the Heads Up game.
    Manages the start screen, game loop, and end screen.
    """
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    current_palette_index = 0
    last_background_change = time.time()

    # --- Start Screen Loop ---
    # Store button components to delete them later
    button_rect_obj = None
    button_text_obj = None
    button_highlight_obj = None
    button_shadow_obj = None
    button_bounds = None # Initialize button_bounds

    while True:
        # Redraw the start screen with the current creative background
        # This also recreates the button elements, so we need to capture their IDs
        draw_creative_background(canvas, current_palette_index) # Use creative background
        draw_centered_text(canvas, CANVAS_WIDTH / 2, 80, "🧠 Heads Up 🧠", 40, "#2C3E50")
        draw_centered_text(canvas, CANVAS_WIDTH / 1.75, 130, "Click to Start the Game", 20, "#34495E")
        draw_centered_text(canvas, CANVAS_WIDTH / 1.9, CANVAS_HEIGHT - 30, "© 2025 Mohamed Ayoub Essalami", 12, "black")
        
        button_x = (CANVAS_WIDTH - 150) / 2
        button_y = CANVAS_HEIGHT / 2 - 30
        
        # Draw button components separately to get their IDs
        button_shadow_obj = canvas.create_rectangle(button_x + 3, button_y + 3, button_x + 150 + 3, button_y + 60 + 3, "#222", "#222")
        button_rect_obj = canvas.create_rectangle(button_x, button_y, button_x + 150, button_y + 60, "#4CAF50", "#388E3C")
        button_highlight_obj = canvas.create_rectangle(button_x + 2, button_y + 2, button_x + 150 - 2, button_y + 15, "#A5D6A7", "#A5D6A7")
        button_text_obj = draw_centered_text(canvas, button_x + 150 / 2 + 6, button_y + 60 / 2 - 5, "🚀 Start Game 🚀", 18, "white")
        button_bounds = (button_x, button_y, 150, 60) # Update button_bounds

        click = canvas.get_last_click()
        now = time.time()
        
        # Cycle creative background every 3 seconds on the start screen
        if now - last_background_change > 3:
            current_palette_index = (current_palette_index + 1) % len(elegant_palettes)
            # No need to redraw button explicitly here, as the loop will redraw the entire screen
            last_background_change = now

        if click and is_click_inside(click, button_bounds):
            # Simulate button press effect by redrawing with different color
            canvas.delete(button_rect_obj)
            canvas.delete(button_highlight_obj)
            canvas.delete(button_shadow_obj)
            canvas.delete(button_text_obj)
            
            # Draw pressed state
            button_shadow_obj = canvas.create_rectangle(button_x + 3, button_y + 3, button_x + 150 + 3, button_y + 60 + 3, "#111", "#111")
            button_rect_obj = canvas.create_rectangle(button_x, button_y, button_x + 150, button_y + 60, "#2E8B57", "#1E6B47") # Darker green
            button_highlight_obj = canvas.create_rectangle(button_x + 2, button_y + 2, button_x + 150 - 2, button_y + 15, "#7CB342", "#7CB342") # Darker highlight
            button_text_obj = draw_centered_text(canvas, button_x + 150 / 2 + 6, button_y + 60 / 2 - 5, "🚀 Start Game 🚀", 18, "white")
            
            time.sleep(0.5) # Brief pause for the effect
            break # Exit start screen loop
        time.sleep(0.5) # Small delay to prevent busy-waiting

    # --- Game Setup ---
    # Clear the creative background and set the game image background
    canvas.clear()
    canvas.create_image_with_size(
        0, 0,
        CANVAS_WIDTH, CANVAS_HEIGHT,
        "Heads up Game.png"
    )

    words = get_words_from_file()
    descriptions_dict = get_descriptions_from_file()
    
    if not words:
        print("No words loaded. Please check your words file.")
        return
    
    # Create a case-insensitive dictionary for descriptions lookup
    case_insensitive_dict = {}
    for key, value in descriptions_dict.items():
        case_insensitive_dict[key.lower()] = value
    
    word_pairs = []
    for word in words:
        description = descriptions_dict.get(word)
        if not description:
            description = case_insensitive_dict.get(word.lower())
        if not description:
            description = f"No description available for '{word}'"
        word_pairs.append((word, description))
    
    random.shuffle(word_pairs) # Shuffle the words for random order

    word_id = None
    box_id = None
    shadow_id = None
    index = 0

    # --- Main Game Loop ---
    while index < len(word_pairs):
        # The "Heads up Game.png" will persist.
        # The word box and text will be drawn on top of this image.

        clicks = canvas.get_new_mouse_clicks()
        if clicks: # If there's a click, reveal the next word
            for obj in [word_id, box_id, shadow_id]:
                if obj is not None:
                    canvas.delete(obj) # Clear previous word/box

            word, description = word_pairs[index]
            
            print_bubble_description(word, description) # Print description to console

            # Calculate positions for the word box
            top_y = 50
            left_x = (CANVAS_WIDTH - BOX_WIDTH) // 2
            right_x = left_x + BOX_WIDTH
            bottom_y = top_y + BOX_HEIGHT

            center_x = (left_x + right_x) // 2
            center_y = (top_y + bottom_y) // 2

            # Draw the shadow and the word box
            shadow_id = canvas.create_rectangle(
                left_x + SHADOW_OFFSET, top_y + SHADOW_OFFSET,
                right_x + SHADOW_OFFSET, bottom_y + SHADOW_OFFSET,
                color='#34eba5'
            )
            box_id = canvas.create_rectangle(
                left_x, top_y, right_x, bottom_y,
                color='#c3eb34', outline='lightgreen'
            )

            # Draw the word
            word_id = canvas.create_text(
                180 , 85, # Initial arbitrary position, will be moved
                text=word,
                font='Arial bold italic',
                font_size=36,
                color='black'
            )
            
            # Center the word within the box
            text_width = canvas.get_object_width(word_id)
            text_height = canvas.get_object_height(word_id)
            
            if text_width and text_height:
                text_x = center_x - text_width // 2
                text_y = center_y - text_height // 2
            else:
                # Fallback if get_object_width/height returns None
                text_x = center_x - 60
                text_y = center_y - 18
            
            canvas.moveto(word_id, text_x, text_y)

            index += 1 # Move to the next word

        time.sleep(0.5) # Small delay to prevent busy-waiting

    # --- End Screen ---
    canvas.clear()
    # Draw the static game image background for the end screen
    canvas.create_image_with_size(
        0, 0,
        CANVAS_WIDTH, CANVAS_HEIGHT,
        "Heads up Game.png"
    )
    draw_centered_text(
        canvas,
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2 - 50,
        text="🌟🌈💥 All words revealed! 🧠⚡️🎉",
        font_size=25,
        color='white'
    )
    draw_centered_text(
        canvas,
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2,
        text="Thanks for playing! 🤩🎯🥳",
        font_size=25,
        color='white'
    )

    # Add a "Play Again" button
    restart_button_x = (CANVAS_WIDTH - 150) / 2
    restart_button_y = CANVAS_HEIGHT / 2 + 50
    _, restart_bounds = draw_button(canvas, "🔄 Play Again 🔄", restart_button_x, restart_button_y, 150, 60)

    while True:
        click = canvas.get_last_click()
        if click and is_click_inside(click, restart_bounds):
            main() # Restart the game by calling main again (consider alternative for large games)
        time.sleep(0.5) # Delay for restart screen

if __name__ == '__main__':
    main()