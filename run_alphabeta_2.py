from Primi_composti_2.tree_primi_composti_2 import generate_tree_2
from utilities.solve_tree import solve
from utilities.utils import set_initial_players_deck, show_visible_cards
from utilities.Stack import *
from utilities.Node import *
from prettytable import PrettyTable 

if __name__ == "__main__":

    seed = 31
    cards_p1, cards_p2 = set_initial_players_deck(seed)

    tree_root = Node(cards_p1, cards_p2, visible_cards=[Stack(), Stack(), Stack(), Stack()], current_player=1)  # initial state tree
    depths = [3] * 8 # partial depths for the resolution of the tree
    assert(sum(depths)==24)
    final_score, final_node, all_paths = solve(tree_root, depths, generate_tree_function=generate_tree_2)

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
            table.add_row([node.parent.current_player, node.card_just_played, show_visible_cards(node.visible_cards), node.delta_score, node.cards_player1, node.cards_player2])
    print(table)
    
    
