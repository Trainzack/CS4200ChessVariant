import Piece
import Variant
import Engine
import Match
import MatchRunner
import LatexExport
import Evaluator

stalemateChessMoves = ["h2h4", "e7e5", "h1h3", "d8h4", "a2a4", "h4g4", "h3a3", "g4g2", "c2c3", "g2g1", "d1b3", "g1f2", "e1d1", "f2f1", "d1c2", "f1e2", "b3a2", "a7a5", "c2b3", "e2d3"]
whitwWinChessMoves = ["e2e4", "f7f6", "d2d3", "g7g5", "d1h5"]
blackWinChessMoves = ["f2f3", "e7e5", "g2g4", "d8h4"]

def testEngine():

    results = dict()
    for v in Variant.StaticVariants.BUILTINS:
        results[v] = evaluateVariant(v)

    for v, d in results.items():
        print("Variant {0} results: ".format(v.name))
        print("\tW/B/D: {0}-{1}-{2}".format(d.whiteWins, d.blackWins, d.draws))
        print("\tEvaluation: {0}".format(Evaluator.evaluate(d)))





def evaluateVariant(variant: Variant) -> MatchRunner.MatchData:
    print("Evaluating {0}.".format(variant.name))
    runner = MatchRunner.MatchRunner(depth=10)

    matchData = runner.runMatches(variant, 100, debug=False)

    print("W/B/D: {0}-{1}-{2}".format(matchData.whiteWins, matchData.blackWins, matchData.draws))
    print("Evaluation: {0}".format(Evaluator.evaluate(matchData)))
    matchData.dumpPGN("{0}".format(variant.name))
    matchData.dumpMCT("{0}-MCT".format(variant.name))

    return(matchData)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testEngine()

