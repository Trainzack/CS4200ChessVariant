import socket
from datetime import date

import pyffish

import Variant


class Match:
    """
    This class represents one single match.
    """
    def __init__(self, variant:Variant, round:int):
        self.moves = []
        self.FEN = [variant.getStartingFEN()]
        self.site = socket.gethostname()
        self.match_date=date.today()
        self.variant = variant
        self.round = round
        # Valid values for result:
        #    "1-0" (White wins)
        #    "0-1" (Black wins)
        #    "1/2-1/2" (Drawn game)
        #    "*" (game still in progress, game abandoned, or result otherwise unknown)
        self.result = "*"

    def __str__(self):
        return "{0} Match. {1} turns, result: {2}".format(self.variant.name, len(self.moves), self.result)

    def addMove(self, move:str):
        self.FEN.append(pyffish.get_fen(self.variant.name, self.FEN[-1], [move]))
        self.moves.append(move)


    def markWhiteVictory(self):
        self.result = "1-0"

    def markBlackVictory(self):
        self.result = "0-1"

    def markDraw(self):
        self.result = "1/2-1/2"

    def getPGN(self) -> str:
        output = "[Event \"Computer Match, Variant: {0}\"]\n".format(self.variant.name)
        output += "[Site \"{0}\"]\n".format(self.site)
        output += "[Date \"{0}\"]\n".format(self.match_date)
        output += "[Round \"{0}\"]\n".format(self.round)
        output += "[WhiteType \"program\"]\n[BlackType \"program\"]\n"
        output += "[PlyCount \"{0}\"]\n".format(len(self.moves))
        output += "[Result \"{0}\"]\n".format(self.result)
        output += "[Variant \"{0}\"]\n".format(self.variant.name)

        # I think the following tags are non-standard!

        # We need to get the list of variant pieces for winboard or other viewers to understand.
        # variantMenString = ""
        # for char, piece in self.variant.getVariantMen().items():
        #     variantMenString += "{0}:{1};".format(char, piece.betza)
        # variantMenString = variantMenString[0:-1] # Strip the last semicolon

        # output += "[VarientMen \"{0}\"]\n".format(variantMenString) # As WinBoard seems to support
        # output += "[pieceToCharTable \"{0}\"]\n".format(self.variant.getPieceToCharTable())
        output += "[FEN \"{0}\"]\n".format(self.variant.getStartingFEN())
        # output += "[SetUp \"1\"]"

        # Finally, we need to get the list of moves.

        output += "\n"
        for i, move in enumerate(self.moves):
            if i % 2 == 0:
                output += "{0}. ".format((i // 2) + 1)
            output += "{0} ".format(move)
        output += self.result
        return output