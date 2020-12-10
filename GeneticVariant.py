from typing import Dict, List, Tuple, Optional
import Variant
#import Genetics

def convertToTuple(pieceList: List[List]) -> Tuple[Tuple]:
    boardTuple: Tuple[Tuple]
    boardTuple = tuple(pieceList)
    return boardTuple

class GeneticVariant:

    evaluations = []
    depths = []
    matchCounts = []

    def __init__(self, ID: str, variant, board, generation, parents: [str, str] = None):
        self.variant = variant
        self.ID = ID
        self.board = board
        self.parents = parents
        self.generation = generation


    def getScore(self):
        # score = self.evaluations[len(self.evaluations) - 1]
        #print("getScore:", self.evaluations)
        return self.evaluations

    def addEvaluation(self, score, depth, matchCount):
        # self.evaluations.append(score)
        # self.depths.append(depth)
        # self.matchCounts.append(matchCount)
        self.evaluations=score
        self.depths=depth
        self.matchCounts=matchCount
    def __str__(self):
        startingFEN = self.variant.startingFEN
        parents = "None"
        if self.parents != None:
            parents = self.parents[0] + "/" + self.parents[1]
        results = self.evaluations
        # for i in range(len(self.evaluations)):
        #     results += "Score: " + str(self.evaluations) + " "
        return "{0} {1} {2} depth: {3} matchCount: {4} results: {5}".format(self.ID,startingFEN, parents, self.depths, self.matchCounts, results)

