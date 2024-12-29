from utilities.Node import Node
from utilities.utils import *
from play_primi_composti_1 import best_score

def place_card(visible_cards, new_card, player):
    new_gameboard = visible_cards[:]
    if player == 1:
        if is_prime(new_card):
            new_gameboard[0] = new_card
        else:
            new_gameboard[1] = new_card
    else:
        if is_prime(new_card):
            new_gameboard[2] = new_card
        else:
            new_gameboard[3] = new_card
    return new_gameboard

def generate_tree_1(cards_p1, cards_p2, table_cards, depth):
    root = Node(cards_p1, cards_p2, visible_cards=table_cards)

    def expand(node: Node, depth):
        if depth == 0:
            return
        if node.current_player == 1:
            for c in node.cards_player1:
                this_move_score = best_score(node.visible_cards, c)
                new_delta_score = node.delta_score + this_move_score
                cards_player1_copy = node.cards_player1.copy()
                cards_player1_copy.remove(c)
                new_node = Node(cards_player1_copy, node.cards_player2,
                                current_player=2,
                                delta_score=new_delta_score,
                                visible_cards=place_card(node.visible_cards, c, 1),
                                card_just_played=c,
                                parent=node,
                                )
                node.add_child(new_node)
                expand(new_node, depth - 1)
        else:
            for c in node.cards_player2:
                this_move_score = best_score(node.visible_cards, c)
                new_delta_score = node.delta_score - this_move_score
                cards_player2_copy = node.cards_player2.copy()
                cards_player2_copy.remove(c)
                new_node = Node(node.cards_player1, cards_player2_copy,
                                current_player=1,
                                delta_score=new_delta_score,
                                visible_cards=place_card(node.visible_cards, c, 2),
                                card_just_played=c,
                                parent=node,
                                )
                node.add_child(new_node)
                expand(new_node, depth - 1)

    expand(root, depth)
    return root



