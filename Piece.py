# This class represents the different pieces that Fairy Stockfish udnerstands
from typing import List



class Piece:

    pieces: List = []

    def __init__(self, name:str, iniName:str, betza:str, preferredChar:str, preferredIconIndexes: List[int], royal=False):
        """

        :param name: The human-readable name of this piece
        :param iniName: The name that Fairy-Stockfish will recognize when read in variants.ini
        :param betza: The betza notation for this piece
        :param preferredChar: The preferred character for this piece.
        :param preferredIconIndexes: A list of preferred indexes into winBoard's pieceToCharTable. First one is most preferred, then onwards.
        :param royal: Whether this piece is ordinarily royal
        """

        Piece.pieces.append(self)

        self.name = name
        self.iniName = iniName
        self.betza = betza
        self.preferredChar = preferredChar.lower()
        self.preferredIconIndexes = preferredIconIndexes

class Pieces:

    ALFIL = Piece("Alfil", "alfil", "A", "a", [13, 18, 2])

    PAWN = Piece("Pawn", "pawn", "fmWfceF", "p", [0])
    KNIGHT = Piece("Knight", "knight", "N", "n", [1])
    BISHOP = Piece("Bishop", "bishop", "B", "b", [2])
    ROOK = Piece("Rook", "rook", "R", "r", [3])
    QUEEN = Piece("Queen", "queen", "RB", "q", [4])
    KING = Piece("King", "king", "K", "k", [21], royal=True)

