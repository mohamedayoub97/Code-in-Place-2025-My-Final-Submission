from graphics import Canvas
import math
import time
import random

# --- Constants ---
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

# Solar System Parameters
SOLAR_SYSTEM_DATA = [
    {"name": "Sun", "radius_au": 0, "period_years": 0, "size_px": 50, "color": "#FFD700", "description": "The Sun is the star at the center of the Solar System and by far the most important source of energy for life on Earth. It is a nearly perfect sphere of hot plasma, heated to incandescence by nuclear fusion reactions in its core. The Sun has been an object of veneration in many cultures throughout human history. It is a G-type main-sequence star, meaning it fuses hydrogen into helium in its core and is currently in the most stable phase of its life. The Sun's enormous gravitational pull keeps all the planets, dwarf planets, asteroids, and comets in orbit around it.\n\nRadius: 695,700 km\nLength of day: 27 Earth days (at equator)\nDistance from the Sun: 0 km (center)\nGravity: 274 m/s²\nSurface area: 6.09 × 10^12 km²\nMass: 1.989 × 10^30 kg (330,000 Earths)\nComposition: Approximately 73% Hydrogen, 25% Helium, and trace amounts of other elements."}, # Gold
    {"name": "Mercury", "radius_au": 0.39, "period_years": 0.24, "size_px": 8, "color": "#A9A9A9", "description": "Mercury is the smallest planet in our Solar System and the closest to the Sun. Its orbit around the Sun takes just 88 Earth days, the shortest of all the planets. Mercury is a terrestrial planet, meaning it has a rocky body, and is heavily cratered, similar to the Moon. It has virtually no atmosphere to trap heat, resulting in extreme temperature swings between day (up to 430°C) and night (down to -180°C). Its surface features include plains, scarps (cliffs), and a large impact basin called Caloris Basin.\n\nRadius: 2,439.7 km\nLength of day: 58 Earth days, 15 hours, 30 minutes\nDistance from the Sun: 57.9 million km\nGravity: 3.7 m/s²\nSurface area: 7.48 × 10^7 km²\nMass: 3.301 × 10^23 kg (0.055 Earths)\nNotable Feature: Very eccentric orbit and a 3:2 spin-orbit resonance."}, # DarkGray
    {"name": "Venus", "radius_au": 0.72, "period_years": 0.62, "size_px": 12, "color": "#FFDAB9", "description": "Venus is the second planet from the Sun, often called Earth's 'sister planet' due to their similar size, mass, and bulk composition. However, Venus is dramatically different, with a dense, toxic atmosphere of carbon dioxide and thick, yellowish clouds of sulfuric acid. It has the hottest surface of any planet in our Solar System, with temperatures averaging 462°C (864°F), hot enough to melt lead. This extreme heat is due to a runaway greenhouse effect. Venus rotates in the opposite direction to most planets, meaning the Sun rises in the west and sets in the east.\n\nRadius: 6,051.8 km\nLength of day: 243 Earth days (retrograde)\nDistance from the Sun: 108.2 million km\nGravity: 8.87 m/s²\nSurface area: 4.60 × 10^8 km²\nMass: 4.867 × 10^24 kg (0.815 Earths)\nAtmosphere: Dense CO2 with sulfuric acid clouds."}, # PeachPuff
    {"name": "Earth", "radius_au": 1.0, "period_years": 1.0, "size_px": 14, "color": "#4169E1", "description": "Earth is the third planet from the Sun and the only astronomical object known to harbor life. About 71% of Earth's surface is covered by water, mostly by oceans, and the remaining 29% is land consisting of continents and islands. Earth's atmosphere, composed primarily of nitrogen and oxygen, protects life from harmful solar radiation and allows for a stable climate. It has one natural satellite, the Moon, which influences tides and stabilizes Earth's axial tilt.\n\nRadius: 6,371 km\nLength of day: 23 hours, 56 minutes, 4 seconds\nDistance from the Sun: 149.6 million km\nGravity: 9.81 m/s²\nSurface area: 5.10 × 10^8 km²\nMass: 5.972 × 10^24 kg (1 Earth Mass)\nUnique Feature: Presence of liquid water and diverse ecosystems."}, # RoyalBlue
    {"name": "Mars", "radius_au": 1.52, "period_years": 1.88, "size_px": 10, "color": "#CD5C5C", "description": "Mars is the fourth planet from the Sun and the second smallest planet in the Solar System, after Mercury. It is often referred to as the 'Red Planet' due to its reddish appearance, which is caused by iron oxide (rust) on its surface. Mars is a terrestrial planet with a thin atmosphere, polar ice caps, and surface features reminiscent of both the impact craters of the Moon and the valleys, deserts, and polar ice caps of Earth. Scientists continue to search for signs of past or present life on Mars, with evidence suggesting liquid water once flowed on its surface. It has two small moons, Phobos and Deimos.\n\nRadius: 3,389.5 km\nLength of day: 24 hours, 37 minutes\nDistance from the Sun: 227.9 million km\nGravity: 3.72 m/s²\nSurface area: 1.45 × 10^8 km²\nMass: 6.417 × 10^23 kg (0.107 Earths)\nMoons: Phobos, Deimos."}, # IndianRed
    {"name": "Jupiter", "radius_au": 5.2, "period_years": 11.86, "size_px": 30, "color": "#FFA07A", "description": "Jupiter est la cinquième planète du Système solaire par ordre d'éloignement au Soleil, et la plus grande par la taille et la masse devant Saturne, qui est comme elle une planète géante gazeuse. Jupiter est composée principalement d'hydrogène et d'hélium et est connue pour ses bandes et ses tourbillons proéminents, qui sont des nuages froids et venteux d'ammoniac et d'eau. La Grande Tache Rouge, une tempête géante plus grande que la Terre, est observée depuis des siècles. Jupiter possède un système d'anneaux faibles et un grand nombre de lunes, dont les quatre plus grandes sont les lunes galiléennes.\n\nLunes : Europe, Io, Ganymède, Callisto, Amalthée, Lysithée, Euporie\nRayon : 69 911 km\nDurée du jour : 0j 9h 56m\nDistance du Soleil : 778,5 millions km\nGravité : 24,79 m/s²\nSuperficie : 61,42 milliards km²\nMasse : 1,898 × 10^27 kg (317,8 M⊕)\nComposition: Principalement hydrogène et hélium."}, # LightSalmon
    {"name": "Saturn", "radius_au": 9.58, "period_years": 29.46, "size_px": 25, "color": "#DAA520", "description": "Saturn is the sixth planet from the Sun and the second-largest in the Solar System, after Jupiter. It is best known for its prominent and beautiful ring system, which is made up of billions of small chunks of ice and rock. Saturn is also a gas giant, composed mostly of hydrogen and helium. It has numerous moons, with Titan being the largest and the only moon in the Solar System known to have a dense atmosphere and stable bodies of surface liquid. The rings are incredibly thin, yet span hundreds of thousands of kilometers.\n\nRadius: 58,232 km\nLength of day: 10 hours, 33 minutes\nDistance from the Sun: 1.434 billion km\nGravity: 10.44 m/s²\nSurface area: 4.27 × 10^10 km²\nMass: 5.683 × 10^26 kg (95.16 Earths)\nNotable Feature: Extensive and complex ring system."}, # Goldenrod
    {"name": "Uranus", "radius_au": 19.2, "period_years": 84.01, "size_px": 20, "color": "#AFEEEE", "description": "Uranus is the seventh planet from the Sun and the third-largest in diameter. It is an ice giant, composed mostly of various ices (water, methane, ammonia) over a small rocky core. Its most distinctive feature is its axial tilt, which is nearly parallel to its orbit, causing it to effectively roll on its side as it orbits the Sun. This results in extreme seasonal variations, with each pole experiencing 42 years of continuous sunlight followed by 42 years of darkness. It has a faint ring system and numerous moons.\n\nRadius: 25,362 km\nLength of day: 17 hours, 14 minutes (retrograde)\nDistance from the Sun: 2.871 billion km\nGravity: 8.69 m/s²\nSurface area: 8.08 × 10^9 km²\nMass: 8.681 × 10^25 kg (14.53 Earths)\nComposition: Primarily ices and rock."}, # PaleTurquoise
    {"name": "Neptune", "radius_au": 30.1, "period_years": 164.79, "size_px": 18, "color": "#4682B4", "description": "Neptune is the eighth and farthest known planet from the Sun in the Solar System. It is an ice giant, similar to Uranus, and is slightly smaller than Uranus but more massive. Neptune is known for its strong winds, which can reach supersonic speeds, and its dynamic weather systems, including the Great Dark Spot, a storm similar to Jupiter's Great Red Spot but shorter-lived. Its blue color is due to the presence of methane in its atmosphere. Neptune has a faint ring system and 14 known moons, with Triton being the largest.\n\nRadius: 24,622 km\nLength of day: 16 hours, 6 minutes\nDistance from the Sun: 4.495 billion km\nGravity: 11.15 m/s²\nSurface area: 7.619 × 10^9 km²\nMass: 1.024 × 10^26 kg (17.15 Earths)\nMoons: Triton (largest), Nereid, Naiad, Thalassa, Despina, Galatea, Larissa, Proteus, Halimede, Psamathe, Sao, Laomedeia, Neso, S/2004 N 1."}, # SteelBlue
    {"name": "Pluto", "radius_au": 39.5, "period_years": 248.0, "size_px": 6, "color": "#DDA0DD", "description": "Pluto is a dwarf planet in the Kuiper belt, a ring of bodies beyond Neptune's orbit. It was discovered in 1930 and was long considered the ninth planet, but was reclassified as a dwarf planet in 2006. Pluto has a complex surface with mountains, valleys, plains, and craters. It has five known moons, the largest of which is Charon, which is so large relative to Pluto that they are sometimes considered a binary system. Pluto's atmosphere is thin and collapses as it moves further from the Sun.\n\nRadius: 1,188.3 km\nLength of day: 6 Earth days, 9 hours, 17 minutes (retrograde)\nDistance from the Sun: 5.906 billion km\nGravity: 0.62 m/s²\nSurface area: 1.77 × 10^7 km²\nMass: 1.303 × 10^22 kg (0.0022 Earths)\nMoons: Charon, Styx, Nix, Kerberos, Hydra."}, # Plum (Dwarf Planet)
]

# Simulation speed
TIME_STEP = 0.05

# Star properties for the background
NUM_STARS = 200
STAR_COLORS = ["#FFFFFF", "#F0F8FF", "#ADD8E6", "#FFFACD"] # White, AliceBlue, LightBlue, LemonChiffon

# Define elegant and chic color palettes for the creative background
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

def estimate_text_width(text, font_size):
    """
    Estimates the width of the text based on font size and length.
    This is a rough estimation; actual text width depends on font and platform.
    Adjusted factor for better centering.
    """
    # This factor is a heuristic. It might need fine-tuning depending on the exact font rendering.
    # Increased the multiplier slightly to improve centering for all text.
    return font_size * 0.45 * len(text)

def draw_centered_text(canvas, center_x, center_y, text, font_size, color, font='Arial'):
    """
    Draws text centered at the given (center_x, center_y) coordinates on the canvas.
    """
    text_width = estimate_text_width(text, font_size)
    draw_x = center_x - text_width / 2  # Shift x left to center the text
    return canvas.create_text(
        draw_x,
        center_y,
        text=text,
        font=font,
        font_size=font_size,
        color=color
    )

def draw_button(canvas, text, x, y, w, h, gradient_colors):
    """
    Draws a more elegant and colorful button on the canvas with a shadow and text.
    Returns the bounds (x, y, w, h) of the button for click detection.
    """
    border_thickness = 2 # Define border thickness

    # Draw the white border first, slightly larger than the button
    # This will be behind the gradient, creating the border effect.
    canvas.create_rectangle(
        x - border_thickness, y - border_thickness,
        x + w + border_thickness, y + h + border_thickness,
        "#FFFFFF", "#FFFFFF" # Fill and outline with white for the border
    )

    # Draw shadow for depth effect, positioned relative to the main button area
    canvas.create_rectangle(x + 3, y + 3, x + w + 3, y + h + 3, "#222", "#222")

    num_steps = len(gradient_colors)
    step_height = h / num_steps
    
    # Draw gradient background by layering thin rectangles, within the main button area
    for i in range(num_steps):
        color = gradient_colors[i]
        canvas.create_rectangle(
            x, y + i * step_height,
            x + w, y + (i + 1) * step_height,
            color, color
        )
    
    # Draw button text, centered within the button
    draw_centered_text(canvas, x + w / 2, y + h / 2, text, 18, "white")

    # Return the bounds directly for click detection.
    return (x, y, w, h)

def is_click_inside(click_coords, bounds):
    """
    Checks if a mouse click occurred within the given rectangular bounds.
    
    Args:
        click_coords: A tuple (x, y) representing the click coordinates.
        bounds: A tuple (bx, by, bw, bh) representing the button's x, y, width, height.
        
    Returns:
        True if the click is inside the bounds, False otherwise.
    """
    x, y = click_coords
    bx, by, bw, bh = bounds
    return bx <= x <= bx + bw and by <= y <= by + bh

def generate_stars_data(canvas_width, canvas_height, num_stars, star_colors):
    """
    Generates data for a specified number of stars with random positions, sizes, and colors.
    """
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, canvas_width)
        y = random.randint(0, canvas_height)
        size = random.randint(1, 3) # Star size between 1 and 3 pixels
        color = random.choice(star_colors)
        stars.append({"x": x, "y": y, "size": size, "color": color})
    return stars

def draw_stars(canvas, stars_data):
    """
    Draws the stars on the canvas based on the provided stars_data.
    """
    for star in stars_data:
        canvas.create_oval(
            star["x"], star["y"],
            star["x"] + star["size"], star["y"] + star["size"],
            star["color"], star["color"]
        )

def draw_and_initialize_planets(canvas, solar_system_data, scale_factor, center_x, center_y):
    """
    Draws the Sun and planets on the canvas and initializes their properties.
    This function is called both at the start and whenever the scale factor changes.
    
    Args:
        canvas: The graphics Canvas object.
        solar_system_data: List of dictionaries containing celestial body data.
        scale_factor: The current scaling factor from AU to pixels.
        center_x: The X-coordinate of the canvas center (Sun's position).
        center_y: The Y-coordinate of the canvas center (Sun's position).
        
    Returns:
        A list of dictionaries, each representing a planet with its current state and object ID.
    """
    planets = []

    # --- Draw the Sun ---
    sun_data = solar_system_data[0] # Get Sun's data from the list
    sun_size = sun_data["size_px"]
    
    # Create the Sun as an oval at the center of the canvas
    sun_obj = canvas.create_oval(
        center_x - sun_size / 2, center_y - sun_size / 2,
        center_x + sun_size / 2, center_y + sun_size / 2,
        sun_data["color"], sun_data["color"] # Fill and outline color are the same
    )
    
    # Add Sun's data to the planets list for consistent iteration, even though it doesn't orbit
    planets.append({
        "name": sun_data["name"],
        "radius_px": 0, # Sun has no orbital radius
        "period_years": 0, # Sun has no orbital period
        "size_px": sun_size,
        "color": sun_data["color"],
        "current_angle": 0, # Initial angle (not used for Sun)
        "object_id": sun_obj,
        "center_x": center_x, # Store its fixed center coordinates
        "center_y": center_y,
        "description": sun_data["description"] # Add description
    })

    # --- Draw the Planets ---
    # Iterate through the SOLAR_SYSTEM_DATA, starting from index 1 to skip the Sun
    for i in range(1, len(solar_system_data)):
        planet_data = solar_system_data[i]
        
        # Calculate the orbital radius in pixels based on AU and the scaling factor
        radius_px = planet_data["radius_au"] * scale_factor
        
        # Set the initial position of the planet. All planets start to the right of the Sun (angle 0).
        initial_x = center_x + radius_px
        initial_y = center_y

        # Create the planet as an oval on the canvas
        planet_size = planet_data["size_px"]
        planet_obj = canvas.create_oval(
            initial_x - planet_size / 2, initial_y - planet_size / 2,
            initial_x + planet_size / 2, initial_y + planet_size / 2,
            planet_data["color"], planet_data["color"] # Fill and outline color are the same
        )

        # Store the planet's dynamic properties in the 'planets' list
        planets.append({
            "name": planet_data["name"],
            "radius_px": radius_px,
            "period_years": planet_data["period_years"],
            "size_px": planet_size,
            "color": planet_data["color"],
            "current_angle": 0, # Each planet starts at 0 radians (right side)
            "object_id": planet_obj,
            "center_x": center_x, # Reference to the Sun's center for orbital calculations
            "center_y": center_y,
            "description": planet_data["description"] # Add description
        })
    return planets

def display_description_page(canvas, planet_info, stars_data):
    """
    Displays a detailed description page for the given planet.
    Waits for a 'Back' button click to return.
    """
    canvas.clear() # Clear the solar system view
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, "#000000", "#000000") # Ensure black background for description
    draw_stars(canvas, stars_data) # Redraw stars on the description page background

    # Draw planet name
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 50, planet_info["name"], 30, planet_info["color"])

    # Draw description with improved text wrapping
    description_text = planet_info["description"]
    max_line_width_px = CANVAS_WIDTH - 40 # 20px padding on each side
    current_y = 100 # Initial Y for the description text
    
    # Split the description by explicit newlines first, then process each segment for word wrapping
    segments = description_text.split('\n')
    
    for segment in segments:
        words = segment.split() # Split by any whitespace within the segment
        current_line_words = []
        for word in words:
            test_line = " ".join(current_line_words + [word])
            # Check if adding the next word exceeds the max line width
            if estimate_text_width(test_line, 14) < max_line_width_px:
                current_line_words.append(word)
            else:
                # Draw the current line and start a new one
                draw_centered_text(canvas, CANVAS_WIDTH / 2, current_y, " ".join(current_line_words), 14, "#FFF") # White text for descriptions
                current_y += 20 # Line height
                current_line_words = [word]
        # Draw any remaining words in the last line of the segment
        if current_line_words:
            draw_centered_text(canvas, CANVAS_WIDTH / 2, current_y, " ".join(current_line_words), 14, "#FFF") # White text for descriptions
            current_y += 20 # Add line height after each segment (even if only one line)

    # Draw the planet/sun peaking from all four corners
    # Size for corner elements (can be adjusted)
    corner_size = planet_info["size_px"] * 2 
    offset = corner_size / 2 # How much of the circle is off-canvas

    # Top-left corner
    canvas.create_oval(
        -offset, -offset,
        corner_size - offset, corner_size - offset,
        planet_info["color"], planet_info["color"]
    )
    # Top-right corner
    canvas.create_oval(
        CANVAS_WIDTH - corner_size + offset, -offset,
        CANVAS_WIDTH + offset, corner_size - offset,
        planet_info["color"], planet_info["color"]
    )
    # Bottom-left corner
    canvas.create_oval(
        -offset, CANVAS_HEIGHT - corner_size + offset,
        corner_size - offset, CANVAS_HEIGHT + offset,
        planet_info["color"], planet_info["color"]
    )
    # Bottom-right corner
    canvas.create_oval(
        CANVAS_WIDTH - corner_size + offset, CANVAS_HEIGHT - corner_size + offset,
        CANVAS_WIDTH + offset, CANVAS_HEIGHT + offset,
        planet_info["color"], planet_info["color"]
    )

    # Define 'Back' button
    back_button_width = 100
    back_button_height = 30
    back_button_x = (CANVAS_WIDTH - back_button_width) / 2
    back_button_y = CANVAS_HEIGHT - back_button_height - 20 # Position above bottom
    
    # Define gradient colors for the "Back" button
    back_button_gradient = ["#4682B4", "#5F9EA0", "#6495ED", "#87CEEB"] # Shades of blue/steel blue
    back_button_bounds = draw_button(canvas, "Back", back_button_x, back_button_y, back_button_width, back_button_height, back_button_gradient)

    # Wait for 'Back' button click
    while True:
        new_clicks = canvas.get_new_mouse_clicks()
        for click in new_clicks:
            if is_click_inside(click, back_button_bounds):
                return # Exit the description page function
        time.sleep(0.01) # Small delay to prevent busy-waiting

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

def draw_start_screen_solar_system(canvas, palette_index):
    """
    Draws the initial start screen for the solar system simulation.
    """
    draw_creative_background(canvas, palette_index) # Use the creative background
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 80, "🌌 Solar System Explorer 🚀", 30, "#2C3E50", font='Chalkboardbold')
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 130, "Click a planet for info", 20, "#34495E")
    draw_centered_text(canvas, CANVAS_WIDTH / 2-15, CANVAS_HEIGHT - 30, "© 2025 Mohamed ayoub Essalami", 12, "black") # Update copyright
    
    # Position the start button in the center
    button_x = (CANVAS_WIDTH - 180) / 2
    button_y = CANVAS_HEIGHT / 2 - 30
    
    start_button_gradient = ["#1E90FF", "#4169E1", "#6495ED", "#87CEEB"] # Shades of blue
    return draw_button(canvas, "✨Start Simulation ", button_x, button_y, 180, 60, start_button_gradient)


def main():
    """
    Main function to set up the canvas, draw the solar system, and run the animation.
    """
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    # --- Start Screen Loop ---
    current_palette_index = 0
    last_background_change = time.time()
    start_button_bounds = (0, 0, 0, 0) # Initialize with dummy values

    while True:
        # Draw the start screen with the current creative background
        draw_start_screen_solar_system(canvas, current_palette_index)
        
        # Capture button bounds after drawing
        button_x = (CANVAS_WIDTH - 180) / 2
        button_y = CANVAS_HEIGHT / 2 - 30
        start_button_bounds = (button_x, button_y, 180, 60)

        click = canvas.get_last_click()
        now = time.time()
        
        # Cycle creative background every 3 seconds on the start screen
        if now - last_background_change > 3:
            current_palette_index = (current_palette_index + 1) % len(elegant_palettes)
            last_background_change = now

        if click and is_click_inside(click, start_button_bounds):
            # Simulate button press effect (optional, as canvas clear will happen immediately)
            # You could add a quick visual change here if desired.
            time.sleep(1) # Brief pause for a "click" feel
            break # Exit start screen loop
        time.sleep(1) # Small delay to prevent busy-waiting on the start screen

    # --- Clear to Start Game ---
    # Clear the dynamic background and prepare for the solar system simulation
    canvas.clear()
    
    # Calculate the center coordinates of the canvas, which will be the Sun's position
    center_x = CANVAS_WIDTH / 2
    center_y = CANVAS_HEIGHT / 2

    # Initial scaling factor
    current_scale_factor = 6
    MIN_SCALE_FACTOR = 1 # Minimum scale factor to prevent objects from becoming too small

    # Generate star data once
    stars_data = generate_stars_data(CANVAS_WIDTH, CANVAS_HEIGHT, NUM_STARS, STAR_COLORS)
    draw_stars(canvas, stars_data) # Draw stars initially (static background for simulation)

    # Draw the solar system for the first time
    planets = draw_and_initialize_planets(canvas, SOLAR_SYSTEM_DATA, current_scale_factor, center_x, center_y)

    # Define button properties
    button_width = 150
    button_height = 40
    padding_between_buttons = 20
    total_buttons_width = (button_width * 2) + padding_between_buttons
    
    # Calculate positions for both buttons to be centered together
    start_x = (CANVAS_WIDTH - total_buttons_width) / 2
    button_y = CANVAS_HEIGHT - button_height - 10 # 10 pixels from bottom

    zoom_out_button_x = start_x
    zoom_in_button_x = start_x + button_width + padding_between_buttons

    # Define distinct gradient colors for each button
    zoom_out_gradient = ["#2E8B57", "#3CB371", "#66CDAA", "#90EE90"] # Shades of green/sea green
    zoom_in_gradient = ["#FF4500", "#FF6347", "#FF7F50", "#FFA07A"] # Shades of orange/red

    # Create the Zoom Out button
    zoom_out_button_bounds = draw_button(canvas, "Zoom Out", zoom_out_button_x, button_y, button_width, button_height, zoom_out_gradient)
    # Create the Zoom In button
    zoom_in_button_bounds = draw_button(canvas, "Zoom In", zoom_in_button_x, button_y, button_width, button_height, zoom_in_gradient)

    # --- Animation Loop ---
    while True:
        # Check for new mouse clicks
        new_clicks = canvas.get_new_mouse_clicks()
        for click in new_clicks: # Iterate through all new clicks
            # If a click occurred on the zoom in button, increase the scale factor
            if is_click_inside(click, zoom_in_button_bounds):
                current_scale_factor += 5
                print(f"Scale factor increased to: {current_scale_factor}")
                
                # Clear the canvas to redraw everything with the new scale
                canvas.clear()
                draw_stars(canvas, stars_data) # Redraw stars after clearing
                
                # Redraw and re-initialize planets with the new scale factor
                planets = draw_and_initialize_planets(canvas, SOLAR_SYSTEM_DATA, current_scale_factor, center_x, center_y)
                
                # Re-draw the zoom buttons after clearing and redrawing planets
                zoom_out_button_bounds = draw_button(canvas, "Zoom Out", zoom_out_button_x, button_y, button_width, button_height, zoom_out_gradient)
                zoom_in_button_bounds = draw_button(canvas, "Zoom In", zoom_in_button_x, button_y, button_width, button_height, zoom_in_gradient)
            
            # If a click occurred on the zoom out button, decrease the scale factor
            elif is_click_inside(click, zoom_out_button_bounds):
                if current_scale_factor > MIN_SCALE_FACTOR: # Ensure scale doesn't go below minimum
                    current_scale_factor -= 5
                    if current_scale_factor < MIN_SCALE_FACTOR: # Cap at minimum
                        current_scale_factor = MIN_SCALE_FACTOR
                    print(f"Scale factor decreased to: {current_scale_factor}")

                    # Clear the canvas to redraw everything with the new scale
                    canvas.clear()
                    draw_stars(canvas, stars_data) # Redraw stars after clearing
                    
                    # Redraw and re-initialize planets with the new scale factor
                    planets = draw_and_initialize_planets(canvas, SOLAR_SYSTEM_DATA, current_scale_factor, center_x, center_y)
                    
                    # Re-draw the zoom buttons after clearing and redrawing planets
                    zoom_out_button_bounds = draw_button(canvas, "Zoom Out", zoom_out_button_x, button_y, button_width, button_height, zoom_out_gradient)
                    zoom_in_button_bounds = draw_button(canvas, "Zoom In", zoom_in_button_x, button_y, button_width, button_height, zoom_in_gradient)

            else:
                # Check if a planet or the Sun was clicked
                clicked_planet_info = None
                # Iterate through planets to see if click overlaps with any
                for planet in planets:
                    # Get the current coordinates and size of the planet object
                    obj_coords = canvas.coords(planet["object_id"])
                    if not obj_coords: # Skip if object doesn't have coordinates (e.g., deleted)
                        continue
                    obj_left_x = obj_coords[0]
                    obj_top_y = obj_coords[1]
                    obj_width = canvas.get_object_width(planet["object_id"])
                    obj_height = canvas.get_object_height(planet["object_id"])
                    
                    # Calculate the center of the planet for click detection
                    planet_center_x = obj_left_x + obj_width / 2
                    planet_center_y = obj_top_y + obj_height / 2
                    
                    # Use distance from center for circular click detection
                    distance = math.sqrt((click[0] - planet_center_x)**2 + (click[1] - planet_center_y)**2)
                    
                    # If click is within the planet's visual radius
                    if distance <= planet["size_px"] / 2:
                        clicked_planet_info = planet
                        break # Found the clicked planet, exit inner loop

                if clicked_planet_info:
                    display_description_page(canvas, clicked_planet_info, stars_data) # Pass stars_data to description page
                    # After returning from description page, redraw the solar system and button
                    canvas.clear()
                    draw_stars(canvas, stars_data) # Redraw stars after returning from description
                    planets = draw_and_initialize_planets(canvas, SOLAR_SYSTEM_DATA, current_scale_factor, center_x, center_y)
                    zoom_out_button_bounds = draw_button(canvas, "Zoom Out", zoom_out_button_x, button_y, button_width, button_height, zoom_out_gradient)
                    zoom_in_button_bounds = draw_button(canvas, "Zoom In", zoom_in_button_x, button_y, button_width, button_height, zoom_in_gradient)


        for planet in planets:
            # Skip the Sun as it does not orbit
            if planet["name"] == "Sun":
                continue

            # Calculate the angular increment for the current frame.
            if planet["period_years"] > 0: # Avoid division by zero for planets
                angle_increment = (2 * math.pi * TIME_STEP) / planet["period_years"]
                planet["current_angle"] += angle_increment
                
                # Normalize the angle to keep it within 0 to 2*pi (a full circle)
                if planet["current_angle"] >= 2 * math.pi:
                    planet["current_angle"] -= 2 * math.pi

            # Calculate the new x and y coordinates for the planet's center.
            new_x_center = planet["center_x"] + planet["radius_px"] * math.cos(planet["current_angle"])
            new_y_center = planet["center_y"] + planet["radius_px"] * math.sin(planet["current_angle"])

            # Move the planet object on the canvas to its new calculated position.
            canvas.moveto(
                planet["object_id"],
                new_x_center - planet["size_px"] / 2,
                new_y_center - planet["size_px"] / 2
            )
        
        # Pause execution for a short duration to control the animation frame rate.
        time.sleep(0.02)

if __name__ == "__main__":
    main()