from gtproject.Alphabeta_pruning.tree_primi_composti_1 import generate_tree_1
from gtproject.Alphabeta_pruning.tree_primi_composti_2 import generate_tree_2
from gtproject.utilities.Node import Node
from gtproject.utilities.Stack import *
import time


def minimax(position, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or not position.children:  # Check for leaf node or game over
        return position.delta_score, position

    if maximizingPlayer:
        maxEval = float('-inf')
        bestLeaf = None
        for child in position.children:
            eval, leaf = minimax(child, depth - 1, alpha, beta, False)
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
            eval, leaf = minimax(child, depth - 1, alpha, beta, True)
            if eval < minEval:
                minEval = eval
                bestLeaf = leaf
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, bestLeaf


def resolve(current_node, depths):

    all_paths = []

    for depth in depths:
        start = time.time()

        if isinstance(current_node.visible_cards, list) and all(isinstance(x, Stack) for x in current_node.visible_cards):
            root = generate_tree_2(current_node.cards_player1, current_node.cards_player2, current_node.visible_cards,depth)
        else:
            root = generate_tree_1(current_node.cards_player1, current_node.cards_player2, current_node.visible_cards,depth)

        score, leaf_minimax = minimax(root, depth, float('-inf'), float('+inf'), True)

        current_node = leaf_minimax
        path = Node.get_path(leaf_minimax)
        all_paths.append(path)

        end = time.time()
        print(f"Done {depth} levels in {end - start:.2f} s")

    return score, current_node, all_paths