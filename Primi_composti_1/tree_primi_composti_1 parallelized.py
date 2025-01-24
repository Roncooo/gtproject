from utilities.Node import Node
from utilities.utils import is_prime, remove
from Primi_composti_1.score import best_score_1
from multiprocessing import Pool
import copy

def place_card(visible_cards, new_card, player):
    new_gameboard = visible_cards.copy()
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

def process_card_p1(c, node, depth):
    this_move_score = best_score_1(node.visible_cards, c)
    new_delta_score = node.delta_score + this_move_score
    cards_player1_copy = remove(node.cards_player1, c)
    new_node = Node(cards_player1_copy, node.cards_player2,
                    current_player=2,
                    delta_score=new_delta_score,
                    visible_cards=place_card(node.visible_cards, c, 1),
                    card_just_played=c,
                    parent=node,
                    )
    node.add_child(new_node)
    expand(new_node, depth - 1, parallelize=False)
    return new_node

def process_card_p2(c, node, depth):
    this_move_score = best_score_1(node.visible_cards, c)
    new_delta_score = node.delta_score - this_move_score
    cards_player2_copy = remove(node.cards_player2, c)
    new_node = Node(node.cards_player1, cards_player2_copy,
                    current_player=1,
                    delta_score=new_delta_score,
                    visible_cards=place_card(node.visible_cards, c, 2),
                    card_just_played=c,
                    parent=node,
                    )
    node.add_child(new_node)
    expand(new_node, depth - 1, parallelize=False)
    return new_node

def expand(node: Node, depth:int, parallelize: bool):
    if depth == 0:
        return
    if parallelize:
        if node.current_player == 1:
            with Pool(processes=7) as pool:
                children = pool.starmap(process_card_p1, [(c, copy.deepcopy(node), depth) for c in node.cards_player1])
            for child in children:
                node.add_child(child)
        else:
            with Pool(processes=7) as pool:
                children = pool.starmap(process_card_p2, [(c, copy.deepcopy(node), depth) for c in node.cards_player2])
            for child in children:
                node.add_child(child)
    else:
        if node.current_player == 1:
            for c in node.cards_player1:
                process_card_p1(c, node, depth)
        else:
            for c in node.cards_player2:
                process_card_p2(c, node, depth)
