
#population setup
def fitness(matchResults, pop) -> list:
    #run matches
    #rank matches ---- how do we rank matches if they are only win or lose?
    #return match results
    pass

def selectParents(pop, matchRank, parentCount) -> list:
    #return highest ranked varients up to parentcount
    pass

#mating
def combineBoards(parents, childCount, combineType) -> list:
    #combineTypes are halfAndHalf or Folded: combine left half of parent A with right half of parent B or take every other file from parent A then parent B
    #if no king or two are present after combining, average the location of both parents, or randomly pick one.
    #combining pattern, parentA with parentB, parentB with parentC...until childCount is met
    pass

#mutations
def mutatePieces(children, changeCount) -> list:
    #randomly select piece to change to a random piece
    #repeat for changeCount
    pass

def shufflePieces(children) -> list:
    #flip(fileRange)
    #exchange((file,rank),(file,rank))
    #random(randomCount)
    pass