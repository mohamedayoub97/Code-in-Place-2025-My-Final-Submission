from graphics import Canvas
import time
import math
import random

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

# Define color themes
DARK_THEME_COLORS = {
    "canvas_bg": "#1a1a2e",
    "text_primary": "#FFFFFF",
    "text_secondary": "#E0E0E0",
    "text_highlight": "#FFD700",
    "button_shadow": "#333333",
    "button_border": "#2C5282",
    "start_button": "#38A169",
    "restart_button": "#805AD5",
    "option_colors": ["#3182CE", "#38A169", "#D69E2E", "#E53E3E"],
    "feedback_correct": "#38A169",
    "feedback_incorrect": "#E53E3E",
    "info_text": "#87CEEB",
    "star_color": "#FFD700",
    "toggle_button_bg": "#4A5568",
    "toggle_button_text": "#FFFFFF",
}

LIGHT_THEME_COLORS = {
    "canvas_bg": "#F7FAFC",
    "text_primary": "#2D3748",
    "text_secondary": "#4A5568",
    "text_highlight": "#D97706",
    "button_shadow": "#A0AEC0",
    "button_border": "#63B3ED",
    "start_button": "#48BB78",
    "restart_button": "#9F7AEA",
    "option_colors": ["#4299E1", "#48BB78", "#ED8936", "#F56565"],
    "feedback_correct": "#48BB78",
    "feedback_incorrect": "#F56565",
    "info_text": "#3182CE",
    "star_color": "#ECC94B",
    "toggle_button_bg": "#CBD5E0",
    "toggle_button_text": "#2D3748",
}

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

def draw_button(canvas, x, y, width, height, text, color, text_color, shadow_color, border_color):
    # Shadow
    shadow_offset = 2
    shadow = canvas.create_rectangle(
        x + shadow_offset, y + shadow_offset,
        x + width + shadow_offset, y + height + shadow_offset,
        shadow_color, shadow_color
    )
    
    # Button body
    button_rect = canvas.create_rectangle(
        x, y, x + width, y + height,
        color, border_color
    )
    
    # Button text
    text_y = y + height / 2 - 8
    button_label = draw_centered_text(canvas, x + width / 2, text_y, text, 14, text_color)
    
    return button_rect, button_label, shadow

def is_point_in_button(x, y, btn_x, btn_y, btn_width, btn_height):
    return btn_x <= x <= btn_x + btn_width and btn_y <= y <= btn_y + btn_height

class TunisiaRiddleGame:
    def __init__(self):
        self.canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.current_question = 0
        self.score = 0
        self.game_state = "start"  # start, playing, result
        self.is_dark_mode = True  # Initial mode
        self.current_theme = DARK_THEME_COLORS
        self.stars = []
        
        # Riddles about Tunisia
        self.riddles = [
            {
                "question": "🏛️ I am the ancient city where Carthage\nonce stood. What am I?",
                "options": ["A) Sfax", "B) Tunis", "C) Sousse", "D) Kairouan"],
                "correct": 1,
                "explanation": "Tunis is the capital built near ancient Carthage!"
            },
            {
                "question": "🌊 I am a blue and white town on a cliff.\nArtists love my beauty. What am I?",
                "options": ["A) Hammamet", "B) Mahdia", "C) Sidi Bou Said", "D) Bizerte"],
                "correct": 2,
                "explanation": "Sidi Bou Said is famous for its blue and white architecture!"
            },
            {
                "question": "🏜️ What desert covers 40% of Tunisia's\nterritory?",
                "options": ["A) Kalahari", "B) Sahara", "C) Gobi", "D) Mojave"],
                "correct": 1,
                "explanation": "The Sahara Desert covers about 40% of Tunisia!"
            },
            {
                "question": "🕌 I am the first mosque built in Africa.\nIn Kairouan, I stand proudly. What am I?",
                "options": ["A) Al-Zaytuna", "B) Great Mosque", "C) Sidi Mahrez", "D) Hammouda Pasha"],
                "correct": 1,
                "explanation": "Great Mosque of Kairouan was the first mosque in Africa!"
            },
            {
                "question": "🫒 Tunisia is the world's second largest\nproducer of what?",
                "options": ["A) Dates", "B) Olive Oil", "C) Oranges", "D) Wheat"],
                "correct": 1,
                "explanation": "Tunisia produces excellent olive oil, ranking globally!"
            },
            {
                "question": "🏺 What ancient queen founded Carthage\naccording to legend?",
                "options": ["A) Cleopatra", "B) Dido", "C) Zenobia", "D) Nefertiti"],
                "correct": 1,
                "explanation": "Queen Dido (Elissa) founded Carthage in 814 BC!"
            },
            {
                "question": "🎬 Which famous movie series was filmed\nin Tunisia's desert?",
                "options": ["A) Indiana Jones", "B) Star Wars", "C) Mad Max", "D) Dune"],
                "correct": 1,
                "explanation": "Star Wars Tatooine scenes were filmed in Tunisia!"
            },
            {
                "question": "🏖️ What is Tunisia's most popular\nbeach resort town?",
                "options": ["A) Sousse", "B) Monastir", "C) Hammamet", "D) Mahdia"],
                "correct": 2,
                "explanation": "Hammamet is Tunisia's premier beach destination!"
            },
            {
                "question": "🌹 What is the national flower of Tunisia?",
                "options": ["A) Rose", "B) Jasmine", "C) Lily", "D) Sunflower"],
                "correct": 1,
                "explanation": "Jasmine is Tunisia's national flower and symbol!"
            },
            {
                "question": "🏛️ How many UNESCO World Heritage Sites\ndoes Tunisia have?",
                "options": ["A) 6", "B) 8", "C) 10", "D) 12"],
                "correct": 1,
                "explanation": "Tunisia has 8 UNESCO World Heritage Sites!"
            },
            {
                "question": "🐪 What is the name of Tunisia's largest\nsalt lake?",
                "options": ["A) Chott el Djerid", "B) Lake Bizerte", "C) Sebkhet Kelbia", "D) Lac de Tunis"],
                "correct": 0,
                "explanation": "Chott el Djerid is Tunisia's largest salt lake!"
            },
            {
                "question": "🎭 In which city is the famous Carthage\nFilm Festival held?",
                "options": ["A) Sfax", "B) Tunis", "C) Sousse", "D) Bizerte"],
                "correct": 1,
                "explanation": "Carthage Film Festival is held in Tunis!"
            },
            {
                "question": "🏺 What ancient Carthaginian general\ncrossed the Alps with elephants?",
                "options": ["A) Scipio", "B) Hannibal", "C) Hamilcar", "D) Hasdrubal"],
                "correct": 1,
                "explanation": "Hannibal famously crossed the Alps with elephants!"
            },
            {
                "question": "🌊 Tunisia is bordered by which two\ncountries?",
                "options": ["A) Libya & Egypt", "B) Algeria & Libya", "C) Morocco & Algeria", "D) Egypt & Sudan"],
                "correct": 1,
                "explanation": "Tunisia borders Algeria to the west and Libya to the east!"
            },
            {
                "question": "🕌 What is the holiest city in Tunisia\nfor Muslims?",
                "options": ["A) Tunis", "B) Kairouan", "C) Sfax", "D) Monastir"],
                "correct": 1,
                "explanation": "Kairouan is considered the fourth holiest city in Islam!"
            },
            {
                "question": "🏺 What ancient Roman city ruins can\nbe found in Tunisia?",
                "options": ["A) Pompeii", "B) Dougga", "C) Leptis Magna", "D) Timgad"],
                "correct": 1,
                "explanation": "Dougga is a UNESCO site with amazing Roman ruins!"
            },
            {
                "question": "🌍 What revolution started in Tunisia\nin 2010?",
                "options": ["A) Jasmine Revolution", "B) Rose Revolution", "C) Cedar Revolution", "D) Orange Revolution"],
                "correct": 0,
                "explanation": "The Jasmine Revolution began the Arab Spring!"
            },
            {
                "question": "🏖️ What sea borders Tunisia's\nnorthern coast?",
                "options": ["A) Red Sea", "B) Mediterranean", "C) Atlantic Ocean", "D) Black Sea"],
                "correct": 1,
                "explanation": "Tunisia's coast is on the Mediterranean Sea!"
            },
            {
                "question": "🎨 What craft is Nabeul famous for?",
                "options": ["A) Carpets", "B) Pottery", "C) Jewelry", "D) Leather"],
                "correct": 1,
                "explanation": "Nabeul is renowned for its beautiful pottery!"
            },
            {
                "question": "🐟 What traditional Tunisian dish is made\nwith couscous and fish?",
                "options": ["A) Brik", "B) Lablabi", "C) Couscous au Poisson", "D) Mechouia"],
                "correct": 2,
                "explanation": "Couscous au Poisson is a beloved Tunisian dish!"
            }
        ]
        
        self.ui_elements = {}
        self.game_elements = {}
        self.toggle_button_coords = (CANVAS_WIDTH - 40, 10, 30, 20) # (x, y, width, height)

    def clear_all_elements(self):
        """Clears all elements from the canvas."""
        self.canvas.clear()
        self.ui_elements = {}
        self.game_elements = {}
        self.stars = [] # Clear star list too

    def create_stars(self):
        """Create decorative stars for the background with random positions and sizes."""
        num_stars = 25 # More stars for better effect
        for _ in range(num_stars):
            x = random.randint(0, CANVAS_WIDTH)
            y = random.randint(0, CANVAS_HEIGHT)
            size = random.randint(1, 3) # Smaller random sizes
            star_color = self.current_theme["star_color"]
            star = self.canvas.create_oval(x-size, y-size, x+size, y+size, star_color, star_color)
            self.stars.append(star)

    def draw_background(self):
        """Draws the background rectangle and stars, clearing previous ones."""
        self.canvas.clear() # Clear everything before redrawing
        
        bg_color = self.current_theme["canvas_bg"]
        self.canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, color=bg_color)
        self.create_stars() # Redraw stars each time

    def draw_toggle_button(self):
        btn_x, btn_y, btn_width, btn_height = self.toggle_button_coords
        
        # Use the requested emojis based on the current mode
        if self.is_dark_mode:
            text = "🌑 " # Dark mode emoji
        else:
            text = "☀️" # Light mode emoji
        
        btn_elements = draw_button(
            self.canvas, btn_x, btn_y, btn_width, btn_height,
            text, self.current_theme["toggle_button_bg"], self.current_theme["toggle_button_text"],
            self.current_theme["button_shadow"], self.current_theme["toggle_button_bg"]
        )
        self.ui_elements['toggle_button'] = btn_elements
        self.ui_elements['toggle_button_coords'] = self.toggle_button_coords

    def draw_start_screen(self):
        self.draw_background()
        self.draw_toggle_button()
        
        # Title
        draw_centered_text(self.canvas, CANVAS_WIDTH/2, 100, "🇹🇳 TUNISIA RIDDLE GAME 🇹🇳", 24, self.current_theme["text_highlight"])
        draw_centered_text(self.canvas, CANVAS_WIDTH/2, 140, "Test your knowledge about beautiful Tunisia!", 16, self.current_theme["text_primary"])
        
        # Instructions
        instructions = [
            "🎯 Answer riddles about Tunisia",
            "🧠 Learn culture, history & geography",  
            "🏆 Get your final score",
            "🌟 Ready to explore Tunisia?"
        ]
        
        for i, instruction in enumerate(instructions):
            draw_centered_text(self.canvas, CANVAS_WIDTH/2, 180 + i*25, instruction, 12, self.current_theme["text_secondary"])
        
        # Start button
        btn_width, btn_height = 160, 40
        btn_x = CANVAS_WIDTH/2 - btn_width/2
        btn_y = 300
        
        self.ui_elements['start_btn'] = draw_button(
            self.canvas, btn_x, btn_y, btn_width, btn_height,
            "🚀 START GAME", self.current_theme["start_button"], self.current_theme["text_primary"],
            self.current_theme["button_shadow"], self.current_theme["button_border"]
        )
        self.ui_elements['start_coords'] = (btn_x, btn_y, btn_width, btn_height)
        
        # Fun facts
        draw_centered_text(self.canvas, CANVAS_WIDTH/2, 380, "Tunisia is home to ancient Carthage!", 10, self.current_theme["info_text"])
        draw_centered_text(self.canvas, CANVAS_WIDTH/2, 395, "Star Wars Tatooine scenes were filmed here! 🎬", 10, self.current_theme["info_text"])
    
    def draw_question_screen(self):
        self.draw_background()
        self.draw_toggle_button()
        
        riddle = self.riddles[self.current_question]
        
        # Header
        draw_centered_text(self.canvas, CANVAS_WIDTH/2, 50, f"Question {self.current_question + 1} of {len(self.riddles)}", 18, self.current_theme["text_highlight"])
        draw_centered_text(self.canvas, CANVAS_WIDTH/2, 80, f"Score: {self.score}/{self.current_question}", 14, self.current_theme["text_secondary"])
        
        # Question text (multi-line)
        question_lines = riddle["question"].split('\n')
        for i, line in enumerate(question_lines):
            draw_centered_text(self.canvas, CANVAS_WIDTH/2, 130 + i*25, line, 16, self.current_theme["text_primary"])
        
        # Answer buttons
        btn_width, btn_height = 200, 30
        btn_x = CANVAS_WIDTH/2 - btn_width/2
        start_y = 220
        
        for i, option in enumerate(riddle["options"]):
            btn_y = start_y + i * 45
            btn_elements = draw_button(
                self.canvas, btn_x, btn_y, btn_width, btn_height,
                option, self.current_theme["option_colors"][i], self.current_theme["text_primary"],
                self.current_theme["button_shadow"], self.current_theme["button_border"]
            )
            self.ui_elements[f'option_{i}'] = btn_elements
            self.ui_elements[f'option_{i}_coords'] = (btn_x, btn_y, btn_width, btn_height)
    
    def draw_result_screen(self):
        self.draw_background()
        self.draw_toggle_button()
        
        # Results
        percentage = (self.score / len(self.riddles)) * 100
        
        if percentage >= 80:
            title = "🏆 EXCELLENT! 🏆"
            subtitle = "You're a Tunisia expert!"
            color = self.current_theme["feedback_correct"]
        elif percentage >= 60:
            title = "👏 GOOD JOB! 👏"
            subtitle = "You know Tunisia well!"
            color = self.current_theme["option_colors"][0] # Blue
        else:
            title = "📚 KEEP LEARNING! 📚"
            subtitle = "Tunisia has so much to discover!"
            color = self.current_theme["option_colors"][2] # Yellow
        
        draw_centered_text(self.canvas, CANVAS_WIDTH/2, 150, title, 24, color)
        draw_centered_text(self.canvas, CANVAS_WIDTH/2, 190, subtitle, 16, self.current_theme["text_primary"])
        draw_centered_text(self.canvas, CANVAS_WIDTH/2, 230, f"Final Score: {self.score}/{len(self.riddles)} ({percentage:.0f}%)", 18, self.current_theme["text_secondary"])
        
        # Tunisia facts
        facts = [
            "🌟 Birthplace of the Arab Spring in 2010",
            "🏺 Has 8 UNESCO World Heritage Sites",  
            "🫒 Major producer of olive oil",
            "🎭 Hosts the Carthage Film Festival"
        ]
        
        draw_centered_text(self.canvas, CANVAS_WIDTH/2, 280, "Learn more about Tunisia:", 14, self.current_theme["text_highlight"])
        for i, fact in enumerate(facts):
            draw_centered_text(self.canvas, CANVAS_WIDTH/2, 305 + i*20, fact, 10, self.current_theme["text_secondary"])
        
        # Play again button
        btn_width, btn_height = 160, 40
        btn_x = CANVAS_WIDTH/2 - btn_width/2
        btn_y = 410
        
        self.ui_elements['restart_btn'] = draw_button(
            self.canvas, btn_x, btn_y, btn_width, btn_height,
            "🔄 PLAY AGAIN", self.current_theme["restart_button"], self.current_theme["text_primary"],
            self.current_theme["button_shadow"], self.current_theme["button_border"]
        )
        self.ui_elements['restart_coords'] = (btn_x, btn_y, btn_width, btn_height)
    
    def show_answer_feedback(self, selected_option):
        riddle = self.riddles[self.current_question]
        is_correct = selected_option == riddle["correct"]
        
        if is_correct:
            self.score += 1
            feedback_text = "✅ CORRECT!"
            feedback_color = self.current_theme["feedback_correct"]
        else:
            feedback_text = "❌ INCORRECT!"
            feedback_color = self.current_theme["feedback_incorrect"]
            
        # Show feedback
        feedback_obj = draw_centered_text(self.canvas, CANVAS_WIDTH/2, 420, feedback_text, 16, feedback_color)
        explanation_obj = draw_centered_text(self.canvas, CANVAS_WIDTH/2, 445, riddle["explanation"], 12, self.current_theme["text_secondary"])
        
        # Wait before continuing
        time.sleep(2.5)
        
        # Clean up feedback
        self.canvas.delete(feedback_obj)
        self.canvas.delete(explanation_obj)
        
        self.current_question += 1
        if self.current_question >= len(self.riddles):
            self.game_state = "result"
            
    def handle_click(self, x, y):
        # Handle toggle button click first
        toggle_coords = self.ui_elements.get('toggle_button_coords')
        if toggle_coords and is_point_in_button(x, y, *toggle_coords):
            self.is_dark_mode = not self.is_dark_mode
            self.current_theme = DARK_THEME_COLORS if self.is_dark_mode else LIGHT_THEME_COLORS
            # Redraw the current screen to apply theme change
            if self.game_state == "start":
                self.draw_start_screen()
            elif self.game_state == "playing":
                self.draw_question_screen()
            elif self.game_state == "result":
                self.draw_result_screen()
            return # Don't process other clicks if toggle button was pressed

        if self.game_state == "start":
            coords = self.ui_elements.get('start_coords')
            if coords and is_point_in_button(x, y, *coords):
                self.game_state = "playing"
                self.current_question = 0
                self.score = 0
                
        elif self.game_state == "playing":
            for i in range(4):
                coords = self.ui_elements.get(f'option_{i}_coords')
                if coords and is_point_in_button(x, y, *coords):
                    self.show_answer_feedback(i)
                    break
                    
        elif self.game_state == "result":
            coords = self.ui_elements.get('restart_coords')
            if coords and is_point_in_button(x, y, *coords):
                self.game_state = "start"
                self.current_question = 0
                self.score = 0
    
    def run(self):
        while True:
            # Clear all elements from the canvas at the beginning of each frame
            # This is important for redrawing backgrounds and stars every time
            self.clear_all_elements()

            if self.game_state == "start":
                self.draw_start_screen()
            elif self.game_state == "playing":
                self.draw_question_screen()
            elif self.game_state == "result":
                self.draw_result_screen()
            
            # Handle input
            click = self.canvas.get_last_click()
            if click is not None:
                self.handle_click(click[0], click[1])
                
            time.sleep(0.5)

def main():
    game = TunisiaRiddleGame()
    game.run()

if __name__ == '__main__':
    main()