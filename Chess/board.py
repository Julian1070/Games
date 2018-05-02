# Board class


# Board-class
class Board:
    def __init__(self, board, pieces, side=1, move=0, check=False, score=0, parent=None, test_check=False):
        # Side says whose move it is. White = 1, Black = -1
        self.side = side
        # Board is a list of lists that stores the configuration of the board
        self.board = board
        # Pieces is a list of lists with all pieces on the board. pieces[0] = white pieces and pieces[1] = black pieces
        self.pieces = pieces
        # Move counts the number of moves
        self.move = move
        # True if the board position is a check of the King
        self.check = check
        # Score is the evaluation of the position (negative favoring black, positive favoring white)
        self.score = score
        # Parent stores the previous position
        self.parent = parent
        # True if the algorithm is supposed to check the position for check of the King
        self.test_check = test_check

    # Visualize inserts the unicode depictions of the pieces so that the board can be printed
    def visualize(self):
        board_viz = []
        for row in self.board:
            board_viz.append(list(row))
        for row in self.board:
            for square in row:
                if type(square) != str and type(square) != int:
                    board_viz[square.position[1]][square.position[0]] = square.symbol
        return board_viz
