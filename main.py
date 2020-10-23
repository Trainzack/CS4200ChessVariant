import Piece
import Variant
import Engine
import Match
import MatchRunner
import LatexExport

def testEngine():

    for piece in Piece.Piece.pieces:
        print(LatexExport.getPieceDefinition(piece, piece.preferredChar))

    runner = MatchRunner.MatchRunner(depth=3)

    matchData = runner.runMatches(Variant.StaticVariants.STONK_VARIANT, 1, debug=False)
    print(LatexExport.getMatchLatex(matchData.matches[0]))

    matchData.dumpPGN("test")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testEngine()

