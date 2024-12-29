from Alphabeta_pruning.resolve_tree import resolve
from utilities.utils import set_initial_players_deck
from utilities.Node import *
from prettytable import PrettyTable 

if __name__ == "__main__":

    seed = 31
    cards_p1, cards_p2 = set_initial_players_deck(seed)
    if 2 not in cards_p1:
        cards_p1, cards_p2 = cards_p2, cards_p1

    tree_root = Node(cards_p1, cards_p2, visible_cards=[0, 0, 0, 0]) # initial state tree
    depths = [6, 6, 12] # partial depths for the resolution of the tree
    final_score, final_node, all_paths = resolve(tree_root, depths)

    # Print the path
    table = PrettyTable()
    table.field_names = ["Player", "Played card", "Gameboard", "Delta", "Deck P1", "Deck P2"]
    table.border = False
    # Set all columns to left-align
    for column in table.field_names:
        table.align[column] = "l"
    for i, path in enumerate(all_paths):
        table.add_row([" ", " ", " ", "", " ", " "])
        for node in path[1:]:
            table.add_row([node.parent.current_player, node.card_just_played, node.visible_cards, node.delta_score, node.cards_player1, node.cards_player2])
    print(table)
