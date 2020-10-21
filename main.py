from Engine import Engine
from Variant import *
from MatchRunner import *

def testEngine():

    runner = MatchRunner(depth=3)

    matchData = runner.runMatches(StaticVariants.STONK_VARIANT, 1, debug=False)

    matchData.dumpPGN("test")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testEngine()

