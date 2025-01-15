from Primi_composti_2.tree_primi_composti_2 import generate_tree_2
from utilities.solve_tree import solve
from utilities.utils import set_initial_players_deck, print_path
from utilities.Stack import Stack
from utilities.Node import Node

if __name__ == "__main__":

    cards_p1, cards_p2 = set_initial_players_deck(number_of_cards=12, seed=None)

    tree_root = Node(cards_p1, cards_p2, visible_cards=[Stack(), Stack(), Stack(), Stack()], current_player=1)

    print(f"Solving a match of the version 2 of the game with minimax algorithm and alpha-beta pruning")
    print(f"P1 has {cards_p1} and P2 has {cards_p2}")
    
    full_path = solve(tree_root, generate_tree_function=generate_tree_2)
    
    print_path(full_path)
