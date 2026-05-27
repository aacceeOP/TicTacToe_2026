import random

def new_board():
    return [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]


def render(board):

    print("\n  1 2 3")

    for i, row in enumerate(board):

        rendered_row = []

        for square in row:
            if square is None:
                rendered_row.append("-")
            else:
                rendered_row.append(square)

        print(f"{i + 1} " + " ".join(rendered_row))

    print()


def get_move():
    while True:
        x = input("What is your row (1-3)? ").strip()
        y = input("What is your column (1-3)? ").strip()
        if len(x) != 1 or len(y) != 1:
            print("Enter only one digit.")
            continue

        if x not in "123" or y not in "123":
            print("Please enter numbers from 1 to 3.")
            continue

        return (int(x) - 1, int(y) - 1)
    

def human_player(board, side):
    return get_move()

def get_legal_moves(board):
    legal_moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                legal_moves.append((row, col))

    return legal_moves

def random_player(board, side): # has two variables so its consistent
    legal_moves = get_legal_moves(board)
    return random.choice(legal_moves)

# the new stuff 
def get_opponent(side):
    if side == "X":
        return "O"
    else:
        return "X"


def find_winning_move(board, side):
    legal_moves = get_legal_moves(board)

    for move in legal_moves:
        new_board = make_move(board, move, side)

        if get_winner(new_board) == side:
            return move

    return None

def minimax(board, current_side, ai_side):
    winner = get_winner(board)

    if winner == ai_side:
        return 1

    if winner is not None:
        return -1
    
    if is_board_full(board):
        return 0
    
    legal_moves = get_legal_moves(board)

    if current_side == ai_side:
        best_score = -999
        for move in legal_moves:
            new_board = make_move(board, move, current_side)
            score = minimax(new_board, get_opponent(current_side), ai_side)
            if score > best_score:
                best_score = score

        return best_score
    else:
        best_score = 999
        for move in legal_moves:
            new_board = make_move(board, move, current_side)
            score = minimax(new_board, get_opponent(current_side), ai_side)
            if score < best_score:
                best_score = score
        return best_score
    
def minimax_player(baord, side):
    legal_moves = get_legal_moves(board)
    best_score = -999
    best_move = None
    for move in legal_moves:
        new_board = make_move(board, move, side)
        score = minimax(new_board, get_opponent(side), side)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move



def smart_player(board, side):
    # 1. Win if possible
    move = find_winning_move(board, side)
    if move is not None:
        return move

    # 2. Block opponent if needed
    opponent = get_opponent(side)
    move = find_winning_move(board, opponent)
    if move is not None:
        return move

    # 3. Take center if available
    if board[1][1] is None:
        return (1, 1)

    # 4. Otherwise random
    return random_player(board, side)


def make_move(old_board, move, side):
    row, col = move

    # duplicate the board properly
    new_board = [r.copy() for r in old_board]

    # check if occupied
    if new_board[row][col] is not None:
        print("That square is already taken!")
        return None

    # place the move
    new_board[row][col] = side

    return new_board


def get_winner(board):

    lines = []

    # rows
    lines.extend(board)

    # columns
    for col in range(3):
        lines.append([
            board[0][col],
            board[1][col],
            board[2][col]
        ])

    # diagonals
    lines.append([
        board[0][0],
        board[1][1],
        board[2][2]
    ])

    lines.append([
        board[0][2],
        board[1][1],
        board[2][0]
    ])

    # check all lines
    for line in lines:
        if line == ["X", "X", "X"]:
            return "X"

        if line == ["O", "O", "O"]:
            return "O"

    return None


def is_board_full(board):

    for row in board:
        for square in row:
            if square is None:
                return False

    return True

x_player = human_player
o_player = minimax_player

# MAIN GAME LOOP

board = new_board()

turn = 0

while True:

    render(board)

    # choose player
    if turn % 2 == 0:
        player = "X"
        move = x_player(board, player)
    else:
        player = "O"
        move = o_player(board, player)

    print(f"Player {player}'s turn")



    new_board = make_move(board, move, player)

    if new_board is None:
        continue

    board = new_board

    winner = get_winner(board)

    if winner is not None:
        render(board)
        print(f"{winner} wins!")
        break

    if is_board_full(board):
        render(board)
        print("It's a draw!")
        break

    turn += 1

