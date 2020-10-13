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
        return "[variant:chess]\n startFen = " + self.getStartingFEN()
