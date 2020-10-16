#  Loosely based off of pystockfish

from Engine import Engine
from Variant import Variant
import socket
from datetime import date
import pyffish
import random

class Match:
    """
    This class represents one single match.
    """
    def __init__(self, variant:Variant):
        self.moves = []
        self.site = socket.gethostname()
        self.match_date=date.today()
        self.variant = variant
        # Valid values for result:
        #    "1-0" (White wins)
        #    "0-1" (Black wins)
        #    "1/2-1/2" (Drawn game)
        #    "*" (game still in progress, game abandoned, or result otherwise unknown)
        self.result = "*"

    def __str__(self):
        return "{0} Match. {1} turns, result: {2}".format(self.variant.getVariantName(), len(self.moves), self.result)

    def markWhiteVictory(self):
        self.result = "1-0"

    def markBlackVictory(self):
        self.result = "0-1"

    def markDraw(self):
        self.result = "1/2-1/2"

    def getPGN(self) -> str:
        output = "[Event \"Computer Match, Variant: {0}\"]\n".format(self.variant.getVariantName())
        output += "[Site \"{0}\"]\n".format(self.site)
        output += "[Date \"{0}\"]\n".format(self.match_date)
        output += "[WhiteType \"program\"]\n[BlackType \"program\"]\n"
        output += "[PlyCount \"{0}\"]\n".format(len(self.moves))
        output += "[Result \"{0}\"]\n".format(self.result)
        output += "[Variant \"{0}\"]\n".format(self.variant.getVariantName())

        # We need to get the list of variant pieces for winboard or other viewers to understand.
        variantMenString = ""
        for p, b in self.variant.getVariantMen().items():
            variantMenString += "{0}:{1};".format(p,b)
        variantMenString = variantMenString[0:-1] # Strip the last semicolon

        output += "[VarientMen \"{0}\"]\n".format(variantMenString) # As WinBoard seems to support
        output += "[FEN \"{0}\"]\n".format(self.variant.getStartingFEN())
        output += "[SetUp \"1\"]"

        # Finally, we need to get the list of moves.

        output += "\n"
        for i, move in enumerate(self.moves):
            if i % 2 == 0:
                output += "{0}. ".format((i // 2) + 1)
            output += "{0} ".format(move)
        output += self.result
        return output

class MatchData:
    """
    This class contains all the data we get from running matches, ready to be analyzed by an evaluator
    """
    def __init__(self):
        self.matches = list()
        """A list of all the matches done, which are tuples of moves."""

    def dumpPGN(self, fileName:str):
        """
        Dumps all of the matches contained in this matchdata object to one PGN file.
        :param fileName: The name of the file, without extension (this will create a .pgn file)
        :return:None
        """

        with open(fileName + ".pgn", "w") as file:
            for match in self.matches:
                file.write(match.getPGN())
                file.write("\n\n")

class MatchRunner:
    """
    This class runs matches between engines, and records the data in a MatchData class
    """

    def __init__(self, depth=2):
        """

        :param depth: The depth of the engine
        """

        self.whiteEngine: Engine = Engine(depth=depth)
        self.blackEngine: Engine = Engine(depth=depth)
        self.engines = (self.whiteEngine, self.blackEngine)

    def runMatches(self, variant:Variant, matchCount=100, debug=False, variantPath:str="") -> MatchData:
        """

        :param variant: The variant we want to run matches of.
        :param matchCount: The number of matches to run
        :param debug: If true, print debug statements
        :param variantPath: A path to the .ini file that contains the variant. If none is provided, one will be created.
        :return:
        """


        matchData = MatchData()

        if variantPath == "":
            variantPath = "variant-{0}.ini".format(variant.getVariantName())
            with open(variantPath, "w") as ini:
                ini.write(variant.getFairyStockfishINI())

        pyffish.set_option("VariantPath", variantPath)

        for e in self.engines:
            # Set the engines to the variant we are running.
            e.setVariant(variant, variantPath)

        for matchNo in range(matchCount):


            match = Match(variant)

            for e in self.engines:
                e.newgame()

            # Go through a MCTS opening
            for i in range(2):
                legal_moves = pyffish.legal_moves(variant.getVariantName(), variant.getStartingFEN(), match.moves)
                if len(legal_moves) == 0:
                    # Checkmate!
                    # TODO: this needs to be replaced with calls to pyffish
                    if i % 2 == 0:
                        match.markBlackVictory()
                    else:
                        match.markWhiteVictory()
                    break

                move = legal_moves[random.randint(0,len(legal_moves)-1)]
                # TODO: Apply MCTS algorithm
                match.moves.append(move)


            # This is the loop that goes through the moves in any individual game
            while True:
                # Don't let too many moves happen!
                if len(match.moves) >= 200:
                    match.markDraw()
                    break

                active_engine = self.engines[len(match.moves)%2]
                inactive_engine = self.engines[(len(match.moves)+1)%2]

                active_engine.setposition(match.moves)
                moveDict = active_engine.bestmove()
                bestMove: str = moveDict["move"]
                ponder: str = moveDict["ponder"]
                info: str = moveDict["info"]
                match.moves.append(bestMove)

                if debug:
                    print("{0}, move {1}, info {2}".format(len(match.moves), bestMove, info))

                # If the engine found mate, then we can stop running through the steps.
                # TODO: This needs to be replaced with calls to pyffish.
                if 'mate' in moveDict.keys():
                    mateNum:int = moveDict['mate']
                    if mateNum in (1, 0):
                        # Somebody has checkmate, so find out who is the winner
                        if mateNum > 0:
                            winning = active_engine
                        else:
                            winning = inactive_engine

                        if winning == self.whiteEngine:
                            match.markWhiteVictory()
                        else:
                            match.markBlackVictory()
                        break
                # Add the matches we just played to the match data.
            matchData.matches.append(match)
            print(match)
        return matchData