#  Loosely based off of pystockfish

from Engine import Engine
from Variant import Variant
import socket
from datetime import date

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
        output += "[Variant  \"{0}\"]\n".format(self.variant.getVariantName())

        # We need to get the list of variant pieces for winboard or other viewers to understand.
        variantMenString = ""
        for p, b in self.variant.getVariantMen().items():
            variantMenString += "{0}:{1};".format(p,b)
        variantMenString = variantMenString[0:-1] # Strip the last semicolon

        output += "[VarientMen  \"{0}\"]\n".format(variantMenString) # As WinBoard seems to support
        output += "[FEN \"{0}\"]\n".format(self.variant.getStartingFEN())
        output += "[WhiteType \"program\"]\n[BlackType \"program\"]\n"
        output += "[PlyCount \"{0}\"]\n".format(len(self.moves))
        output += "[Result \"{0}\"]\n".format(self.result)

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

    def __init__(self):

        self.whiteEngine = Engine()
        self.blackEngine = Engine(depth=10)
        self.engines = (self.whiteEngine, self.blackEngine)


    def runMatches(self, variant:Variant, matchCount = 100) -> MatchData:

        matchData = MatchData()

        for e in self.engines:
            # Set the engines to the variant we are running.
            e.setVariant(variant)

        for matchNo in range(matchCount):

            match = Match(variant)

            for e in self.engines:
                e.newgame()

            # TODO: add MCTS here

            # This is the loop that goes through the moves in any individual game
            while True:
                # Don't let too many moves happen!
                if len(match.moves) > 200:
                    match.markDraw()
                    break
                elif len(match.moves) % 2:
                    active_engine = self.blackEngine
                    inactive_engine = self.whiteEngine
                else:
                    inactive_engine = self.whiteEngine
                    active_engine = self.blackEngine

                active_engine.setposition(match.moves)
                moveDict = active_engine.bestmove()
                bestMove: str = moveDict["move"]
                ponder: str = moveDict["ponder"]
                info: str = moveDict["info"]
                match.moves.append(bestMove)

                # If the engine found mate, then we can stop running through the steps.
                if 'mate' in moveDict.keys():
                    mateNum:int = moveDict['mate']
                    # Somebody has mate, so find out who is the winner
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
        return matchData