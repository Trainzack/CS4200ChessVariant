# This class represents a chess variant.
# This is what the genetic algroithm will develop
import Piece
from typing import Dict, List


class Variant:
    """Represents a variant of the game chess."""

    def __init__(self, name: str, startingFEN: str, pieces: List[Piece.Piece], iniFlags: List[str]=None):
        """

        :param name: The name of this variant
        :param startingFEN: The FEN of the starting positions
        :param pieces: A list of Pieces that this variant uses
        :param iniFlags: A list of strings that will be put in the INI file for this variant.
        """

        self.name = name
        self.startingFEN = startingFEN
        self.pieces = pieces
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

    def getStartingFEN(self) -> str:
        """
        I'm leaving this in in case we want to construct the starting FEN from tuples or something at a later date.
        :return: The starting FEN position for this variant
        """
        return self.startingFEN

    def getVariantMen(self) -> Dict[str, Piece.Piece]:
        """Returns a dict of the following format:

            Key: A str containing the letter of the piece
            Value: The Piece object containing the piece

        For each piece.
        """
        out = dict()

        for piece in self.pieces:
            out[piece.preferredChar] = piece
            # TODO: This does not check for conflicts!
        return out

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
                    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                    [Piece.PAWN, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK, Piece.QUEEN, Piece.KING])

    STONK_VARIANT = Variant("stonkchess",
                            "rcbzkbcr/aaaaaaaa/1f4f1/8/8/1F4F1/AAAAAAAA/RCBZKBCR w KQkq - 0 1",
                            [Piece.ALFIL, Piece.FERZ, Piece.BISHOP, Piece.CHANCELLOR, Piece.ROOK, Piece.AMAZON, Piece.KING])

