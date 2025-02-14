import itertools

# Game Board
board = [' ' for _ in range(9)]

# Check if the given position on the board is empty
def is_empty(position):
    return board[position] == ' '

# Place a marker (X or O) at the given position
def place_marker(marker, position):
    board[position] = marker

# Print the current state of the game board
def print_board():
    for i in range(3):
        print(" | ".join(board[i*3:i*3+3]))
        if i < 2:
            print("-" * 9)

# Check if there's a winner
def check_win(player):
    # Rows
    for row in range(3):
        if all(board[row * 3 + i] == player for i in range(3)):
            return True
    # Columns
    for col in range(3):
        if all(board[i * 3 + col] == player for i in range(3)):
            return True
    # Diagonals
    if all(board[i] == player for i in [0, 4, 8]) or \
       all(board[i] == player for i in [2, 4, 6]):
        return True
    return False

# Check if the game is over (draw)
def game_over():
    return check_win('X') or check_win('O') or not any(is_empty(i) for i in range(9))

# Minimax Algorithm with Alpha-Beta Pruning
def minimax(depth, alpha, beta, maximizing_player):
    if check_win('X'):
        return {'utility': 1, 'move': None}
    if check_win('O'):
        return {'utility': -1, 'move': None}
    if not any(is_empty(i) for i in range(9)):
        return {'utility': 0, 'move': None}

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in [i for i, cell in enumerate(board) if is_empty(i)]:
            place_marker('X', move)
            eval = minimax(depth + 1, alpha, beta, False)['utility']
            place_marker(' ', move)  # Backtrack
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return {'utility': max_eval, 'move': best_move}
    else:
        min_eval = float('inf')
        best_move = None
        for move in [i for i, cell in enumerate(board) if is_empty(i)]:
            place_marker('O', move)
            eval = minimax(depth + 1, alpha, beta, True)['utility']
            place_marker(' ', move)  # Backtrack
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return {'utility': min_eval, 'move': best_move}

# Get the best move for the AI
def get_ai_move():
    return minimax(0, float('-inf'), float('inf'), True)['move']

# Play the game
def play_game():
    turn = 'O'  # Human starts first
    while not game_over():
        print_board()
        if turn == 'O':
            human_move = int(input(f"Player {turn}, enter your move (1-9): ")) - 1
            while human_move not in range(9) or not is_empty(human_move):
                human_move = int(input("Invalid move! Enter again (1-9): ")) - 1
            place_marker(turn, human_move)
            turn = 'X'
        else:
            print("AI is making a move...")
            ai_move = get_ai_move()
            if ai_move is not None:
                place_marker('X', ai_move)
            turn = 'O'
    
    print_board()
    if check_win('X'):
        print("AI wins!")
    elif check_win('O'):
        print("You win!")
    else:
        print("It's a draw!")

play_game()
