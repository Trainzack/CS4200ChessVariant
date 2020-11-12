# This class represents a chess variant.
# This is what the genetic algroithm will develop
import Piece

from typing import Dict, List, Tuple, Optional


def pieceTupleToFENString(pieceTuple: Tuple[Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]]],
                          variantMen: Dict[str, Piece.Piece]) -> str:
    """
    This class turns a 2D tuple of pieces to the characters that will be used in the first field of the FEN string.
    This assumes that  white and black start on their usual sides, with no white pieces on black's side of the board and
    vice versa.
    :param pieceTuple: A 2D tuple of piece
    :param variantMen: A dict where keys are the letter shorthand for the pieces, and the values are the pieces.
    :return: The first section of the FEN string.
    """
    out = ""

    pieceNames = {v: k for k, v in variantMen.items()}

    for i, row in enumerate(pieceTuple):
        emptyCount = 0
        for piece in row:
            if piece is None:
                emptyCount += 1
            else:
                if emptyCount > 0:
                    out += str(emptyCount)
                    emptyCount = 0
                nextChar = pieceNames[piece]
                if i > 3:
                    nextChar = nextChar.upper()
                else:
                    nextChar = nextChar.lower()
                out += nextChar

        if emptyCount > 0:
            out += str(emptyCount)
        out += "/"

    return out[0:-1]


class Variant:
    """Represents a variant of the game chess."""

    def __init__(self, name: str, startingPosition: Tuple[Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]]],
                 pieces: List[Piece.Piece], iniFlags: List[str]=None):
        """

        :param name: The name of this variant
        :param startingPosition: a 2D tuple of the starting position.
        :param pieces: A list of Pieces that this variant uses
        :param iniFlags: A list of strings that will be put in the INI file for this variant.
        """

        self.name = name


        self.pieces = pieces
        self.variantMen = dict() # Letter: piece

        # Fill the variantMen dicitonary
        availableChars = "abcdefghijklmnopqrstuvqxyz" # keep track of what letters we've got left.
        for piece in self.pieces:
            if len(availableChars) <= 0:
                raise Exception("Cannot create variant with more than 26 unique pieces, as we run out of letters.")

            if piece.preferredChar not in self.variantMen.keys():
                nextChar = piece.preferredChar
            else:
                nextChar = availableChars[0]

            availableChars.replace(nextChar, "")
            self.variantMen[nextChar] = piece

        self.startingFEN = pieceTupleToFENString(startingPosition, self.variantMen) + " w KQkq - 0 1"

        self.iniFlags = iniFlags if iniFlags is not None else []

    def getFairyStockfishINI(self) -> str:
        """Returns the fairystockfish ini file that defines this variant"""
        out = "[{0}]\nstartFen = {1}\n".format(self.name, self.startingFEN)
        out += "pieceToCharTable = {0}\n".format(self.getPieceToCharTable())
        for char, piece in self.getVariantMen().items():
            out += "{0} = {1}\n".format(piece.iniName, char)
        for flag in self.iniFlags:
            out += "{0}\n".format(flag)
        return out

    def getVariantMen(self) -> Dict[str, Piece.Piece]:
        """Returns a dict of the following format:

            Key: A str containing the letter of the piece
            Value: The Piece object containing the piece

        For each piece.
        """
        return self.variantMen

    def getPieceToCharTable(self) -> str:
        """
        This is for WinBoard, so that it displays properly. Do not override this method
        :return: A string containing the pieceToCharTable
        """
        pieces = self.getVariantMen()

        charTable = ["."] * (22 * 2)

        usedIndicies = set()

        # For each piece, assign it a WinBoard icon.
        for char, piece in pieces.items():
            piece_added = False
            for i in piece.preferredIconIndexes + list(range(22)):
                # Here we add [0..23] to the list of preferred indexes, so if the one we want isn't availible, we
                # choose the next available one.
                if i not in usedIndicies:
                    usedIndicies.add(i)
                    piece_added = True
                    charTable[i] = char.upper()
                    charTable[i + 22] = char.lower()
                    break
            if not piece_added:
                raise Exception("Match variant has too many pieces to assign WinBoard icons!")

        return "".join(charTable)



class StaticVariants:

    CHESS = Variant("chess",
                    (
                        (Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK),
                        (Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN),
                        (None, None, None, None, None, None, None, None),
                        (None, None, None, None, None, None, None, None),
                        (None, None, None, None, None, None, None, None),
                        (None, None, None, None, None, None, None, None),
                        (Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN),
                        (Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK),
                    ),
                    [Piece.PAWN, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK, Piece.QUEEN, Piece.KING])

    STONK_VARIANT = Variant("stonkchess",
                            (
                                (Piece.ROOK, Piece.CHANCELLOR, Piece.FERZ, Piece.AMAZON, Piece.KING, Piece.BISHOP, Piece.CHANCELLOR, Piece.ROOK),
                                (Piece.ALFIL, Piece.ALFIL, Piece.ALFIL, Piece.ALFIL, Piece.ALFIL, Piece.ALFIL, Piece.ALFIL, Piece.ALFIL),
                                (None, None, None, None, None, None, None, None),
                                (None, None, None, None, None, None, None, None),
                                (None, None, None, None, None, None, None, None),
                                (None, None, None, None, None, None, None, None),
                                (Piece.ALFIL, Piece.ALFIL, Piece.ALFIL, Piece.ALFIL, Piece.ALFIL, Piece.ALFIL, Piece.ALFIL, Piece.ALFIL),
                                (Piece.ROOK, Piece.CHANCELLOR, Piece.FERZ, Piece.AMAZON, Piece.KING, Piece.BISHOP, Piece.CHANCELLOR, Piece.ROOK),
                            ),
                            [Piece.ALFIL, Piece.FERZ, Piece.BISHOP, Piece.CHANCELLOR, Piece.ROOK, Piece.AMAZON, Piece.KING])

