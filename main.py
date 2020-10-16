from Engine import Engine
from Variant import *
from MatchRunner import *

def testEngine():

    runner = MatchRunner()

    matchData = runner.runMatches(ArchBishopVariant(), 2, debug=True)

    for match in matchData.matches:
        print(match)

    matchData.dumpPGN("test")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testEngine()

