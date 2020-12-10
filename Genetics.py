from typing import Dict, List, Tuple, Optional
import Piece
import random
import MatchRunner
from Variant import Variant
import Evaluator
import time
#from GeneticVariant import GeneticVariant
from GeneticVariant import GeneticVariant
#population setup

def fitness(pop) -> list:
    #run matches
    #rank matches ---- how do we rank matches if they are only win or lose?
    #return match results
    pass

def selectParents(pop: List, matchRank: List, parentCount: int) -> list:
    #return highest parentCount ranked varients
    parents = []
    for i in range(parentCount):
        highestRank = matchRank.index(max(matchRank))
        parents.append(pop[highestRank])
        matchRank[highestRank] = -9999999
    return parents

#mating
def combineBoards(parents, childCount, combineType, king) -> list:
    #combineTypes are halfAndHalf or Folded: combine left half of parent A with right half of parent B or take every other file from parent A then parent B
    #if no king or two are present after combining, average the location of both parents, or randomly pick one.
    #combining pattern, parentA with parentB, parentB with parentC...until childCount is met

    rows = len(parents[0].board)
    crossover_point = len(parents[0].board[0])//2
    #print(rows,crossover_point)
    children = []
    if combineType == "halfAndHalf":
        for i in range(childCount):
            parentAidx = i % len(parents)
            parentBidx = (i+1) % len(parents)
            child = []
            for row in parents[parentAidx].board:
                child.append(row.copy())
            for row in range(rows):
                child[row][crossover_point:] = parents[parentBidx].board[row][crossover_point:]

            #check that there is just one king
            checkKingPlacement([parents[parentAidx].board,parents[parentBidx].board], child, (0,3), crossover_point, king)
            checkKingPlacement([parents[parentAidx].board, parents[parentBidx].board], child, (4, 7), crossover_point, king)

            children.append([child, [parents[parentAidx].ID,parents[parentBidx].ID]])

            #printTest(convertToTuple(child))
    elif combineType == "folded":
        pass
    return children
def checkKingPlacement(parents, child, ranks, crossover_point, king):
    kingA = findKing(parents[0], king, ranks)
    kingB = findKing(parents[1], king, ranks)
    #print(kingA[1], kingB[1])
    if kingA[1] >= crossover_point and kingB[1] < crossover_point:
        if random.randint(0, 1) == 0:
            child[kingA[0]][kingA[1]] = king
        else:
            child[kingB[0]][kingB[1]] = king
        #print("king added")
    elif kingB[1] >= crossover_point > kingA[1]:
        if random.randint(0, 1) == 0:
            child[kingB[0]][kingB[1]] = parents[0][kingB[0]][kingB[1]]
        else:
            child[kingA[0]][kingA[1]] = parents[1][kingA[0]][kingA[1]]
        #print("king removed")
#mutations
def mutatePieces(children, changeCount, pieces, king) -> list:
    #randomly select piece to change to a random piece
    #repeat for changeCount
    for child in children:
        remaingMutants = changeCount
        while(remaingMutants > 0):
            kingLoc = findKing(child[0], king, (0,3))
            randPos = getRandomLoc(0,3,0,7)

            currentPiece = child[0][randPos[0]][randPos[1]]
            if currentPiece != None and currentPiece != king:
                child[0][randPos[0]][randPos[1]] = getRandomPiece(pieces, [king])
                remaingMutants -= 1
        remaingMutants = changeCount
        while (remaingMutants > 0):
            kingLoc = findKing(child[0], king, (4,7))
            randPos = getRandomLoc(4, 7, 0, 7)
            currentPiece = child[0][randPos[0]][randPos[1]]
            if currentPiece != None and currentPiece != king:
                child[0][randPos[0]][randPos[1]] = getRandomPiece(pieces, [king])
                remaingMutants -= 1

    return children
    pass

def shufflePieces(children, shuffleCount, king) -> list:
    #flip(fileRange)
    #exchange((file,rank),(file,rank))
    #random(randomCount)
    #Ensure King remains in back rank


    #childList = convertToList(child)
    newChildren = []
    for childList in children:
        random.randint(0, 1)
        remainingShuffles = shuffleCount
        logBlack = ""
        logWhite = ""
        while remainingShuffles > 0:

            #do a random shuffle for the bottom side(row 0 and 1)
            while True:
                randRow1 = random.randint(0, 1)
                randCol1 = random.randint(0, 7)
                piece1 = childList[0][randRow1][randCol1]

                randRow2 = random.randint(0, 1)
                randCol2 = random.randint(0, 7)
                piece2 = childList[0][randRow2][randCol2]

                #print(len(children),remainingShuffles,piece1, piece2)

                if piece1 == piece2:
                    #swapping the same piece won't change anything
                    #try again and pick two different pieces
                    continue

                if piece1 == king or piece2 == king:
                    if (randRow1 == 0 or randRow2 == 0):
                        #dont swap because the king will be in front
                        #try again and pick two different pieces
                        continue

                #when no problems with king swap then break
                childList[0][randRow1][randCol1] = piece2
                childList[0][randRow2][randCol2] = piece1

                logBlack = logBlack + "black side swapped " + piece2.name + " with " + piece1.name + "\n"
                break

            #do a random shuffle for the bottom side(row 6 and 7)
            while True:
                randRow1 = random.randint(0, 1) + 6
                randCol1 = random.randint(0, 7)
                piece1 = childList[0][randRow1][randCol1]

                randRow2 = random.randint(0, 1) + 6
                randCol2 = random.randint(0, 7)
                piece2 = childList[0][randRow2][randCol2]
                if piece1 == piece2:
                    #swapping the same piece won't change anything
                    #try again and pick two different pieces
                    continue
                if piece1 == king or piece2 == king:
                    if (randRow1 == 6 or randRow2 == 6):
                        # dont swap because the king will be in front
                        #try again and pick two different pieces
                        continue

                # when no problems with king swap then break
                childList[0][randRow1][randCol1] = piece2
                childList[0][randRow2][randCol2] = piece1

                logWhite = logWhite + "white side swapped " + piece2.name + " with " + piece1.name + "\n"
                break

            remainingShuffles = remainingShuffles - 1

        #print(logBlack)
        #print(logWhite)
        #childTuple = convertToTuple(childList)
        newChildren.append(childList)
    return newChildren

def getRandomLoc(rankMin, rankMax, fileMin, fileMax):
    rank = random.randint(rankMin, rankMax)
    file = random.randint(fileMin, fileMax)
    return (rank, file)

def getRandomPiece(pieces, excludedPieces):
    piece = random.choice(pieces)
    while piece in excludedPieces:
        piece = random.choice(pieces)
    return piece



def findKing(board: List[List], king, ranks) -> tuple:
    for i in range(ranks[0], ranks[1]+1):
        for j in range(len(board[0])):
            if board[i][j] == king:
                return (i,j)
    return (-1,-1)

def convertToList(pieceTuple: Tuple[Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]], Tuple[Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece], Optional[Piece.Piece]]]) -> List[List]:
    #convert the pieceTuple to a list of lists
    rowList = []
    boardList = []
    for row in pieceTuple:
        rowList = list(row)
        boardList.append(rowList)
    return boardList

def convertToTuple(pieceList: List[List]) -> Tuple[Tuple]:
    boardTuple: Tuple[Tuple]
    boardTuple = tuple(pieceList)
    return boardTuple


def printTest(pieceTuple): #formats and prints the test board
    for row in pieceTuple:
        for piece in row:
             if piece == None:
                 print("none", end=" "),
             else:
                print(piece.name, end=" "),
        print("")

def getRandomBoard(size, pieces, whiteRanks, blackRanks, king):
    board = []
    for rows in range(size[0]):
        row = []
        for cols in range(size[1]):
            row.append(None)
        board.append(row)
    #printTest(convertToTuple(board))
    for rows in range(whiteRanks[0], whiteRanks[1] + 1):
        for cols in range(size[1]):
            board[rows][cols] = getRandomPiece(pieces, [king])
    for rows in range(blackRanks[0], blackRanks[1] + 1):
        for cols in range(size[1]):
            board[rows][cols] = getRandomPiece(pieces, [king])
    whiteKingLoc = getRandomLoc(0,0,0,size[1]-1)
    blackKingLoc = getRandomLoc(blackRanks[1],blackRanks[1],0,size[1]-1)
    #print(blackKingLoc)
    board[whiteKingLoc[0]][whiteKingLoc[1]] = king
    board[blackKingLoc[0]][blackKingLoc[1]] = king
    return board


def getRandomVariant(name, size, pieces, whiteRanks, blackRanks, king):
    randomBoard = getRandomBoard(size,pieces,whiteRanks,blackRanks,king)
    return  getGeneticVariant(name, randomBoard, 0, None)

def getGeneticVariant(name, board, generation, parents):
    pieceList = []
    for row in range(len(board)):
        for piece in board[row]:
            if piece != None and piece not in pieceList:
                pieceList.append(piece)
                # print(piece.name, piece)
    #printTest(convertToTuple(board))
    # print(len(pieceList), pieceList)
    variant = Variant(name, convertToTuple(board), pieceList)
    return GeneticVariant(name,variant, board,generation,parents)

def createPopulation(popSize, pieces, prefix):
    pop = []
    for i in range(popSize):
        pop.append(getRandomVariant(prefix + "_0_" + str(i), (8,8),pieces,(0,1),(6,7), Piece.KING))
    return pop

def runPopultion(pop, matchCount, depth):
    for variant in pop:
        evaluation = Evaluator.evaluate(evaluateVariant(variant.variant, matchCount, depth))
        #print("Evaluation Added", evaluation)
        variant.addEvaluation(evaluation, depth,matchCount)

    return pop

def runGenetic(popSize, pieces, prefix, matchCount, depth, epoch):
    childCount = popSize // 2 #* 2 // 3
    parentCount = popSize - childCount
    popVariants = createPopulation(popSize, pieces,prefix)
    parents = []
    generations = []
    #run for number of epochs
    for generationIndex in range(epoch):
        generations += popVariants
        runPopultion(popVariants,matchCount,depth)
        pop = []
        ranking = []
        #pull out boards and ranking for child generation
        for variant in popVariants:
            pop.append(variant)
            ranking.append(variant.getScore())

        #add parents from previous generation to the current population for ranking evaluation
        for parent in parents:
            pop.append(parent)
            ranking.append(parent.getScore())

        parents = selectParents(pop, ranking, parentCount)
        children = combineBoards(parents, childCount, "halfAndHalf", Piece.KING)
        #print(children, childCount)
        children = shufflePieces(children, 5, Piece.KING)
        children = mutatePieces(children,5,pieces,Piece.KING)
        #pop = parents + children
        pop = children.copy()
        popVariants = []
        variantIndex = 0
        for board in pop:
            popVariants.append(getGeneticVariant(prefix + "_" + str(generationIndex+1) + "_" + str(variantIndex),board[0],generationIndex,board[1]))
            variantIndex += 1
    with open(prefix + ".csv", "w") as file:

        for variant in generations:
            print(variant)
            file.write(str(variant))
            file.write("\n")


def evaluateVariant(variant: Variant, matchCount, depth) -> MatchRunner.MatchData:
    print("Evaluating {0}.".format(variant.name))
    runner = MatchRunner.MatchRunner(depth= depth)

    matchData = runner.runMatches(variant, matchCount, debug=False)

    print("W/B/D: {0}-{1}-{2}".format(matchData.whiteWins, matchData.blackWins, matchData.draws))
    print("Evaluation: {0}".format(Evaluator.evaluate(matchData)))
    matchData.dumpPGN("{0}".format(variant.name))
    matchData.dumpMCT("{0}-MCT".format(variant.name))

    return(matchData)



