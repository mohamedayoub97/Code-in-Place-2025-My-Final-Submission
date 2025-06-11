from graphics import Canvas
import random
import time

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

# Background themes for different topics
BACKGROUND_THEMES = {
    0: {"primary": "#E8F5E8", "secondary": "#C8E6C9", "accent": "#A5D6A7", "name": "Nature Green"},
    1: {"primary": "#E3F2FD", "secondary": "#BBDEFB", "accent": "#90CAF9", "name": "Ocean Blue"},
    2: {"primary": "#FFEBEE", "secondary": "#FFCDD2", "accent": "#EF9A9A", "name": "Warm Red"},
    3: {"primary": "#FFFDE7", "secondary": "#FFF9C4", "accent": "#FFF176", "name": "Sunny Yellow"},
    4: {"primary": "#F3E5F5", "secondary": "#E1BEE7", "accent": "#CE93D8", "name": "Royal Purple"},
}

# Comprehensive Python quiz questions
QUIZ_QUESTIONS = [
    # Variables and Basic Data Types (6 questions)
    {
        "question": "What is the correct way to create a variable in Python?",
        "options": ["int x = 5", "x = 5", "var x = 5", "x := 5"],
        "correct": 1,
        "topic": "Variables",
        "difficulty": "Easy"
    },
    {
        "question": "Which of these is NOT a valid Python data type?",
        "options": ["int", "float", "char", "str"],
        "correct": 2,
        "topic": "Data Types",
        "difficulty": "Easy"
    },
    {
        "question": "What does type(42.0) return?",
        "options": ["<class 'int'>", "<class 'float'>", "<class 'number'>", "42.0"],
        "correct": 1,
        "topic": "Data Types",
        "difficulty": "Medium"
    },
    {
        "question": "Which operator checks if two values are identical objects?",
        "options": ["==", "!=", "is", "==="],
        "correct": 2,
        "topic": "Operators",
        "difficulty": "Medium"
    },
    {
        "question": "What is the result of 10 // 3 in Python?",
        "options": ["3.33", "3", "4", "3.0"],
        "correct": 1,
        "topic": "Operators",
        "difficulty": "Easy"
    },
    {
        "question": "How do you create a multi-line string in Python?",
        "options": ['Using "', "Using '", 'Using """', "Using \\n"],
        "correct": 2,
        "topic": "Strings",
        "difficulty": "Medium"
    },
    
    # Data Structures (8 questions)
    {
        "question": "Which method adds an element to the end of a list?",
        "options": ["add()", "append()", "insert()", "push()"],
        "correct": 1,
        "topic": "Lists",
        "difficulty": "Easy"
    },
    {
        "question": "What is the output of [1, 2, 3][1:3]?",
        "options": ["[1, 2]", "[2, 3]", "[1, 2, 3]", "[2]"],
        "correct": 1,
        "topic": "Lists",
        "difficulty": "Medium"
    },
    {
        "question": "Which data structure is ordered and unchangeable?",
        "options": ["List", "Dictionary", "Tuple", "Set"],
        "correct": 2,
        "topic": "Tuples",
        "difficulty": "Easy"
    },
    {
        "question": "How do you create an empty dictionary?",
        "options": ["dict()", "{}", "Both A and B", "[]"],
        "correct": 2,
        "topic": "Dictionaries",
        "difficulty": "Easy"
    },
    {
        "question": "What method returns all keys from a dictionary?",
        "options": ["values()", "keys()", "items()", "get()"],
        "correct": 1,
        "topic": "Dictionaries",
        "difficulty": "Easy"
    },
    {
        "question": "Which operation removes duplicates from a list?",
        "options": ["list(dict.fromkeys(lst))", "set(lst)", "Both A and B", "unique(lst)"],
        "correct": 2,
        "topic": "Sets",
        "difficulty": "Medium"
    },
    {
        "question": "What is the result of len('Hello World')?",
        "options": ["10", "11", "12", "Error"],
        "correct": 1,
        "topic": "Strings",
        "difficulty": "Easy"
    },
    {
        "question": "Which method splits a string into a list?",
        "options": ["divide()", "split()", "separate()", "break()"],
        "correct": 1,
        "topic": "Strings",
        "difficulty": "Easy"
    },
    
    # Control Flow (6 questions)
    {
        "question": "Which keyword is used to exit a loop prematurely?",
        "options": ["exit", "break", "stop", "end"],
        "correct": 1,
        "topic": "Loops",
        "difficulty": "Easy"
    },
    {
        "question": "What does 'continue' do in a loop?",
        "options": ["Exits the loop", "Skips current iteration", "Restarts the loop", "Pauses the loop"],
        "correct": 1,
        "topic": "Loops",
        "difficulty": "Medium"
    },
    {
        "question": "Which loop runs at least once?",
        "options": ["for loop", "while loop", "Neither", "Both can"],
        "correct": 2,
        "topic": "Loops",
        "difficulty": "Medium"
    },
    {
        "question": "What is the syntax for an if-else statement?",
        "options": ["if condition: else:", "if (condition) else", "if condition then else", "if condition: ... else:"],
        "correct": 3,
        "topic": "Conditionals",
        "difficulty": "Easy"
    },
    {
        "question": "Which function creates a sequence of numbers?",
        "options": ["sequence()", "range()", "numbers()", "seq()"],
        "correct": 1,
        "topic": "Loops",
        "difficulty": "Easy"
    },
    {
        "question": "What does 'elif' stand for?",
        "options": ["else if", "elif", "electric if", "element if"],
        "correct": 0,
        "topic": "Conditionals",
        "difficulty": "Easy"
    },
    
    # Functions (6 questions)
    {
        "question": "How do you define a function in Python?",
        "options": ["function myFunc():", "def myFunc():", "func myFunc():", "define myFunc():"],
        "correct": 1,
        "topic": "Functions",
        "difficulty": "Easy"
    },
    {
        "question": "What keyword returns a value from a function?",
        "options": ["return", "yield", "give", "send"],
        "correct": 0,
        "topic": "Functions",
        "difficulty": "Easy"
    },
    {
        "question": "What are *args in function parameters?",
        "options": ["Required arguments", "Variable arguments", "Keyword arguments", "Default arguments"],
        "correct": 1,
        "topic": "Functions",
        "difficulty": "Medium"
    },
    {
        "question": "What are **kwargs in function parameters?",
        "options": ["Variable arguments", "Keyword arguments", "Required arguments", "Optional arguments"],
        "correct": 1,
        "topic": "Functions",
        "difficulty": "Medium"
    },
    {
        "question": "What is a lambda function?",
        "options": ["A named function", "An anonymous function", "A class method", "A built-in function"],
        "correct": 1,
        "topic": "Functions",
        "difficulty": "Medium"
    },
    {
        "question": "What is the scope of variables inside a function?",
        "options": ["Global", "Local", "Both", "Neither"],
        "correct": 1,
        "topic": "Functions",
        "difficulty": "Medium"
    },
    
    # Object-Oriented Programming (4 questions)
    {
        "question": "How do you create a class in Python?",
        "options": ["class MyClass:", "Class MyClass:", "new class MyClass:", "create MyClass:"],
        "correct": 0,
        "topic": "Classes",
        "difficulty": "Easy"
    },
    {
        "question": "What is __init__ method used for?",
        "options": ["Destroying objects", "Initializing objects", "Copying objects", "Comparing objects"],
        "correct": 1,
        "topic": "Classes",
        "difficulty": "Medium"
    },
    {
        "question": "What is inheritance in OOP?",
        "options": ["Creating objects", "Class extending another class", "Method overloading", "Variable hiding"],
        "correct": 1,
        "topic": "Inheritance",
        "difficulty": "Medium"
    },
    {
        "question": "What does 'self' refer to in a class method?",
        "options": ["The class", "The instance", "The method", "The module"],
        "correct": 1,
        "topic": "Classes",
        "difficulty": "Medium"
    },
    
    # Error Handling and Advanced Topics (5 questions)
    {
        "question": "Which block handles exceptions in Python?",
        "options": ["catch", "except", "handle", "error"],
        "correct": 1,
        "topic": "Exceptions",
        "difficulty": "Easy"
    },
    {
        "question": "What is a list comprehension?",
        "options": ["A type of list", "A concise way to create lists", "A list method", "A list property"],
        "correct": 1,
        "topic": "Advanced",
        "difficulty": "Medium"
    },
    {
        "question": "Which module is used for regular expressions?",
        "options": ["regex", "re", "regexp", "pattern"],
        "correct": 1,
        "topic": "Modules",
        "difficulty": "Medium"
    },
    {
        "question": "What does 'import sys' do?",
        "options": ["Imports system module", "Creates a system", "Starts system", "Stops system"],
        "correct": 0,
        "topic": "Modules",
        "difficulty": "Easy"
    },
    {
        "question": "What is PEP 8?",
        "options": ["Python version", "Style guide", "Error type", "Module name"],
        "correct": 1,
        "topic": "Best Practices",
        "difficulty": "Medium"
    }
]

def draw_background(canvas, theme_index):
    """Draw stable geometric background with shapes"""
    canvas.clear()
    theme = BACKGROUND_THEMES[theme_index]
    
    # Base background
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, theme["primary"], theme["primary"])
    
    # Decorative geometric shapes
    # Top decorative section
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, 120, theme["secondary"], theme["secondary"])
    
    # Diagonal accent stripes
    for i in range(0, CANVAS_WIDTH + 100, 100):
        canvas.create_rectangle(i, 0, i + 50, 120, theme["accent"], theme["accent"])
    
    # Side panels
    canvas.create_rectangle(0, 120, 80, CANVAS_HEIGHT, theme["secondary"], theme["accent"])
    canvas.create_rectangle(CANVAS_WIDTH - 80, 120, CANVAS_WIDTH, CANVAS_HEIGHT, theme["secondary"], theme["accent"])
    
    # Decorative circles in corners
    canvas.create_oval(20, 140, 60, 180, theme["accent"], theme["primary"])
    canvas.create_oval(CANVAS_WIDTH - 60, 140, CANVAS_WIDTH - 20, 180, theme["accent"], theme["primary"])
    
    # Bottom decorative section
    canvas.create_rectangle(0, CANVAS_HEIGHT - 60, CANVAS_WIDTH, CANVAS_HEIGHT, theme["secondary"], theme["secondary"])
    
    # Decorative lines
    for i in range(100, CANVAS_WIDTH - 100, 150):
        canvas.create_line(i, CANVAS_HEIGHT - 40, i + 80, CANVAS_HEIGHT - 40, theme["accent"])
        canvas.create_line(i + 40, CANVAS_HEIGHT - 20, i + 40, CANVAS_HEIGHT - 60, theme["accent"])

def estimate_text_width(text, font_size):
    """Estimate text width for centering"""
    return font_size * 0.6 * len(text)

def draw_centered_text(canvas, center_x, center_y, text, font_size, color, font='Arial'):
    """Draw text centered at given coordinates"""
    text_width = estimate_text_width(text, font_size)
    return canvas.create_text(center_x - text_width / 2, center_y, text, 
                             font=font, font_size=font_size, color=color)

def draw_button(canvas, text, x, y, w=200, h=50, color="#4CAF50", text_color="white"):
    """Draw a styled button with shadow"""
    # Shadow
    canvas.create_rectangle(x + 3, y + 3, x + w + 3, y + h + 3, "#00000030", "#00000030")
    # Main button
    rect = canvas.create_rectangle(x, y, x + w, y + h, color, color)
    # Highlight
    canvas.create_rectangle(x + 2, y + 2, x + w - 2, y + 12, "#FFFFFF40", "#FFFFFF40")
    # Text
    draw_centered_text(canvas, x + w / 2, y + h / 2, text, 16, text_color, 'Arial')
    return rect, (x, y, w, h)

def is_click_inside(click, bounds):
    """Check if click is inside button bounds"""
    if not click:
        return False
    x, y = click
    bx, by, bw, bh = bounds
    return bx <= x <= bx + bw and by <= y <= by + bh

def draw_start_screen(canvas, theme_index):
    """Draw the main menu screen"""
    draw_background(canvas, theme_index)
    theme = BACKGROUND_THEMES[theme_index]
    
    # Title with background
    canvas.create_rectangle(100, 130, CANVAS_WIDTH - 100, 180, "#FFFFFF90", theme["accent"])
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 155, "🐍 PYTHON KNOWLEDGE QUIZ 🐍", 32, "#2C3E50", 'Arial')
    
    # Subtitle
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 200, "Test Your Python Skills", 18, "#34495E")
    
    # Info box with decorative border
    canvas.create_rectangle(150, 240, CANVAS_WIDTH - 150, 380, "#FFFFFF95", theme["accent"])
    canvas.create_rectangle(155, 245, CANVAS_WIDTH - 155, 375, theme["primary"], theme["secondary"])
    
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 265, "📋 QUIZ DETAILS", 18, "#2C3E50")
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 295, "• 35 Questions covering all Python topics", 14, "#34495E")
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 315, "• Variables, Data Structures, Control Flow", 14, "#34495E")
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 335, "• Functions, OOP, and Advanced Concepts", 14, "#34495E")
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 355, "• Get your score and detailed feedback", 14, "#34495E")
    
    # Decorative elements
    canvas.create_oval(120, 250, 140, 270, theme["accent"], theme["secondary"])
    canvas.create_oval(CANVAS_WIDTH - 140, 250, CANVAS_WIDTH - 120, 270, theme["accent"], theme["secondary"])
    
    # Start button
    start_btn = draw_button(canvas, "🚀 START QUIZ", CANVAS_WIDTH // 2 - 100, 400, 200, 60, "#27AE60")
    
    # Footer
    draw_centered_text(canvas, CANVAS_WIDTH / 2, CANVAS_HEIGHT - 20, 
                             f"Current Theme: {theme['name']} | Click to begin", 12, "#7F8C8D")
    
    return start_btn

def wrap_text(text, max_width, font_size):
    """Wrap text to fit within max_width"""
    words = text.split()
    lines = []
    current_line = []
    current_width = 0
    
    for word in words:
        word_width = estimate_text_width(word + " ", font_size)
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_width = word_width
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return lines

def draw_question_screen(canvas, question_data, question_num, total_questions, theme_index):
    """Draw the question screen with options"""
    draw_background(canvas, theme_index)
    theme = BACKGROUND_THEMES[theme_index]
    
    # Header section with decorative background
    canvas.create_rectangle(80, 130, CANVAS_WIDTH - 80, 170, "#FFFFFF90", theme["accent"])
    
    # Progress and info
    progress = f"Question {question_num} of {total_questions}"
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 145, progress, 18, "#2C3E50")
    
    # Topic and difficulty
    topic_diff = f"Topic: {question_data['topic']} | Difficulty: {question_data['difficulty']}"
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 185, topic_diff, 14, "#7F8C8D")
    
    # Progress bar with decorative frame
    progress_width = 600
    progress_x = (CANVAS_WIDTH - progress_width) // 2
    canvas.create_rectangle(progress_x - 5, 200, progress_x + progress_width + 5, 220, theme["secondary"], theme["accent"])
    canvas.create_rectangle(progress_x, 205, progress_x + progress_width, 215, "#ECF0F1", "#BDC3C7")
    filled_width = int((question_num / total_questions) * progress_width)
    canvas.create_rectangle(progress_x, 205, progress_x + filled_width, 215, "#3498DB", "#2980B9")
    
    # Question box with decorative elements
    canvas.create_rectangle(100, 240, CANVAS_WIDTH - 100, 350, "#FFFFFF95", theme["accent"])
    canvas.create_rectangle(105, 245, CANVAS_WIDTH - 105, 345, theme["primary"], theme["secondary"])
    
    # Decorative corners
    canvas.create_oval(110, 250, 125, 265, theme["accent"], theme["accent"])
    canvas.create_oval(CANVAS_WIDTH - 125, 250, CANVAS_WIDTH - 110, 265, theme["accent"], theme["accent"])
    
    # Question text (wrapped)
    question_lines = wrap_text(question_data['question'], CANVAS_WIDTH - 140, 16)
    start_y = 270
    for i, line in enumerate(question_lines):
        draw_centered_text(canvas, CANVAS_WIDTH / 2, start_y + i * 25, line, 16, "#2C3E50")
    
    # Answer options with enhanced styling
    option_buttons = []
    colors = ["#E74C3C", "#3498DB", "#27AE60", "#F39C12"]  # Red, Blue, Green, Orange
    
    for i, option in enumerate(question_data['options']):
        x = 120 + (i % 2) * 320
        y = 380 + (i // 2) * 80
        
        # Option background with border
        canvas.create_rectangle(x - 5, y - 5, x + 285, y + 65, "#FFFFFF80", colors[i])
        
        btn, bounds = draw_button(canvas, f"{chr(65 + i)}. {option}", x, y, 280, 60, colors[i])
        option_buttons.append((btn, bounds, i))
    
    return option_buttons

def draw_result_screen(canvas, score, total_questions, correct_answers, theme_index):
    """Draw the final results screen"""
    draw_background(canvas, theme_index)
    theme = BACKGROUND_THEMES[theme_index]
    
    percentage = (score / total_questions) * 100
    
    # Title based on performance
    if percentage >= 90:
        title = "🏆 EXCELLENT! 🏆"
        subtitle = "Python Master!"
        color = "#27AE60"
    elif percentage >= 70:
        title = "🎉 GREAT JOB! 🎉"
        subtitle = "Python Expert!"
        color = "#3498DB"
    elif percentage >= 50:
        title = "👍 GOOD EFFORT! 👍"
        subtitle = "Keep Learning!"
        color = "#F39C12"
    else:
        title = "📚 KEEP STUDYING! 📚"
        subtitle = "Practice Makes Perfect!"
        color = "#E74C3C"
    
    # Title background
    canvas.create_rectangle(150, 140, CANVAS_WIDTH - 150, 190, "#FFFFFF90", color)
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 165, title, 28, color)
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 210, subtitle, 18, "#34495E")
    
    # Score box with decorative frame
    canvas.create_rectangle(200, 240, CANVAS_WIDTH - 200, 430, "#FFFFFF95", theme["accent"])
    canvas.create_rectangle(205, 245, CANVAS_WIDTH - 205, 425, theme["primary"], theme["secondary"])
    
    # Decorative elements
    canvas.create_oval(220, 255, 240, 275, theme["accent"], theme["accent"])
    canvas.create_oval(CANVAS_WIDTH - 240, 255, CANVAS_WIDTH - 220, 275, theme["accent"], theme["accent"])
    
    # Score details
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 280, "📊 YOUR RESULTS", 20, "#2C3E50")
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 320, f"Score: {score}/{total_questions}", 24, color)
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 350, f"Percentage: {percentage:.1f}%", 18, "#34495E")
    
    # Performance breakdown by topic
    topic_stats = {}
    for q in correct_answers:
        topic = q['topic']
        if topic not in topic_stats:
            topic_stats[topic] = {'correct': 0, 'total': 0}
        topic_stats[topic]['total'] += 1
        if q['user_correct']:
            topic_stats[topic]['correct'] += 1
    
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 380, "📈 Performance by Topic:", 14, "#2C3E50")
    y_offset = 400
    for topic, stats in topic_stats.items():
        perc = (stats['correct'] / stats['total']) * 100
        text = f"{topic}: {stats['correct']}/{stats['total']} ({perc:.0f}%)"
        draw_centered_text(canvas, CANVAS_WIDTH / 2, y_offset, text, 12, "#34495E")
        y_offset += 20
    
    # Buttons with decorative backgrounds
    canvas.create_rectangle(CANVAS_WIDTH // 2 - 225, 480, CANVAS_WIDTH // 2 - 35, 535, "#FFFFFF80", "#3498DB")
    canvas.create_rectangle(CANVAS_WIDTH // 2 + 15, 480, CANVAS_WIDTH // 2 + 205, 535, "#FFFFFF80", "#27AE60")
    
    retry_btn = draw_button(canvas, "🔄 TRY AGAIN", CANVAS_WIDTH // 2 - 220, 485, 180, 50, "#3498DB")
    review_btn = draw_button(canvas, "📝 REVIEW ANSWERS", CANVAS_WIDTH // 2 + 20, 485, 180, 50, "#27AE60")
    
    return retry_btn, review_btn

def draw_review_screen(canvas, correct_answers, current_review, theme_index):
    """Draw the answer review screen"""
    draw_background(canvas, theme_index)
    theme = BACKGROUND_THEMES[theme_index]
    
    question = correct_answers[current_review]
    
    # Header with decorative frame
    canvas.create_rectangle(200, 140, CANVAS_WIDTH - 200, 180, "#FFFFFF90", theme["accent"])
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 160, f"Review: Question {current_review + 1}/{len(correct_answers)}", 18, "#2C3E50")
    
    # Question box with enhanced styling
    canvas.create_rectangle(100, 200, CANVAS_WIDTH - 100, 280, "#FFFFFF95", theme["accent"])
    canvas.create_rectangle(105, 205, CANVAS_WIDTH - 105, 275, theme["primary"], theme["secondary"])
    
    # Decorative elements
    canvas.create_oval(115, 215, 130, 230, theme["accent"], theme["accent"])
    canvas.create_oval(CANVAS_WIDTH - 130, 215, CANVAS_WIDTH - 115, 230, theme["accent"], theme["accent"])
    
    question_lines = wrap_text(question['question'], CANVAS_WIDTH - 140, 14)
    start_y = 225
    for i, line in enumerate(question_lines):
        draw_centered_text(canvas, CANVAS_WIDTH / 2, start_y + i * 20, line, 14, "#2C3E50")
    
    # Options with correct/incorrect marking and backgrounds
    for i, option in enumerate(question['options']):
        y = 310 + i * 40
        
        if i == question['correct']:
            # Correct answer - green background
            canvas.create_rectangle(150, y - 15, CANVAS_WIDTH - 150, y + 15, "#D5EDDA", "#27AE60")
            color = "#27AE60"
            marker = "✓"
        elif i == question['user_answer']:
            # User's wrong answer - red background
            canvas.create_rectangle(150, y - 15, CANVAS_WIDTH - 150, y + 15, "#F8D7DA", "#E74C3C")
            color = "#E74C3C"
            marker = "✗"
        else:
            # Other options - neutral background
            canvas.create_rectangle(150, y - 15, CANVAS_WIDTH - 150, y + 15, "#F8F9FA", "#DEE2E6")
            color = "#34495E"
            marker = " "
        
        text = f"{marker} {chr(65 + i)}. {option}"
        draw_centered_text(canvas, CANVAS_WIDTH / 2, y, text, 14, color)
    
    # Status with decorative background
    status = "✅ Correct!" if question['user_correct'] else "❌ Incorrect"
    status_color = "#27AE60" if question['user_correct'] else "#E74C3C"
    canvas.create_rectangle(300, 475, CANVAS_WIDTH - 300, 505, "#FFFFFF90", status_color)
    draw_centered_text(canvas, CANVAS_WIDTH / 2, 490, status, 16, status_color)
    
    # Navigation buttons with enhanced styling
    nav_y = 520
    if current_review > 0:
        canvas.create_rectangle(145, nav_y - 5, 305, nav_y + 45, "#FFFFFF80", "#95A5A6")
        prev_btn = draw_button(canvas, "⬅ Previous", 150, nav_y, 150, 40, "#95A5A6")
    else:
        prev_btn = None
        
    if current_review < len(correct_answers) - 1:
        canvas.create_rectangle(345, nav_y - 5, 505, nav_y + 45, "#FFFFFF80", "#95A5A6")
        next_btn = draw_button(canvas, "Next ➡", 350, nav_y, 150, 40, "#95A5A6")
    else:
        next_btn = None
        
    canvas.create_rectangle(515, nav_y - 5, 700, nav_y + 45, "#FFFFFF80", "#3498DB")
    back_btn = draw_button(canvas, "🔙 Back to Results", 520, nav_y, 180, 40, "#3498DB")
    
    return prev_btn, next_btn, back_btn

def main():
    """Main game loop"""
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    fixed_theme_index = 1  # Choose a fixed background theme (e.g., Ocean Blue)
    
    while True:  # Main game loop
        # Start screen
        while True:
            start_btn = draw_start_screen(canvas, fixed_theme_index)
            click = canvas.get_last_click()
            
            if click and is_click_inside(click, start_btn[1]):
                break
            
            time.sleep(1)
        
        # Quiz phase
        questions = random.sample(QUIZ_QUESTIONS, len(QUIZ_QUESTIONS))  # Shuffle all questions
        score = 0
        correct_answers = []
        
        for q_num, question in enumerate(questions, 1):
            while True:
                option_buttons = draw_question_screen(canvas, question, q_num, len(questions), fixed_theme_index)
                click = canvas.get_last_click()
                
                if click:
                    for btn, bounds, option_idx in option_buttons:
                        if is_click_inside(click, bounds):
                            # Record answer
                            user_correct = option_idx == question['correct']
                            if user_correct:
                                score += 1
                            
                            # Store for review
                            correct_answers.append({
                                'question': question['question'],
                                'options': question['options'],
                                'correct': question['correct'],
                                'user_answer': option_idx,
                                'user_correct': user_correct,
                                'topic': question['topic']
                            })
                            
                            # Visual feedback
                            feedback_color = "#27AE60" if user_correct else "#E74C3C"
                            feedback_text = "✅ Correct!" if user_correct else f"❌ Wrong! Answer: {chr(65 + question['correct'])}"
                            
                            canvas.create_rectangle(0, CANVAS_HEIGHT - 80, CANVAS_WIDTH, CANVAS_HEIGHT, feedback_color, feedback_color)
                            draw_centered_text(canvas, CANVAS_WIDTH / 2, CANVAS_HEIGHT - 40, feedback_text, 18, "white")
                            
                            time.sleep(1)
                            break
                    else:
                        continue
                    break
                
                time.sleep(1)
        
        # Results screen
        current_review = 0
        while True:
            retry_btn, review_btn = draw_result_screen(canvas, score, len(questions), correct_answers, fixed_theme_index)
            click = canvas.get_last_click()
            
            if click:
                if is_click_inside(click, retry_btn[1]):
                    break  # Restart game
                elif is_click_inside(click, review_btn[1]):
                    # Review answers
                    while True:
                        prev_btn, next_btn, back_btn = draw_review_screen(canvas, correct_answers, current_review, fixed_theme_index)
                        click = canvas.get_last_click()
                        
                        if click:
                            if prev_btn and is_click_inside(click, prev_btn[1]):
                                current_review = max(0, current_review - 1)
                            elif next_btn and is_click_inside(click, next_btn[1]):
                                current_review = min(len(correct_answers) - 1, current_review + 1)
                            elif is_click_inside(click, back_btn[1]):
                                break
                        
                        time.sleep(1)
            
            time.sleep(1)

if __name__ == "__main__":
    main()