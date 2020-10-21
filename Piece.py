# This class represents the different pieces that Fairy Stockfish udnerstands
from typing import List
import LatexExport


class Piece:

    pieces: List = []

    def __init__(self, name:str, iniName:str, betza:str, preferredChar:str, preferredIconIndexes: List[int],
                 latexBase="Pawn", latexOrientation="0", royal=False ):
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

        if latexOrientation not in LatexExport.validOrientations:
            raise Exception("Invalid latexOrientation '{0}'! Valid values are only '{1}'."
                            .format(latexOrientation, LatexExport.validOrientations))
        self.latexOrientation = latexOrientation
        self.latexBase = latexBase


PAWN = Piece("Pawn", "pawn", "fmWfceF", "p", [0], "Pawn")
KNIGHT = Piece("Knight", "knight", "N", "n", [1], "Knight")
BISHOP = Piece("Bishop", "bishop", "B", "b", [2], "Bishop")
ROOK = Piece("Rook", "rook", "R", "r", [3], "Rook")
QUEEN = Piece("Queen", "queen", "RB", "q", [4], "Queen")
KING = Piece("King", "king", "K", "k", [21], "King", royal=True)

#                           Name             .ini Name      Betza   Char Winboard       LaTex Subs
ALFIL =             Piece("Alfil",          "alfil",        "A",    "a", [13, 18, 2],   "Bishop",   "180")
AMAZON =            Piece("Amazon",         "amazon",       "RBN",  "z", [15, 4],       "Queen",    "180")
ARCHBISHOP =        Piece("Archbishop",     "archbishop",   "BN",   "i", [20, 12, 1],   "Bishop",   "90")
ARCHCHANCELLOR =    Piece("Archchancellor", "aiwok",        "RNF",  "r", [14, 16, 3],   "Rook",     "90")
CHANCELLOR =        Piece("Chancellor",     "chancellor",   "RN",   "c", [16, 20, 1],   "Rook",     "180")
FERZ =              Piece("Ferz",           "fers",         "F",    "f", [0, 9, 10],    "Pawn",     "180")
LANCE =             Piece("Lance",          "lance",        "fR",   "l", [18, 13],      "Pawn",     "270")
PAWN_SHOGI =        Piece("Shogi Pawn",     "shogiPawn",    "fW",   "q", [0],           "Pawn",     "90")
WAZIR =             Piece("Wazir",          "wazir",        "W",    "w", [5,14,3],      "Rook",     "270")

