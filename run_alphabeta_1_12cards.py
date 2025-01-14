import numpy as np

from Primi_composti_1.tree_primi_composti_1 import generate_tree_1
from utilities.solve_tree import solve
from utilities.utils import  NUM_CARDS_PER_PLAYER, LOWEST_CARD, HIGHEST_CARD, NUMBER_OF_CARDS
from utilities.Node import Node
from prettytable import PrettyTable
import random

if __name__ == "__main__":

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



    tree_root = Node(cards_p1, cards_p2, visible_cards=[0]*4, current_player=1) # initial state tree
    depths = [12] # partial depths for the resolution of the tree
    #assert(sum(depths)==24)
    all_paths = solve(tree_root, depths, generate_tree_function=generate_tree_1)

    print("Deck for Player 1:")
    print(cards_p1)

    print("Deck for Player 2:")
    print(cards_p2)

    # Print the path
    table = PrettyTable()
    table.field_names = ["Player", "Played card", "Gameboard", "Delta", "Deck P1", "Deck P2"]
    table.border = False
    # Set all columns to left-align
    for column in table.field_names:
        table.align[column] = "l"
    for i, path in enumerate(all_paths):
        table.add_row([""]*len(table.field_names))
        for node in path[1:]:
            table.add_row([node.parent.current_player, node.card_just_played, node.visible_cards, node.delta_score, node.cards_player1, node.cards_player2])
    print(table)
