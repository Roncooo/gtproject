from Primi_composti_1.tree_primi_composti_1 import generate_tree_1
from utilities.solve_tree import solve
from utilities.utils import set_initial_players_deck, print_path
from utilities.Node import Node

if __name__ == "__main__":

    cards_p1, cards_p2 = set_initial_players_deck(number_of_cards=12, seed=None)

    tree_root = Node(cards_p1, cards_p2, visible_cards=[0]*4, current_player=1)

    print(f"Solving a match of the version 1 of the game with minimax algorithm and alpha-beta pruning")
    print(f"P1 has {cards_p1} and P2 has {cards_p2}")
    
    full_path = solve(tree_root, generate_tree_function=generate_tree_1)

    print_path(full_path)
