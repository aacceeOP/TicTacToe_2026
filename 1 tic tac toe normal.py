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
        x = input("What is your row (1-3)? ")
        y = input("What is your column (1-3)? ")

        if x not in "123" or y not in "123":
            print("Please enter numbers from 1 to 3.")
            continue

        return (int(x) - 1, int(y) - 1)


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


# MAIN GAME LOOP

board = new_board()

turn = 0

while True:

    render(board)

    # choose player
    if turn % 2 == 0:
        player = "X"
    else:
        player = "O"

    print(f"Player {player}'s turn")

    move = get_move()

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
