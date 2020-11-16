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
def mutatePieces(children, changeCount, pieces) -> list:
    #randomly select piece to change to a random piece
    #repeat for changeCount
    pass

def shufflePieces(children, shuffleCount) -> list:
    #flip(fileRange)
    #exchange((file,rank),(file,rank))
    #random(randomCount)
    #Ensure King remains in back rank
    pass
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

def convertToTuple(pieceList) -> Tuple[Tuple]:
    boardTuple: Tuple[Tuple]
    boardTuple = tuple(tuple(l) for l in pieceList)
    return boardTuple

# A = [6,7,8,3]
# print(max(A))
# print(A[0:2], A[2:])

parents = [[[1,2,3,"k"],[5,6,7,8]], [["k",10,11,12],[13,14,15,16]]]
print(parents)
children = combineBoards(parents,2, "halfAndHalf", "k")
print(findKing(parents[0], "k"))

print(children)
print(parents)
print(random.randint(0,1))