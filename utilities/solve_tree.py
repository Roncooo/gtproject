from utilities.Node import Node
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


def solve(current_node: Node, generate_tree_function, depths: List[int]=None):
    '''
    Solves the game using minimax policy starting from ```current_node```. 
    
    When the tree is very big (and in particular very deep), one could want to subdivide the solution of the tree in some steps. You can do this by specifying the size of each step in the list ```depths```. In that case the algorithm will solve the subtree of depth ```depths[0]```, take the leaf returned by the minimax and use it as new root and reiterate until the depths are ended. As discussed in the paper, this may have little sense but we still allow it, also for debugging purposes. In particular, just as a practical suggestion, if the number of cards is bigger than 12, the execution of the minimax algorithm on the full tree without intermediate steps becomes very long. 
    
    Returns the path from ```current_node``` to the best leaf as a list of nodes.'''

    assert len(current_node.cards_player1)==len(current_node.cards_player2), f"The two players should have the same amount of cards but player 1 has {len(current_node.cards_player1)} cards and player 2 has {len(current_node.cards_player2)}"
    
    actual_number_of_cards = len(current_node.cards_player1) + len(current_node.cards_player2)
    if depths==None:
        depths = [actual_number_of_cards]
    
    assert sum(depths)==actual_number_of_cards, f"The sum of depths is {sum(depths)} but it must be equal to {actual_number_of_cards}"

    full_path = []
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
        full_path.append(path)

        end = time.time()
        print(f"Done {depth} levels in {end - start:.2f} s")

    return full_path


