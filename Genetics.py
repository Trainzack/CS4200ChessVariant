from typing import Dict, List, Tuple, Optional
import Piece
import random
import MatchRunner
#population setup
def fitness(pop) -> list:
    #run matches
    #rank matches ---- how do we rank matches if they are only win or lose?
    #return match results
    pass

def selectParents(pop: List[List[List]], matchRank: List, parentCount: int) -> list:
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
    rows = len(parents[0])
    crossover_point = len(parents[0][0])//2
    #print(rows,crossover_point)
    children = []
    if combineType == "halfAndHalf":
        for i in range(childCount):
            parentAidx = i % len(parents)
            parentBidx = (i+1) % len(parents)
            child = []
            for row in parents[parentAidx]:
                child.append(row.copy())
            for row in range(rows):
                child[row][crossover_point:] = parents[parentBidx][row][crossover_point:]

            #check that there is just one king
            kingA = findKing(parents[parentAidx], king)
            kingB = findKing(parents[parentBidx], king)
            print(kingA[1], kingB[1])
            if kingA[1] >= crossover_point and kingB[1] < crossover_point:
                if random.randint(0,1) == 0:
                    child[kingA[0]][kingA[1]] = king
                else:
                    child[kingB[0]][kingB[1]] = king
                print("king added")
            elif kingB[1] >= crossover_point > kingA[1]:
                if random.randint(0, 1) == 0:
                    child[kingB[0]][kingB[1]] = parents[parentAidx][kingB[0]][kingB[1]]
                else:
                    child[kingA[0]][kingA[1]] = parents[parentBidx][kingA[0]][kingA[1]]
                print("king removed")

            children.append(child)
    elif combineType == "folded":
        pass
    return children

#mutations
def mutatePieces(children, changeCount, pieces, king) -> list:
    #randomly select piece to change to a random piece
    #repeat for changeCount
    for child in children:
        remaingMutants = changeCount
        while(remaingMutants > 0):
            kingLoc = findKing(child, king)
            randPos = getRandomLoc(0,3,0,7)

            currentPiece = child[randPos[0]][randPos[1]]
            if currentPiece != None and currentPiece != king:
                child[randPos[0]][randPos[1]] = getRandomPiece(pieces, [king])
                remaingMutants -= 1
        remaingMutants = changeCount
        while (remaingMutants > 0):
            kingLoc = findKing(child, king)
            randPos = getRandomLoc(4, 7, 0, 7)
            currentPiece = child[randPos[0]][randPos[1]]
            if currentPiece != None and currentPiece != king:
                child[randPos[0]][randPos[1]] = getRandomPiece(pieces, [king])
                remaingMutants -= 1

    return children
    pass

def shufflePieces(children, shuffleCount) -> list:
    #flip(fileRange)
    #exchange((file,rank),(file,rank))
    #random(randomCount)
    #Ensure King remains in back rank
<<<<<<< Updated upstream
    pass
=======

    childList = convertToList(child)
    random.randint(0, 1)
    remainingShuffles = shuffleCount
    logBlack = ""
    logWhite = ""
    while remainingShuffles > 0:

        #do a random shuffle for the bottom side(row 0 and 1)
        while True:
            randRow1 = random.randint(0, 1)
            randCol1 = random.randint(0, 7)
            piece1 = childList[randRow1][randCol1]

            randRow2 = random.randint(0, 1)
            randCol2 = random.randint(0, 7)
            piece2 = childList[randRow2][randCol2]

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
            childList[randRow1][randCol1] = piece2
            childList[randRow2][randCol2] = piece1

            logBlack = logBlack + "black side swapped " + piece2.name + " with " + piece1.name + "\n"
            break

        #do a random shuffle for the bottom side(row 6 and 7)
        while True:
            randRow1 = random.randint(0, 1) + 6
            randCol1 = random.randint(0, 7)
            piece1 = childList[randRow1][randCol1]

            randRow2 = random.randint(0, 1) + 6
            randCol2 = random.randint(0, 7)
            piece2 = childList[randRow2][randCol2]
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
            childList[randRow1][randCol1] = piece2
            childList[randRow2][randCol2] = piece1

            logWhite = logWhite + "white side swapped " + piece2.name + " with " + piece1.name + "\n"
            break

        remainingShuffles = remainingShuffles - 1

    #print(logBlack)
    #print(logWhite)
    childTuple = convertToTuple(childList)
    return childTuple

def getRandomLoc(rankMin, rankMax, fileMin, fileMax):
    rank = random.randint(rankMin, rankMax)
    file = random.randint(fileMin, fileMax)
    return (rank, file)

def getRandomPiece(pieces, excludedPieces):
    piece = random.choice(pieces)
    while piece in excludedPieces:
        piece = random.choice(pieces)
    return piece


>>>>>>> Stashed changes
def findKing(board: List[List], king) -> tuple:
    for i in range(len(board)):
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

<<<<<<< Updated upstream
=======
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
    printTest(convertToTuple(board))
    for rows in range(whiteRanks[0], whiteRanks[1] + 1):
        for cols in range(size[1]):
            board[rows][cols] = getRandomPiece(pieces, [king])
    for rows in range(blackRanks[0], blackRanks[1] + 1):
        for cols in range(size[1]):
            board[rows][cols] = getRandomPiece(pieces, [king])
    whiteKingLoc = getRandomLoc(0,0,0,size[1])
    blackKingLoc = getRandomLoc(blackRanks[1],blackRanks[1],0,size[1])
    print(blackKingLoc)
    board[whiteKingLoc[0]][whiteKingLoc[1]] = king
    board[blackKingLoc[0]][blackKingLoc[1]] = king
    return board
>>>>>>> Stashed changes
# A = [6,7,8,3]
# print(max(A))
# print(A[0:2], A[2:])

parents = [[[1,2,3,"k"],[5,6,7,8]], [["k",10,11,12],[13,14,15,16]]]
print(parents)
children = combineBoards(parents,2, "halfAndHalf", "k")
print(findKing(parents[0], "k"))

<<<<<<< Updated upstream
print(children)
print(parents)
print(random.randint(0,1))
=======
#standard board for testing
shuffleTest = (Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK),(Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN),(None, None, None, None, None, None, None, None),(None, None, None, None, None, None, None, None),(None, None, None, None, None, None, None, None),(None, None, None, None, None, None, None, None),(Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN, Piece.PAWN),(Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK)
printTest(shuffleTest)
print("")
#printTest(shufflePieces(shuffleTest, 50, Piece.KING))
mutateTest = [convertToList(shuffleTest)]

mutatePieces(mutateTest, 5, Piece.Piece.pieces, Piece.KING)
mutateTest[0][5][5] = Piece.KING
printTest(mutateTest[0])

randBoard = getRandomBoard((8,8),Piece.Piece.pieces,(0,1),(6,7), Piece.KING)
printTest(convertToTuple(randBoard))
>>>>>>> Stashed changes
