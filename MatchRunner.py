#  Loosely based off of pystockfish

from Engine import Engine
from Variant import Variant
from Match import Match

import pyffish
import random


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

    def runMatches(self, variant: Variant, matchCount=100, debug=False, variantPath: str="") -> MatchData:
        """

        :param variant: The variant we want to run matches of.
        :param matchCount: The number of matches to run
        :param debug: If true, print debug statements
        :param variantPath: A path to the .ini file that contains the variant. If none is provided, one will be created.
        :return:
        """

        matchData = MatchData()

        if variantPath == "":
            variantPath = "variant-{0}.ini".format(variant.name)
            with open(variantPath, "w") as ini:
                ini.write(variant.getFairyStockfishINI())

        pyffish.set_option("VariantPath", variantPath)

        for e in self.engines:
            # Set the engines to the variant we are running.
            e.setVariant(variant, variantPath)

        for matchNo in range(matchCount):


            match = Match(variant, (matchNo + 1))

            for e in self.engines:
                e.newgame()

            # Go through a MCTS opening
            for i in range(2):
                legal_moves = pyffish.legal_moves(variant.name, variant.getStartingFEN(), match.moves)
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
                match.addMove(move)


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
                match.addMove(bestMove)

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