from utilities.Node import Node
from utilities.utils import NUMBER_OF_CARDS
from typing import List
import time

def minimax(position: Node, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('+inf')):
    '''Executes the minimax (recursive) algorithm with alpha-beta pruning on the tree for ```depth``` levels starting from ```position```. Returns the best value and the best leaf, which, according to the type of the current player (maximizing or minimizing player) is the one with the highest or lowest value.'''
        
    if depth == 0 or not position.children:  # Check for leaf node or game over
        return position.delta_score, position

    if maximizingPlayer:
        maxEval = float('-inf')
        bestLeaf = None
        for child in position.children:
            eval, leaf = minimax(child, depth - 1, False, alpha, beta)
            if eval > maxEval:
                maxEval = eval
                bestLeaf = leaf
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, bestLeaf

    else:
        minEval = float('+inf')
        bestLeaf = None
        for child in position.children:
            eval, leaf = minimax(child, depth - 1, True, alpha, beta)
            if eval < minEval:
                minEval = eval
                bestLeaf = leaf
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, bestLeaf


def solve(current_node: Node, depths: List[int], generate_tree_function):
    '''Solves the game using minimax policy iteratively with steps defined by ```depths```. Returns the path from ```current_node``` to the best leaf as a list of nodes.'''

    assert sum(depths)==NUMBER_OF_CARDS, f"The sum of depths is {sum(depths)} but it must be equal to {NUMBER_OF_CARDS}"

    all_paths = []
    current_player = 1 # According to the rules, player 1 starts

    for i, depth in enumerate(depths):
        start = time.time()

        # if previous depth is odd, then i need to switch to the other starting player
        if i>0 and depth%2!=0:
            current_player = 2 if current_player==1 else 1
        
        # current player = 1 because we are only using even depths
        root = generate_tree_function(current_node.cards_player1, current_node.cards_player2, current_node.visible_cards, depth, current_player)
        score, leaf_minimax = minimax(root, depth, True)

        current_node = leaf_minimax
        path = Node.get_path(leaf_minimax)
        all_paths.append(path)

        end = time.time()
        print(f"Done {depth} levels in {end - start:.2f} s")

    return all_paths