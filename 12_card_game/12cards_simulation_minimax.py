import numpy as np

from Primi_composti_1.tree_primi_composti_1 import generate_tree_1
from utilities.solve_tree import  solve2
from utilities.utils import   LOWEST_CARD
from utilities.Node import Node
from prettytable import PrettyTable
import random

def count_positive_negative_scores(all_leaves):
    '''Calculates the percentage of nodes in all_leaves with positive and negative scores.'''

    positive_count = 0
    negative_count = 0

    # Count positive and negative scores
    for node in all_leaves:
        if node.delta_score > 0:
            positive_count += 1
        elif node.delta_score < 0:
            negative_count += 1

    return positive_count, negative_count


if __name__ == "__main__":

    p1_win_count = 0
    p2_win_count = 0

    for i in range(500):

        seed = None
        deck = np.linspace(start=LOWEST_CARD, stop=15, num=12, dtype='int')
        if seed != None:
            random.seed(seed)
        random.shuffle(deck)
        cards_p1 = deck[:6]
        cards_p2 = deck[6:]

        # player1 is the first to play: according to the rules, he must have 2 in his deck
        # if this is not the case i switch the decks
        if 2 not in cards_p1:
            cards_p1, cards_p2 = cards_p2, cards_p1

        tree_root = Node(cards_p1, cards_p2, visible_cards=[0] * 4, current_player=1)  # initial state tree
        depths = [12]  # partial depths for the resolution of the tree
        all_paths, all_leaves = solve2(tree_root, depths, generate_tree_function=generate_tree_1)


        # Calculate the count of positive and negative delta_scores
        positive_count, negative_count = count_positive_negative_scores(all_leaves)

        # Update the win counts (add the counts)
        p1_win_count += positive_count
        p2_win_count += negative_count

    # Calculate winrates for each player
    p1_winrate = p1_win_count / 500
    p2_winrate = p2_win_count / 500

    print(f"p1_winrate: {p1_winrate:.2f}")
    print(f"p2_winrate: {p2_winrate:.2f}")


