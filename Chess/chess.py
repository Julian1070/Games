import random
import sys
import time
import re
from board import Board
from pieces import King, Queen, Rook, Bishop, Knight, Pawn


# A dictionary of the unicode depictions of the pieces
pieces_symbols = {'wK': u'\u2654', 'wQ': u'\u2655', 'wR': u'\u2656', 'wB': u'\u2657', 'wN': u'\u2658', 'wP': u'\u2659',
                  'bK': u'\u265A', 'bQ': u'\u265B', 'bR': u'\u265C', 'bB': u'\u265D', 'bN': u'\u265E', 'bP': u'\u265F'}

# Initiating all pieces with side (white = 1, black = -1), position (column, row), and unicode symbol
wK = King(1, (5, 1), pieces_symbols['wK'])
bK = King(-1, (5, 8), pieces_symbols['bK'])
wQ = Queen(1, (4, 1), pieces_symbols['wQ'])
bQ = Queen(-1, (4, 8), pieces_symbols['bQ'])
wR1 = Rook(1, (1, 1), pieces_symbols['wR'])
wR2 = Rook(1, (8, 1), pieces_symbols['wR'])
bR1 = Rook(-1, (8, 8), pieces_symbols['bR'])
bR2 = Rook(-1, (1, 8), pieces_symbols['bR'])
wB1 = Bishop(1, (3, 1), pieces_symbols['wB'])
wB2 = Bishop(1, (6, 1), pieces_symbols['wB'])
bB1 = Bishop(-1, (3, 8), pieces_symbols['bB'])
bB2 = Bishop(-1, (6, 8), pieces_symbols['bB'])
wN1 = Knight(1, (2, 1), pieces_symbols['wN'])
wN2 = Knight(1, (7, 1), pieces_symbols['wN'])
bN1 = Knight(-1, (2, 8), pieces_symbols['bN'])
bN2 = Knight(-1, (7, 8), pieces_symbols['bN'])
wP1 = Pawn(1, (1, 2), pieces_symbols['wP'])
wP2 = Pawn(1, (2, 2), pieces_symbols['wP'])
wP3 = Pawn(1, (3, 2), pieces_symbols['wP'])
wP4 = Pawn(1, (4, 2), pieces_symbols['wP'])
wP5 = Pawn(1, (5, 2), pieces_symbols['wP'])
wP6 = Pawn(1, (6, 2), pieces_symbols['wP'])
wP7 = Pawn(1, (7, 2), pieces_symbols['wP'])
wP8 = Pawn(1, (8, 2), pieces_symbols['wP'])
bP1 = Pawn(-1, (1, 7), pieces_symbols['bP'])
bP2 = Pawn(-1, (2, 7), pieces_symbols['bP'])
bP3 = Pawn(-1, (3, 7), pieces_symbols['bP'])
bP4 = Pawn(-1, (4, 7), pieces_symbols['bP'])
bP5 = Pawn(-1, (5, 7), pieces_symbols['bP'])
bP6 = Pawn(-1, (6, 7), pieces_symbols['bP'])
bP7 = Pawn(-1, (7, 7), pieces_symbols['bP'])
bP8 = Pawn(-1, (8, 7), pieces_symbols['bP'])

# creating a list of lists with all pieces
wpieces = [wK, wQ, wR1, wR2, wB1, wB2, wN1, wN2, wP1, wP2, wP3, wP4, wP5, wP6, wP7, wP8]
bpieces = [bK, bQ, bR1, bR2, bB1, bB2, bN1, bN2, bP1, bP2, bP3, bP4, bP5, bP6, bP7, bP8]
the_pieces = [wpieces] + [bpieces]

# The board with the pieces added
board_board = [['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] if i == 0 else [i] + 8*['_'] for i in range(9)]
for side in the_pieces:
    for piece in side:
        board_board[piece.position[1]][piece.position[0]] = piece
the_board = Board(board_board, the_pieces)


# This function prints the board
def print_board(board):
    board_viz = board.visualize()
    for row in reversed(board_viz):
        print(row)


# This function makes a move, taking as input the current board configuration and the squares (i.e. initial and final
# position) of the piece to move. Returns new board class instance.
def make_move(board, from_square, to_square):
    if type(board.board[from_square[1]][from_square[0]]).__name__ == "Pawn" and \
            ((to_square[1] == 8 and board.board[from_square[1]][from_square[0]].side == 1) or
             (to_square[1] == 1 and board.board[from_square[1]][from_square[0]].side == -1)):
        print_board(move_promotion(board, from_square, to_square))
        return move_promotion(board, from_square, to_square)
    new_check = False
    new_score = board.score
    board_copy = []
    for row in board.board:
        board_copy.append(list(row))
    own_pieces = list(board.pieces[max(0, -board.side)])
    opponent_pieces = list(board.pieces[-max(0, board.side)])
    if type(board.board[to_square[1]][to_square[0]]) != str and \
            type(board.board[to_square[1]][to_square[0]]) != int and \
            board.board[to_square[1]][to_square[0]].side != board.side:
        if type(board.board[to_square[1]][to_square[0]]).__name__ == "King":
            new_check = True
        new_score += board.side*board.board[to_square[1]][to_square[0]].value
        opponent_pieces.remove(board.board[to_square[1]][to_square[0]])
    own_pieces.remove(board.board[from_square[1]][from_square[0]])
    board_copy[to_square[1]][to_square[0]] = board.board[from_square[1]][from_square[0]].clone(to_square)
    own_pieces.append(board_copy[to_square[1]][to_square[0]])
    board_copy[from_square[1]][from_square[0]] = "_"
    board_copy[to_square[1]][to_square[0]].position = to_square
    new_side = -board.side
    new_move = board.move + 1
    if board.side == 1:
        new_pieces = [own_pieces] + [opponent_pieces]
    else:
        new_pieces = [opponent_pieces] + [own_pieces]
    return Board(board_copy, new_pieces, side=new_side, move=new_move, check=new_check, score=new_score, parent=board)


# Special move: pawn promotion. Turns pawn into queen by default.
def move_promotion(board, from_square, to_square):
    new_check = False
    new_score = board.score
    board_copy = []
    for row in board.board:
        board_copy.append(list(row))
    own_pieces = list(board.pieces[max(0, -board.side)])
    opponent_pieces = list(board.pieces[-max(0, board.side)])
    if type(board.board[to_square[1]][to_square[0]]) != str and \
            type(board.board[to_square[1]][to_square[0]]) != int and \
            board.board[to_square[1]][to_square[0]].side != board.side:
        if type(board.board[to_square[1]][to_square[0]]).__name__ == "King":
            new_check = True
        new_score += board.side*board.board[to_square[1]][to_square[0]].value
        opponent_pieces.remove(board.board[to_square[1]][to_square[0]])
    own_pieces.remove(board.board[from_square[1]][from_square[0]])
    if board.side == 1:
        queen_symbol = pieces_symbols['wQ']
    else:
        queen_symbol = pieces_symbols['bQ']
    board_copy[to_square[1]][to_square[0]] = Queen(board.side, to_square, symbol=queen_symbol, moved=True)
    own_pieces.append(board_copy[to_square[1]][to_square[0]])
    board_copy[from_square[1]][from_square[0]] = "_"
    new_score += board.side*board_copy[to_square[1]][to_square[0]].value
    new_side = -board.side
    new_move = board.move + 1
    if board.side == 1:
        new_pieces = [own_pieces] + [opponent_pieces]
    else:
        new_pieces = [opponent_pieces] + [own_pieces]
    return Board(board_copy, new_pieces, side=new_side, move=new_move, check=new_check, score=new_score, parent=board)


# Special move: castling (king- or queen-side)
def move_castle(board, king_from, king_to, rook_from, rook_to):
    is_check = Board(board.board, board.pieces, side=-board.side, test_check=True)
    moves = find_moves(is_check)
    for move in moves:
            if move.check:
                return False
    board_copy = []
    for row in board.board:
        board_copy.append(list(row))
    own_pieces = list(board.pieces[max(0, -board.side)])
    opponent_pieces = list(board.pieces[-max(0, board.side)])
    own_pieces.remove(board.board[king_from[1]][king_from[0]])
    own_pieces.remove(board.board[rook_from[1]][rook_from[0]])
    board_copy[king_to[1]][king_to[0]] = board.board[king_from[1]][king_from[0]].clone(king_to)
    board_copy[rook_to[1]][rook_to[0]] = board.board[rook_from[1]][rook_from[0]].clone(rook_to)
    own_pieces.append(board_copy[king_to[1]][king_to[0]])
    own_pieces.append(board_copy[rook_to[1]][rook_to[0]])
    board_copy[king_from[1]][king_from[0]] = "_"
    board_copy[rook_from[1]][rook_from[0]] = "_"
    board_copy[king_to[1]][king_to[0]].position = king_to
    board_copy[rook_to[1]][rook_to[0]].position = rook_to
    new_side = -board.side
    new_move = board.move + 1
    if board.side == 1:
        new_pieces = [own_pieces] + [opponent_pieces]
    else:
        new_pieces = [opponent_pieces] + [own_pieces]
    new_score = board.score + 5 * board.side
    return Board(board_copy, new_pieces, side=new_side, move=new_move, score=new_score, parent=board)


# This function finds all moves by going through each piece and listing all possible moves. Returns list of new board
# configurations
def find_moves(board):
    moves = []
    pieces = board.pieces[max(0, -board.side)]
    for piece in pieces:
        if type(piece).__name__ == "Pawn":
            for step in piece.moves():
                initial_position = piece.position
                position = piece.position
                for i in range(piece.reach):
                    if i == 1 and piece.moved:
                        break
                    else:
                        move = ([a+b for a, b in zip(step, position)])
                        if all([1 <= i <= 8 for i in move]):
                            if type(board.board[move[1]][move[0]]) != str and \
                                            type(board.board[move[1]][move[0]]) != int:
                                break
                            else:
                                if (piece.side == 1 and move[1] == 8) or (piece.side == -1 and move[1] == 1):
                                    new_move = move_promotion(board, initial_position, move)
                                    moves.append(new_move)
                                    break
                                new_move = make_move(board, initial_position, move)
                                moves.append(new_move)
                        position = move
            for step in piece.take():
                initial_position = piece.position
                position = piece.position
                move = ([a+b for a, b in zip(step, position)])
                if all([1 <= i <= 8 for i in move]):
                    if type(board.board[move[1]][move[0]]) != str and type(board.board[move[1]][move[0]]) != int:
                        if board.board[move[1]][move[0]].side != piece.side:
                            if (piece.side == 1 and move[1] == 8) or (piece.side == -1 and move[1] == 1):
                                new_move = move_promotion(board, initial_position, move)
                                moves.append(new_move)
                                continue
                            new_move = make_move(board, initial_position, move)
                            moves.insert(0, new_move)
        elif type(piece).__name__ == "King":
            if board.test_check:
                continue
            for step in piece.moves():
                if abs(step[0]) == 2 and not piece.moved:
                    position = piece.position
                    move = ([a+b for a, b in zip(step, position)])
                    rook_end = ([int(0.5*(a+b)) for a, b in zip(position, move)])
                    if type(board.board[move[1]][move[0]]) == str and \
                            type(board.board[rook_end[1]][rook_end[0]]) == str:
                        rook_pos = [[int(1.5*a+b) for a, b in zip(step, position)],
                                    [2*a+b for a, b in zip(step, position)]]
                        for rook in rook_pos:
                            if all([1 <= i <= 8 for i in rook]) and \
                                            type(board.board[rook[1]][rook[0]]).__name__ == "Rook" \
                                    and not board.board[rook[1]][rook[0]].moved:
                                new_move = move_castle(board, position, move, rook, rook_end)
                                if new_move:
                                    moves.append(new_move)
                else:
                    position = piece.position
                    move = ([a+b for a, b in zip(step, position)])
                    if all([1 <= i <= 8 for i in move]):
                        if type(board.board[move[1]][move[0]]) != str and type(board.board[move[1]][move[0]]) != int:
                            if board.board[move[1]][move[0]].side != piece.side:
                                new_move = make_move(board, position, move)
                                moves.insert(0, new_move)
                        else:
                            new_move = make_move(board, position, move)
                            moves.append(new_move)
        else:
            for step in piece.moves():
                initial_position = piece.position
                position = piece.position
                for i in range(piece.reach):
                    move = ([a+b for a, b in zip(step, position)])
                    if all([1 <= i <= 8 for i in move]):
                        if type(board.board[move[1]][move[0]]) != str and type(board.board[move[1]][move[0]]) != int:
                            if board.board[move[1]][move[0]].side != piece.side:
                                new_move = make_move(board, initial_position, move)
                                moves.insert(0, new_move)
                                break
                            else:
                                break
                        else:
                            new_move = make_move(board, initial_position, move)
                            moves.append(new_move)
                    else:
                        break
                    position = move
    return moves


# This function filters out the illegal moves (i.e. check)
def find_legal_moves(moves):
    legal_moves = []
    for move in moves:
        legal = True
        opponent_moves = find_moves(move)
        for opponent_move in opponent_moves:
            if opponent_move.check:
                legal = False
        if legal:
            legal_moves.append(move)
    return legal_moves


# The max function for alpha beta pruning:
def max_value(board, alpha, beta, depth):
    if depth == 2:
        return board.score
    else:
        depth += 1
        v = -9999
        moves = find_legal_moves(find_moves(board))
        if len(moves) == 0:
            return v
        for move in moves:
            v = max(v, min_value(move, alpha, beta, depth))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v


# The min function for alpha beta pruning:
def min_value(board, alpha, beta, depth):
    if depth == 2:
        return board.score
    else:
        depth += 1
        v = 9999
        moves = find_legal_moves(find_moves(board))
        if len(moves) == 0:
            return v
        for move in moves:
            v = min(v, max_value(move, alpha, beta, depth))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


# This function selects the best move (random if several moves have equal evaluation)
def choose_move(board):
    best_moves = []
    moves_utility = []
    moves = find_legal_moves(find_moves(board))
    if len(moves) == 0:
        board.side = -board.side
        mate_moves = find_legal_moves(find_moves(board))
        for move in mate_moves:
            if move.check:
                sys.exit("Checkmate!")
        sys.exit("Draw.")
    if board.side == 1:
        for move in moves:
            moves_utility.append([min_value(move, -9999, 9999, 0), move])
        best_v = max([utility[0] for utility in moves_utility])
    else:
        for move in moves:
            moves_utility.append([max_value(move, -9999, 9999, 0), move])
        best_v = min([utility[0] for utility in moves_utility])
    for utility in moves_utility:
        if utility[0] == best_v:
            best_moves.append(utility[1])
    best_move = random.choice(best_moves)
    print_board(best_move)
    print("Evaluation of move:", int(best_v/10))
    return best_move


# This function let's the player play the AI
def player(board, mode, black=False):
    if mode == 3:
        start = time.time()
        move = choose_move(board)
        end = time.time()
        print("Time for move:", round(end - start, 1), "seconds")
        player(move, 3)
    if black:
        move = choose_move(board)
        player(move, mode)
    moves = find_legal_moves(find_moves(board))
    if len(moves) == 0:
        board.side = -board.side
        mate_moves = find_legal_moves(find_moves(board))
        for move in mate_moves:
            if move.check:
                sys.exit("Checkmate!")
        sys.exit("Draw.")
    ask_from = input("Type the from square (e.g. '5,2')\n\n")
    ask_to = input("Type the to square (e.g. '5,4')\n\n")
    if not (bool(re.match(r'\d,\d', ask_from)) or bool(re.match(r'\d\d,\d\d', ask_from))) or \
            not (bool(re.match(r'\d,\d', ask_to)) or bool(re.match(r'\d\d,\d\d', ask_to))):
        print("Incorrect input. Try again:")
        player(board, mode)
    from_square = tuple(int(x.strip()) for x in ask_from.split(','))
    to_square = tuple(int(x.strip()) for x in ask_to.split(','))
    for x, y in zip(from_square, to_square):
        if not ((x in list(range(1, 9)) and y in list(range(1, 9))) or (x == y == 10) or (x == y == 0)):
            print("Incorrect input. Try again:")
            player(board, mode)
    if from_square == to_square == (0, 0):
        if board.side == 1:
            move = move_castle(board, (5, 1), (7, 1), (8, 1), (6, 1))
        else:
            move = move_castle(board, (5, 8), (7, 8), (8, 8), (6, 8))
    elif from_square == to_square == (10, 10):
        if board.side == 1:
            move = move_castle(board, (5, 1), (3, 1), (1, 1), (4, 1))
        else:
            move = move_castle(board, (5, 8), (3, 8), (1, 8), (4, 8))
    else:
        move = make_move(board, from_square, to_square)
    visualized_moves = [each_move.visualize() for each_move in moves]
    if move.visualize() not in visualized_moves:
        print("Illegal move. Choose a legal move.")
        player(board, mode)
    else:
        print_board(move)
        if mode == 2:
            start = time.time()
            move2 = choose_move(move)
            end = time.time()
            print("Time for move:", round(end - start, 1), "seconds")
            player(move2, mode)
        else:
            player(move, mode)


# ask which side player wants to play (i.e. black or white)
def ask_side():
    print("Which side do you want to play?")
    side = int(input("1: White"
                     "\n2: Black\n\n"))
    if side == 2:
        return True
    elif side == 1:
        return False
    else:
        print("Incorrect input. Try again:")
        ask_side()


# Initiating game:
def start_game():
    print("Welcome to Julian's Chess AI! "
          "\n\nYou can play against another player, against the AI, or you can watch the AI play itself. "
          "\nChoose your playing mode:\n")
    mode = int(input("1: Player vs. Player"
                     "\n2: Player vs. AI "
                     "\n3: AI vs. AI\n\n"))
    explanation = "To play, you need to input the square from which you want to move the piece" \
                  "\nand the square where you want to move the piece. The format is first column" \
                  "\nand then row. For instance, the e4 pawn push requires you to type in the from" \
                  "\nsquare (e2) like this '5,2' and the to square (e4) like this '5,4'. To castle" \
                  "\nkingside, type '0,0' for both squares. To castle queenside, type '10,10' for" \
                  "\nboth squares. Enjoy!"
    if mode == 1:
        print(explanation)
        player(the_board, mode)
    elif mode == 2:
        side = ask_side()
        print(explanation)
        if side:
            print("\nWait for the AI to make the first move...")
        player(the_board, mode, side)
    elif mode == 3:
        print("\nWatch and enjoy!\nWait for the first move...")
        player(the_board, mode)
    else:
        print("Incorrect input. Try again:")
        start_game()
