import math
from typing import Optional, Tuple, List, Dict

import pyffish

import Variant


class MonteCarloTreeNode(object):
    # TODO: Can the root node be it's own __init__, to make all params used in each?
    def __init__(self, variant:Variant, move:str, root, parent=None):
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

        # All of the moves leading up to here, including this node's move
        self.previous_moves: List[str] = []

        if root is None:
            self.root: MonteCarloTreeNode = self
            self.is_root = True
        else:
            self.root: MonteCarloTreeNode = root
            self.previous_moves = parent.previous_moves.copy()
            self.previous_moves.append(move)


        self.parent: Optional[MonteCarloTreeNode] = parent
        self.children: Dict = {}

        # The number of games this node has been a part of
        self.number_visits: int = 0

        # The number of wins + 1/2 of the number of draws of the player that played this move in all games it's been in
        self.total_value: int = 0

    def expand(self):
        """
        This function creates new MCT nodes as the children of this node.
        :return:
        """
        if self.is_expanded:
            raise Exception("Can't expand already expanded MCTS node")
        else:
            self.is_expanded = True
            legal_moves = pyffish.legal_moves(self.variant.name, self.variant.startingFEN, self.previous_moves)
            for move in legal_moves:
                self.children[move] = MonteCarloTreeNode(self.variant, move, self.root, self)

    def markNode(self, win:bool, draw:bool):
        """
        Mark the result of this node, and all parent nodes.
        You should only need to call this once per match.
        Take care that you get win correct depending on the team that did this node.
        :param win: True if this node was a win, false if loss or draw
        :param draw: True if this node was a draw, false if win or loss
        :return:
        """
        self.number_visits += 1
        if win:
            self.total_value += 1
        elif draw:
            self.total_value += 0.5

        if not self.is_root:
            self.parent.markNode(not win if not draw else False, draw) # Alternate wins and lossses up the tree, otherwise

    def selectionFunction(self, explorationParameter:float=1.41421356237) -> float:
        """
        Use this function to compare multiple children to select the best one during MCTS.
        Not valid for the root node.
        :param explorationParameter: The weight associated with exploration. Higher numbers mean exploration is weighted more heavily.
        :return: A value representing how good this node is to chose based on exploration and exploitation.
        """
        if self.is_root:
            raise Exception("You cannot (and should not) use the selection function on the root node of a MCT.")
        exploit = self.total_value / (self.number_visits + 1)
        explore = math.sqrt(math.log(self.parent.number_visits + 1) / (self.number_visits + 1))

        return exploit + explorationParameter * explore

    def selectBestChild(self) -> Tuple:
        """
        Select the current best child for us to go down when exploring the MCTS tree.
        :return: A tuple containing two values:
        1) A boolean that is True when the node returned should no longer be explored with MCTS,
         and instead explored with stockfish.
        2) The next node to explore.
        """
        finish: bool = False

        if not self.is_expanded:
            self.expand()
            finish = True


        bestChild: MonteCarloTreeNode = max(self.children.values(), key=lambda child: child.selectionFunction())

        return finish, bestChild

    def __str__(self):
        if self.is_root:
            return "MCTS Root. Value {0}/{1}".format(self.total_value, self.number_visits)
        else:
            return "MCTS Node. Value {0}/{1}. Move {2} After {3}.".format(self.total_value, self.number_visits, self.move, self.previous_moves)


def testMCT():
    """Tests the MCT, to ensure that we coded it correctly."""

    variant = Variant.StaticVariants.CHESS

    root = MonteCarloTreeNode(variant, "", None, None)


    for i in range(200):
        print('Test game {0}.'.format(i+1))
        print(root)
        stop = False
        curNode = root
        while not stop:
            stop, curNode = curNode.selectBestChild()
            print(curNode)


        draw = i % 5 == 0
        win = i % 2 == 0 and not draw
        print("Faking game result: {0}".format("win" if win else ("draw" if draw else 'loss')))
        curNode.markNode(win, draw)

if __name__ == '__main__':
    testMCT()