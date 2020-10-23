from Engine import Engine
from Variant import *
from MatchRunner import *


class Genetic:
    def __init__(self):
        print("hello")

    def geneticAlgorithm(self, parentsList, matchCount=10, generations=15):

        for generation in range(generations):

            #scores[] resets every generation

            for parent in parentsList:
                #runMatch(parent, depth = matchCount)

            #endfor

            #take parents with highest score
            #somehow mutate or cross over these parents to create new Variant objects

            #reset and re-populate parentsList with new Variants for next generation

        #endfor
