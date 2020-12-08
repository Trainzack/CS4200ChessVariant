import math
import Variant

class MonteCarloTreeNode():
    def __init__(self, variant:Variant, move:str, root:Optional[MonteCarloTreeNode], parent:Optional[MonteCarloTreeNode]=None):
        """
        Represents a single node in the Mote Carlo Tree Search tree.
        :param variant: The variant that this MCTS tree node is exploring
        :param move: The most recent move in the game that this node represents #TODO: We should allow this to be a graph
        :param root: The root of this MCT tree
        :param parent: The MCT node that came before this one.
        """
        self.move = move
        self.variant = variant

        # True if the children of this node have been created, false otherwise.
        self.is_expanded = False

        self.is_root = False

        if root is None:
            self.root = self
            self.is_root = True
        else:
            self.root = root

        self.parent = parent
        self.children = {}

        # The number of games this node has been a part of
        self.number_visits: int = 0

        # The number of wins + 1/2 of the number of draws of the player that played this move in all games it's been in
        self.total_value:int = 0

    def expand(self):
        """
        This function creates new MCT nodes as the children of this node.
        :return:
        """
        if self.is_expanded:
            raise Exception("Can't expand already expanded MCTS node")
        else:
            self.is_expanded = True
            legal_moves = pyffish.legal_moves(variant.name, variant.startingFEN, match.moves)
            for move in legal_moves:
                self.children[move] = MonteCarloTreeNode(self.variant, move, self.root, self)


    def selectionFunction(self, explorationParameter:float=1.41421356237) -> float:
        """
        Use this function to compare multiple children to select the best one during MCTS.
        Not valid for the root node.
        :param explorationParameter: The weight associated with exploration. Higher numbers mean exploration is weighted more heavily.
        :return: A value representing how good this node is to chose based on exploration and exploitation.
        """
        if self.is_root:
            raise Exception("You cannot (and should not) use the selection function on the root node of a MCT.")
        exploit = self.total_value / self.number_visits
        explore = math.sqrt(math.log(self.parent.number_visits) / self.number_visits)

        return exploit + explorationParameter * explore


