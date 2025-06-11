from graphics import Canvas
import time
import random
import math
#from playsound import playsound # Import the playsound library

# === API Configuration ===
# Add your API key here for AI integration
API_KEY = ""    # Put your API key here when you get one

# Define the dimensions of the canvas
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

# Define the number of squares per side for a standard chessboard (8x8)
NUM_SQUARES_PER_SIDE = 8

# Calculate the size of each square
SQUARE_SIZE = CANVAS_WIDTH / NUM_SQUARES_PER_SIDE

# Define a list of color schemes for the chessboard
COLOR_SCHEMES = [
    ["ghostwhite", "lightgray"],     # Classic black and white
    ["powderblue", "lightsteelblue"],   # Blue theme
    ["honeydew", "palegreen"], # Green theme
    ["lavenderblush", "thistle"],     # Pink and purple theme
    ["oldlace", "tan"],     # Earthy tones
    ["lemonchiffon", "burlywood"],    # Gold and brown
    ["whitesmoke", "silver"],   # Gray scale
    ["peachpuff", "lightcoral"],    # Red/Orange theme
    ["azure", "aquamarine"],   # Teal theme
    ["ghostwhite", "lightslateblue"],     # Purple/Blue theme
    ["mintcream", "lightcyan"], # Mint/Cyan theme
    ["mistyrose", "lightpink"], # Rose/Pink theme
    ["linen", "wheat"], # Earthy tones
    ["floralwhite", "navajowhite"], # Cream/Orange theme
    ["aliceblue", "cornflowerblue"], # Light blue shades
    ["seashell", "lightsalmon"], # Coral/Peach theme
    ["snow", "gainsboro"], # Very light gray theme
    ["lavender", "mediumpurple"], # Deeper purple/blue
    ["beige", "darkseagreen"], # Greenish beige
    ["ivory", "darkkhaki"], # Ivory/Khaki
]

# Piece representation mapping (for image files)
PIECE_IMAGES = {
    'R': 'bR.png',  # Black Rook
    'N': 'bN.png',  # Black Knight
    'B': 'bB.png',  # Black Bishop
    'Q': 'bQ.png',  # Black Queen
    'K': 'bK.png',  # Black King
    'P': 'bp.png',  # Black Pawn
    'r': 'wR.png',  # White Rook
    'n': 'wN.png',  # White Knight
    'b': 'wB.png',  # White Bishop
    'q': 'wQ.png',  # White Queen
    'k': 'wK.png',  # White King
    'p': 'wp.png'   # White Pawn
}

# Sound file constants (these will no longer be used for playback)
CAPTURE_SOUND_FILE = "capture.mp3"
MOVE_SOUND_FILE = "move-sound.mp3"

# Game state variables
class GameState:
    def __init__(self):
        self.board = self.get_initial_board()
        self.selected_piece = None  # (row, col) of selected piece
        self.selected_square_id = None  # Canvas object ID for highlighting
        self.possible_moves = []  # List of (row, col) tuples
        self.move_highlights = []  # List of canvas object IDs for move highlights
        self.current_player = 'white'  # 'white' or 'black'
        self.piece_objects = {}  # Dictionary to store piece canvas objects
        self.is_game_over = False
        self.winner = None
        
    def get_initial_board(self):
        """Returns the standard initial chess board setup."""
        return [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],   # Black pieces (uppercase)
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],   # Black pawns
            ['', '', '', '', '', '', '', ''],           # Empty row
            ['', '', '', '', '', '', '', ''],           # Empty row
            ['', '', '', '', '', '', '', ''],           # Empty row
            ['', '', '', '', '', '', '', ''],           # Empty row
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],   # White pawns (lowercase)
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']    # White pieces
        ]

# --- Helper functions for drawing text and buttons ---

def estimate_text_width(text, font_size):
    """Estimates the width of the text for centering purposes."""
    return font_size * 0.45 * len(text)

def draw_centered_text(canvas, center_x, y, text, font_size, color):
    """Draws text centered horizontally at a given y-coordinate."""
    text_width = estimate_text_width(text, font_size)
    true_x = center_x - text_width / 2
    return canvas.create_text(
        true_x, y,
        text,
        font='Arial',
        font_size=font_size,
        color=color
    )

def draw_button(canvas, x, y, width, height, text,
                main_color="#4A90E2", outline_color="#2C5282",
                shadow_color="#333333", highlight_color="#87CEEB",
                text_color="white", font_size=16):
    """
    Draws a styled button on the canvas.
    Returns a tuple of (button_rect_id, button_text_id).
    """
    shadow_offset = 3
    # Draw button shadow for a raised effect
    canvas.create_rectangle(
        x + shadow_offset, y + shadow_offset,
        x + width + shadow_offset, y + height + shadow_offset,
        shadow_color, shadow_color
    )

    # Draw the main button rectangle
    button_rect = canvas.create_rectangle(
        x, y,
        x + width, y + height,
        main_color, outline_color
    )

    # Draw a highlight at the top for a glossy effect
    canvas.create_rectangle(
        x + 2, y + 2,
        x + width - 2, y + 15,
        highlight_color, highlight_color
    )

    # Draw the button text, centered on the button
    text_y = y + height / 2 - font_size / 2
    button_label = draw_centered_text(canvas, x + width / 2, text_y, text, font_size, text_color)

    return button_rect, button_label

# --- Chessboard drawing function ---

def draw_chessboard_squares(canvas, light_color, dark_color):
    """
    Draws the chessboard squares on the given canvas with the specified light and dark colors.
    """
    for row in range(NUM_SQUARES_PER_SIDE):
        for col in range(NUM_SQUARES_PER_SIDE):
            left_x = col * SQUARE_SIZE
            top_y = row * SQUARE_SIZE
            right_x = (col + 1) * SQUARE_SIZE
            bottom_y = (row + 1) * SQUARE_SIZE

            if (row + col) % 2 == 0:
                color = light_color
            else:
                color = dark_color

            canvas.create_rectangle(
                left_x, top_y, right_x, bottom_y, color
            )

def draw_pieces(canvas, game_state):
    """Draws all pieces on the board based on the current board state."""
    # Clear existing piece objects
    for piece_id in game_state.piece_objects.values():
        canvas.delete(piece_id)
    game_state.piece_objects.clear()
    
    for r in range(NUM_SQUARES_PER_SIDE):
        for c in range(NUM_SQUARES_PER_SIDE):
            piece = game_state.board[r][c]
            if piece != '':
                image_file = PIECE_IMAGES.get(piece, None)
                
                if image_file:
                    # Calculate position (top-left corner of the square with small padding)
                    left_x = c * SQUARE_SIZE + 5
                    top_y = r * SQUARE_SIZE + 5
                    
                    # Calculate size (square size minus padding)
                    piece_size = SQUARE_SIZE - 10
                    
                    try:
                        # Draw the piece image and store its ID
                        piece_id = canvas.create_image_with_size(
                            left_x, top_y, 
                            piece_size, piece_size, 
                            image_file
                        )
                        game_state.piece_objects[(r, c)] = piece_id
                    except:
                        # Fallback to text if image loading fails
                        fallback_chars = {
                            'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
                            'r': '♖', 'n': '♘', 'b': '♗', 'q': '♕', 'k': '♔', 'p': '♙'
                        }
                        char = fallback_chars.get(piece, '?')
                        piece_color = "black" if piece.isupper() else "white"
                        center_x = c * SQUARE_SIZE + SQUARE_SIZE / 2
                        center_y = r * SQUARE_SIZE + SQUARE_SIZE / 2
                        piece_id = draw_centered_text(canvas, center_x, center_y - 10, char, int(SQUARE_SIZE * 0.7), piece_color)
                        game_state.piece_objects[(r, c)] = piece_id

def get_square_from_click(click_x, click_y):
    """Convert click coordinates to board square (row, col)."""
    col = int(click_x // SQUARE_SIZE)
    row = int(click_y // SQUARE_SIZE)
    
    if 0 <= row < NUM_SQUARES_PER_SIDE and 0 <= col < NUM_SQUARES_PER_SIDE:
        return (row, col)
    return None

def highlight_square(canvas, row, col, color="yellow", alpha=0.5):
    """Highlight a specific square on the board."""
    left_x = col * SQUARE_SIZE
    top_y = row * SQUARE_SIZE
    right_x = (col + 1) * SQUARE_SIZE
    bottom_y = (row + 1) * SQUARE_SIZE
    
    return canvas.create_rectangle(
        left_x + 2, top_y + 2, right_x - 2, bottom_y - 2,
        color, color
    )

def clear_highlights(canvas, game_state):
    """Clear all move highlights from the board."""
    if game_state.selected_square_id:
        canvas.delete(game_state.selected_square_id)
        game_state.selected_square_id = None
    
    for highlight_id in game_state.move_highlights:
        canvas.delete(highlight_id)
    game_state.move_highlights.clear()

def is_valid_position(row, col):
    """Check if position is within board boundaries."""
    return 0 <= row < NUM_SQUARES_PER_SIDE and 0 <= col < NUM_SQUARES_PER_SIDE

def is_enemy_piece(piece1, piece2):
    """Check if two pieces are enemies (different colors)."""
    if not piece1 or not piece2:
        return False
    return piece1.isupper() != piece2.isupper()

def is_friendly_piece(piece1, piece2):
    """Check if two pieces are friendly (same color)."""
    if not piece1 or not piece2:
        return False
    return piece1.isupper() == piece2.isupper()

def get_possible_moves(game_state, row, col):
    """Get all possible moves for a piece at the given position."""
    piece = game_state.board[row][col]
    if not piece:
        return []
    
    moves = []
    piece_type = piece.lower()
    
    if piece_type == 'p':  # Pawn
        moves = get_pawn_moves(game_state, row, col, piece)
    elif piece_type == 'r':  # Rook
        moves = get_rook_moves(game_state, row, col)
    elif piece_type == 'n':  # Knight
        moves = get_knight_moves(game_state, row, col)
    elif piece_type == 'b':  # Bishop
        moves = get_bishop_moves(game_state, row, col)
    elif piece_type == 'q':  # Queen
        moves = get_queen_moves(game_state, row, col)
    elif piece_type == 'k':  # King
        moves = get_king_moves(game_state, row, col)
    
    return moves

def get_pawn_moves(game_state, row, col, piece):
    """Get possible moves for a pawn."""
    moves = []
    direction = -1 if piece.islower() else 1  # White pawns move up (-1), black pawns move down (+1)
    start_row = 6 if piece.islower() else 1
    
    # Move forward one square
    new_row = row + direction
    if is_valid_position(new_row, col) and not game_state.board[new_row][col]:
        moves.append((new_row, col))
        
        # Move forward two squares from starting position
        if row == start_row:
            new_row = row + 2 * direction
            if is_valid_position(new_row, col) and not game_state.board[new_row][col]:
                moves.append((new_row, col))
    
    # Capture diagonally
    for dc in [-1, 1]:
        new_row, new_col = row + direction, col + dc
        if is_valid_position(new_row, new_col):
            target = game_state.board[new_row][new_col]
            if target and is_enemy_piece(piece, target):
                moves.append((new_row, new_col))
    
    return moves

def get_rook_moves(game_state, row, col):
    """Get possible moves for a rook."""
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
    
    for dr, dc in directions:
        for i in range(1, NUM_SQUARES_PER_SIDE):
            new_row, new_col = row + i * dr, col + i * dc
            if not is_valid_position(new_row, new_col):
                break
            
            target = game_state.board[new_row][new_col]
            if not target:
                moves.append((new_row, new_col))
            elif is_enemy_piece(game_state.board[row][col], target):
                moves.append((new_row, new_col))
                break
            else:
                break
    
    return moves

def get_knight_moves(game_state, row, col):
    """Get possible moves for a knight."""
    moves = []
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    
    for dr, dc in knight_moves:
        new_row, new_col = row + dr, col + dc
        if is_valid_position(new_row, new_col):
            target = game_state.board[new_row][new_col]
            if not target or is_enemy_piece(game_state.board[row][col], target):
                moves.append((new_row, new_col))
    
    return moves

def get_bishop_moves(game_state, row, col):
    """Get possible moves for a bishop."""
    moves = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonals
    
    for dr, dc in directions:
        for i in range(1, NUM_SQUARES_PER_SIDE):
            new_row, new_col = row + i * dr, col + i * dc
            if not is_valid_position(new_row, new_col):
                break
            
            target = game_state.board[new_row][new_col]
            if not target:
                moves.append((new_row, new_col))
            elif is_enemy_piece(game_state.board[row][col], target):
                moves.append((new_row, new_col))
                break
            else:
                break
    
    return moves

def get_queen_moves(game_state, row, col):
    """Get possible moves for a queen (combination of rook and bishop)."""
    return get_rook_moves(game_state, row, col) + get_bishop_moves(game_state, row, col)

def get_king_moves(game_state, row, col):
    """Get possible moves for a king."""
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if is_valid_position(new_row, new_col):
            target = game_state.board[new_row][new_col]
            if not target or is_enemy_piece(game_state.board[row][col], target):
                moves.append((new_row, new_col))
    
    return moves

def make_move(game_state, from_pos, to_pos):
    """Make a move on the board."""
    from_row, from_col = from_pos
    to_row, to_col = to_pos
    
    # Check if it's a capture before moving the piece
    is_capture = game_state.board[to_row][to_col] != ''

    # Move the piece
    piece = game_state.board[from_row][from_col]
    game_state.board[from_row][from_col] = ''
    game_state.board[to_row][to_col] = piece

    # Sound playback removed as per user request
    # try:
    #     if is_capture:
    #         playsound(CAPTURE_SOUND_FILE)
    #     else:
    #         playsound(MOVE_SOUND_FILE)
    # except Exception as e:
    #     print(f"Error playing sound: {e}")
    
    # Switch players
    game_state.current_player = 'black' if game_state.current_player == 'white' else 'white'
    
    # Check for game over conditions (simplified)
    check_game_over(game_state)

def check_game_over(game_state):
    """Simple game over check (can be expanded)."""
    # Count kings
    white_king = False
    black_king = False
    
    for row in game_state.board:
        for piece in row:
            if piece == 'k':
                white_king = True
            elif piece == 'K':
                black_king = True
    
    if not white_king:
        game_state.is_game_over = True
        game_state.winner = 'Black'
    elif not black_king:
        game_state.is_game_over = True
        game_state.winner = 'White'

def handle_square_click(canvas, game_state, row, col):
    """Handle clicking on a board square."""
    piece = game_state.board[row][col]
    
    # If no piece is selected
    if game_state.selected_piece is None:
        if piece and ((piece.islower() and game_state.current_player == 'white') or 
                      (piece.isupper() and game_state.current_player == 'black')):
            # Select this piece
            game_state.selected_piece = (row, col)
            game_state.selected_square_id = highlight_square(canvas, row, col, "yellow")
            
            # Get and highlight possible moves
            game_state.possible_moves = get_possible_moves(game_state, row, col)
            for move_row, move_col in game_state.possible_moves:
                highlight_id = highlight_square(canvas, move_row, move_col, "lightgreen")
                game_state.move_highlights.append(highlight_id)
    
    else:
        # A piece is already selected
        selected_row, selected_col = game_state.selected_piece
        
        if (row, col) == game_state.selected_piece:
            # Clicking on the same piece - deselect
            clear_highlights(canvas, game_state)
            game_state.selected_piece = None
            game_state.possible_moves = []
        
        elif (row, col) in game_state.possible_moves:
            # Valid move
            make_move(game_state, game_state.selected_piece, (row, col))
            clear_highlights(canvas, game_state)
            game_state.selected_piece = None
            game_state.possible_moves = []
            draw_pieces(canvas, game_state)
        
        else:
            # Invalid move or selecting another piece
            clear_highlights(canvas, game_state)
            game_state.selected_piece = None
            game_state.possible_moves = []
            
            # If clicking on own piece, select it
            if piece and ((piece.islower() and game_state.current_player == 'white') or 
                          (piece.isupper() and game_state.current_player == 'black')):
                game_state.selected_piece = (row, col)
                game_state.selected_square_id = highlight_square(canvas, row, col, "yellow")
                
                game_state.possible_moves = get_possible_moves(game_state, row, col)
                for move_row, move_col in game_state.possible_moves:
                    highlight_id = highlight_square(canvas, move_row, move_col, "lightgreen")
                    game_state.move_highlights.append(highlight_id)

def make_ai_move(game_state):
    """Make a simple AI move (random for now - can be enhanced with API_KEY)."""
    if API_KEY:
        # TODO: Implement API-based AI move here
        # This is where you would make an API call to get the best move
        print("AI API integration ready - implement your preferred chess API here")
    
    # Simple random AI for demonstration
    all_pieces = []
    for r in range(NUM_SQUARES_PER_SIDE):
        for c in range(NUM_SQUARES_PER_SIDE):
            piece = game_state.board[r][c]
            if piece and ((piece.isupper() and game_state.current_player == 'black') or
                          (piece.islower() and game_state.current_player == 'white')):
                moves = get_possible_moves(game_state, r, c)
                for move in moves:
                    all_pieces.append(((r, c), move))
    
    if all_pieces:
        from_pos, to_pos = random.choice(all_pieces)
        make_move(game_state, from_pos, to_pos)
        return True
    return False

# --- Main game logic ---

def main():
    """
    Main function to initialize the canvas and manage the game states.
    """
    # Fix Canvas initialization - try different approaches
    try:
        canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    except TypeError:
        # Alternative initialization if Canvas is not callable
        try:
            from graphics import Canvas as CanvasClass
            canvas = CanvasClass(CANVAS_WIDTH, CANVAS_HEIGHT)
        except:
            # Last resort - check if Canvas needs different parameters
            print("Error: Could not initialize Canvas. Please check your graphics module installation.")
            print("Make sure you have the correct graphics library installed.")
            return

    # Define game states as constants for clarity
    START_SCREEN = 0
    COLOR_SELECTION = 1
    GAME_ACTIVE = 2
    current_game_state = START_SCREEN

    # Variables for background animation
    last_bg_update_time = time.time()
    current_bg_scheme_index = 0
    animation_interval = 0.5

    chosen_scheme_index = -1
    game_state = GameState()
    vs_ai = False  # Flag to determine if playing against AI

    # Main application loop
    while True:
        # Check for background animation update in START_SCREEN and COLOR_SELECTION states
        if current_game_state == START_SCREEN or current_game_state == COLOR_SELECTION:
            current_time = time.time()
            if current_time - last_bg_update_time >= animation_interval:
                canvas.clear()
                light_color, dark_color = COLOR_SCHEMES[current_bg_scheme_index]
                draw_chessboard_squares(canvas, light_color, dark_color)
                current_bg_scheme_index = (current_bg_scheme_index + 1) % len(COLOR_SCHEMES)
                last_bg_update_time = current_time

        # --- Render UI elements and handle interactions ---
        if current_game_state == START_SCREEN:
            # Game Title with Emojis
            draw_centered_text(canvas, CANVAS_WIDTH / 2-35, CANVAS_HEIGHT / 2 - 110, "♟️♔ Chess Game ♔♟️", 32, "#333333")

            # Start Game button
            start_button_x = CANVAS_WIDTH / 2 - 75
            start_button_y = CANVAS_HEIGHT / 2 - 60
            start_button_width = 150
            start_button_height = 50
            
            draw_button(canvas, start_button_x, start_button_y, start_button_width,
                        start_button_height, "Start Game",
                        main_color="#FF6347", outline_color="#CD5C5C",
                        highlight_color="#FFA07A", text_color="white")
            
            # VS AI button
            ai_button_x = CANVAS_WIDTH / 2 - 75
            ai_button_y = CANVAS_HEIGHT / 2 + 10
            ai_button_width = 150
            ai_button_height = 50
            
            draw_button(canvas, ai_button_x, ai_button_y, ai_button_width,
                        ai_button_height, "Play vs AI",
                        main_color="#4169E1", outline_color="#191970",
                        highlight_color="#6495ED", text_color="white")

            click = canvas.get_last_click()
            if click:
                click_x, click_y = click
                if (start_button_x <= click_x <= start_button_x + start_button_width and
                    start_button_y <= click_y <= start_button_y + start_button_height):
                    vs_ai = False
                    canvas.clear()
                    current_game_state = COLOR_SELECTION
                    last_bg_update_time = time.time()
                    current_bg_scheme_index = 0
                elif (ai_button_x <= click_x <= ai_button_x + ai_button_width and
                      ai_button_y <= click_y <= ai_button_y + ai_button_height):
                    vs_ai = True
                    canvas.clear()
                    current_game_state = COLOR_SELECTION
                    last_bg_update_time = time.time()
                    current_bg_scheme_index = 0

        elif current_game_state == COLOR_SELECTION:
            draw_centered_text(canvas, CANVAS_WIDTH / 2, 20, "Choose a Color Scheme 🏁 :", 20, "#333333")

            button_width = 180
            button_height = 32
            padding_x = 20
            padding_y = 10

            total_width_of_buttons_group = 2 * button_width + padding_x
            start_x_buttons = (CANVAS_WIDTH - total_width_of_buttons_group) / 2
            start_y_buttons = 60

            color_button_rects = []

            for i, scheme in enumerate(COLOR_SCHEMES):
                col_idx = i % 2
                row_idx = i // 2

                btn_x = start_x_buttons + col_idx * (button_width + padding_x)
                btn_y = start_y_buttons + row_idx * (button_height + padding_y)

                scheme_name = f"{scheme[0].capitalize()} / {scheme[1].capitalize()}"

                draw_button(canvas, btn_x, btn_y, button_width, button_height,
                           scheme_name, main_color="#DA70D6", outline_color="#9932CC",
                           text_color="white", font_size=11,
                           highlight_color="#EE82EE")

                color_button_rects.append((btn_x, btn_y, button_width, button_height, i))

            click = canvas.get_last_click()
            if click:
                click_x, click_y = click
                for btn_x, btn_y, btn_w, btn_h, scheme_idx in color_button_rects:
                    if (btn_x <= click_x <= btn_x + btn_w and
                        btn_y <= click_y <= btn_y + btn_h):
                        chosen_scheme_index = scheme_idx
                        canvas.clear()
                        current_game_state = GAME_ACTIVE
                        game_state = GameState()  # Reset game state
                        break

        elif current_game_state == GAME_ACTIVE:
            # Draw the board once
            if chosen_scheme_index != -1:
                light_color, dark_color = COLOR_SCHEMES[chosen_scheme_index]
            else:
                light_color, dark_color = "white", "black"
            
            draw_chessboard_squares(canvas, light_color, dark_color)
            draw_pieces(canvas, game_state)
            
            # Display current player
            player_text = f"Current Player: {game_state.current_player.capitalize()}"
            #draw_centered_text(canvas, CANVAS_WIDTH / 2, CANVAS_HEIGHT - 30, player_text, 16, "#333333")
            
            # Display game mode
            mode_text = "vs AI" if vs_ai else "vs Human"
            #draw_centered_text(canvas, CANVAS_WIDTH / 2, CANVAS_HEIGHT - 10, mode_text, 12, "#666666")
            
            if game_state.is_game_over:
                winner_text = f"Game Over 💀 {game_state.winner} Wins"
                draw_centered_text(canvas, CANVAS_WIDTH / 2-30, CANVAS_HEIGHT /2 , winner_text, 30, "red")
            
            # Handle clicks
            click = canvas.get_last_click()
            if click and not game_state.is_game_over:
                click_x, click_y = click
                square = get_square_from_click(click_x, click_y)
                if square:
                    row, col = square
                    handle_square_click(canvas, game_state, row, col)
            
            # AI move (if vs AI and it's AI's turn)
            if vs_ai and game_state.current_player == 'black' and not game_state.is_game_over:
                time.sleep(1)  # Brief pause for AI "thinking"
                if make_ai_move(game_state):
                    # Removed canvas.clear() here. The main loop will handle the redraw.
                    pass 

        time.sleep(0.01)

if __name__ == '__main__':
    main()
