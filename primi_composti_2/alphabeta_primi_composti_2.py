import random
import time
import copy
import numpy as np
from utilities.Stack import Stack
from utilities.Node import Node
from utilities.utils import *


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


def place_card(visible_cards, new_card, player):
    if player == 1:
        if is_prime(new_card):
            visible_cards[0].push(new_card)
        else:
            visible_cards[1].push(new_card)
    else:
        if is_prime(new_card):
            visible_cards[2].push(new_card)
        else:
            visible_cards[3].push(new_card)


def delta(visible_cards):
    score_p1 = visible_cards[0].size()*PRIME_SCORE + visible_cards[1].size()*COMPOSITE_SCORE
    score_p2 = visible_cards[2].size()*PRIME_SCORE + visible_cards[3].size()*COMPOSITE_SCORE
    return score_p1 - score_p2
    

def generate_tree(cards_p1, cards_p2, table_cards, depth):
    root = Node(cards_p1, cards_p2, visible_cards=table_cards)
    def expand(node: Node, depth):
        if depth == 0:
            return
        if node.current_player == 1:
            for c in node.cards_player1:
                
                opponent_prime = False if node.visible_cards[2].is_empty() else node.visible_cards[2].top()
                opponent_composite = False if node.visible_cards[3].is_empty() else node.visible_cards[3].top()
                my_prime = False if node.visible_cards[0].is_empty() else node.visible_cards[0].top()
                my_composite = False if node.visible_cards[1].is_empty() else node.visible_cards[1].top()
                
                # i can steal 2 cards from the opponent
                if opponent_prime and opponent_composite and (
                    is_valid_operation(c, opponent_prime, opponent_composite)
                ): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[0].push(new_visible_cards[2].pop())
                    new_visible_cards[1].push(new_visible_cards[3].pop())
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player1_copy = copy.deepcopy(node.cards_player1)
                    cards_player1_copy.remove(c)
                    new_node = Node(cards_player1_copy, node.cards_player2,
                                current_player=2,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                
                # i can steal your prime with my composite or my prime
                if opponent_prime and (
                    (my_composite and is_valid_operation(c, opponent_prime, my_composite)) or
                    (my_prime and is_valid_operation(c, opponent_prime, my_prime))
                ):
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[0].push(new_visible_cards[2].pop())
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player1_copy = copy.deepcopy(node.cards_player1)
                    cards_player1_copy.remove(c)
                    new_node = Node(cards_player1_copy, node.cards_player2,
                                current_player=2,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                    
                # i can steal your composite with my composite or my prime
                if opponent_composite and (
                    (my_prime and is_valid_operation(c, opponent_composite, my_prime)) or 
                    (my_composite and is_valid_operation(c, opponent_composite, my_composite))
                ): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[1].push(new_visible_cards[3].pop())
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player1_copy = copy.deepcopy(node.cards_player1)
                    cards_player1_copy.remove(c)
                    new_node = Node(cards_player1_copy, node.cards_player2,
                                current_player=2,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                
                # i cannot steal cards, we are saying that one can also choose to not steal cards
                if True:
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player1_copy = copy.deepcopy(node.cards_player1)
                    cards_player1_copy.remove(c)
                    new_node = Node(cards_player1_copy, node.cards_player2,
                                current_player=2,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                

        else:
            for c in node.cards_player2:
                
                opponent_prime = False if node.visible_cards[0].is_empty() else node.visible_cards[0].top()
                opponent_composite = False if node.visible_cards[1].is_empty() else node.visible_cards[1].top()
                my_prime = False if node.visible_cards[2].is_empty() else node.visible_cards[2].top()
                my_composite = False if node.visible_cards[3].is_empty() else node.visible_cards[3].top()
                
                # i can steal 2 cards from the opponent
                if opponent_composite and opponent_prime and (
                    is_valid_operation(c, opponent_prime, opponent_composite)
                ): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[2].push(new_visible_cards[0].pop())
                    new_visible_cards[3].push(new_visible_cards[1].pop())
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player2_copy = copy.deepcopy(node.cards_player2)
                    cards_player2_copy.remove(c)
                    new_node = Node(node.cards_player1, cards_player2_copy,
                                current_player=1,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                
                # i can steal your prime with my composite or my prime
                if opponent_prime and (
                    (my_composite and is_valid_operation(c, opponent_prime, my_composite)) or
                    (my_prime and is_valid_operation(c, opponent_prime, my_prime))
                ):
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[2].push(new_visible_cards[0].pop())
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player2_copy = copy.deepcopy(node.cards_player2)
                    cards_player2_copy.remove(c)
                    new_node = Node(node.cards_player1, cards_player2_copy,
                                current_player=1,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                    
                # i can steal your composite with my composite or my prime
                if opponent_composite and (
                    (my_prime and is_valid_operation(c, opponent_composite, my_prime)) or 
                    (my_composite and is_valid_operation(c, opponent_composite, my_composite))
                ): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[3].push(new_visible_cards[1].pop())
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player2_copy = copy.deepcopy(node.cards_player2)
                    cards_player2_copy.remove(c)
                    new_node = Node(node.cards_player1, cards_player2_copy,
                                current_player=1,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                
                # i cannot steal cards, we are saying that one can also choose to not steal cards
                if True:
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player2_copy = copy.deepcopy(node.cards_player2)
                    cards_player2_copy.remove(c)
                    new_node = Node(node.cards_player1, cards_player2_copy,
                                current_player=1,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)

    expand(root, depth)
    return root


def match(seed_value, depths):

    deck = np.linspace(start=LOWEST_CARD, stop=HIGHEST_CARD, num=NUMBER_OF_CARDS, dtype='int')
    if seed_value!=None:
        random.seed(seed_value)
    random.shuffle(deck)
    cards_p1 = set(deck[:NUM_CARDS_PER_PLAYER])
    cards_p2 = set(deck[NUM_CARDS_PER_PLAYER:])

    if 2 not in cards_p1:
        cards_p1, cards_p2 = cards_p2, cards_p1

    # Stato iniziale
    current_node = Node(cards_p1, cards_p2, visible_cards=[Stack(), Stack(), Stack(), Stack()])
    all_paths = []

    for depth in depths:
        start = time.time()
        
        # Genera l'albero per il turno corrente
        root = generate_tree(current_node.cards_player1, current_node.cards_player2, current_node.visible_cards, depth)
        score, leaf_minimax = minimax(root, depth, float('-inf'), float('+inf'), True)

        # Aggiorna lo stato per il prossimo turno
        current_node = leaf_minimax
        path = Node.get_path(leaf_minimax)
        all_paths.append(path)
        
        end = time.time()
        print(f"Done {depth} levels in {end-start:.2f} s")

    return score, current_node, all_paths
