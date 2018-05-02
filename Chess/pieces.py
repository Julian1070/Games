# Piece classes


# King-class with explanation of arguments
class King:
    def __init__(self, side, position, symbol, moved=False, reach=1, value=9999):
        # The side of the piece: white = 1, black = -1
        self.side = side
        # The piece's position on the board, first column then row (i.e. 5,1 = e1; 2,7 = b7; etc.)
        self.position = position
        # Reach is the distance a piece can move. I.e. King has reach = 1, Queen, Rook and Bishop have reach = 8, etc.
        self.reach = reach
        # Moved is a binary value whether the piece has moved (used for castling and initial pawn push of 2 squares)
        self.moved = moved
        # Symbol is the unicode representation of the chess piece
        self.symbol = symbol
        # The value of the piece (i.e. pawn = 1, bishop & knight = 3, rook = 5, etc.)
        self.value = value

    # Moves is a list of tuples that describe the direction the piece can moved. Used in combination with reach (above)
    def moves(self):
        return [(0, 1), (1, 0), (0, -1), (-1, 0),  (1, 1), (-1, 1), (1, -1), (-1, -1), (2, 0), (-2, 0)]

    # Clone is used to quickly create the same piece with a new position. Note that cloned pieces have always moved.
    def clone(self, new_position):
        return King(self.side, new_position, self.symbol, moved=True, reach=self.reach)


# Queen-class (see King-class for explanation of arguments)
class Queen:
    def __init__(self, side, position, symbol, moved=False, reach=8, value=90):
        self.side = side
        self.position = position
        self.reach = reach
        self.symbol = symbol
        self.moved = moved
        self.value = value

    def moves(self):
        return [(0, 1), (1, 0), (0, -1), (-1, 0),  (1, 1), (-1, 1), (1, -1), (-1, -1)]

    def clone(self, new_position):
        return Queen(self.side, new_position, self.symbol, moved=True, reach=self.reach)


# Rook-class (see King-class for explanation of arguments)
class Rook:
    def __init__(self, side, position, symbol, moved=False, reach=8, value=50):
        self.side = side
        self.position = position
        self.reach = reach
        self.symbol = symbol
        self.moved = moved
        self.value = value

    def moves(self):
        return [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def clone(self, new_position):
        return Rook(self.side, new_position, self.symbol, moved=True, reach=self.reach)


# Bishop-class (see King-class for explanation of arguments)
class Bishop:
    def __init__(self, side, position, symbol, moved=False, reach=8, value=30):
        self.side = side
        self.position = position
        self.reach = reach
        self.symbol = symbol
        self.moved = moved
        self.value = value

    def moves(self):
        return [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    def clone(self, new_position):
        return Bishop(self.side, new_position, self.symbol, moved=True, reach=self.reach)


# Knight-class (see King-class for explanation of arguments)
class Knight:
    def __init__(self, side, position, symbol, moved=False, reach=1, value=30):
        self.side = side
        self.position = position
        self.reach = reach
        self.symbol = symbol
        self.moved = moved
        self.value = value

    def moves(self):
        return [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

    def clone(self, new_position):
        return Knight(self.side, new_position, self.symbol, moved=True, reach=self.reach)


# Pawn-class (see King-class for explanation of arguments)
class Pawn:
    def __init__(self, side, position, symbol, moved=False, reach=2, value=10):
        self.side = side
        self.position = position
        self.moved = moved
        self.reach = reach
        self.symbol = symbol
        self.value = value

    def moves(self):
        return [tuple([self.side*x for x in (0, 1)])]

    def take(self):
        return [tuple([self.side*x for x in (1, 1)]), tuple([self.side*x for x in (-1, 1)])]

    def clone(self, new_position):
        return Pawn(self.side, new_position, self.symbol, moved=True, reach=self.reach)

