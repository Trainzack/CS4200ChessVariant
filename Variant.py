# This class represents a chess variant.
# This is what the genetic algroithm will develop



class Variant:
    """Represents a variant of the game chess."""



    def getStartingFEN(self) -> str:
        """Returns the starting FEN"""
        # TODO
        return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def getFairyStockfishINI(self) -> str:
        """Returns the fairystockfish ini file that defines this variant"""
        # TODO
        return "[variant:{0}]\n startFen = {1}".format(self.getVariantName(), self.getStartingFEN())

    def getVariantName(self) -> str:
        """Returns the name of this variant, as in its variant.ini file"""
        return "chess"

    def getVariantMen(self) -> dict:
        """Returns a dict of the following format:

            Key: A str containing the letter of the piece
            Value: A str containing the betza notation of the piece

        For each piece.
        """
        return {
            "P": "fmWfceF",
            "B": "B",
            "N": "N",
            "R": "R",
            "Q": "Q",
            "K": "K",
        }

class ChessVariant(Variant):
    """This variant is literally just chess."""