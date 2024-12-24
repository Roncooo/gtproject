from inspect import stack
import random
import time
import copy

import numpy as np

# Costanti
PRIMI = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73}
COMPOSTI = set(range(2, 74)) - PRIMI
ALL_NUMBERS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25)
IS_PRIME = (
True, True, False, True, False, True, False, False, False, True, False, True, False, False, False, True, False, True,
False, False, False, True, False, False)

#mi dice se il numero in questione è primo
def is_prime(number):
    return IS_PRIME[number - 2]


composite_score = 1
prime_score = 2

def is_prime_index(index):
    '''Tells if at position index of the gameboard there are prime cards (True) or composites (False)'''
    return index % 2 == 0

# restituisce lo score di una carta
def card_score(card):
    return prime_score if is_prime(card) else composite_score

def is_valid_operation(result, operand1, operand2):
    '''
    Tells if `operand1` and `operand2` can give `result` with the admitted operations.
    This function automatically checks all the possible order of operands.
    '''
    if result == operand1 + operand2:
        return True
    if result == operand1 - operand2 or result == operand2 - operand1:
        return True
    if result == operand1 * operand2:
        return True
    if operand2 != 0 and result == operand1 / operand2:
        return True
    if operand1 != 0 and result == operand2 / operand1:
        return True
    return False

# Nodo dell'albero
class Node:
    def __init__(self, cards_player1: set, cards_player2: set, current_player=1, delta_score=0,
                 visible_cards=[[0], [0], [0], [0]], card_just_played=None, parent=None):
        self.current_player = current_player  # 1 or 2, it's who has to move next (not who has just played)
        self.delta_score = delta_score  # score 1 - score 2
        self.cards_player1 = cards_player1
        self.cards_player2 = cards_player2
        self.visible_cards = visible_cards  # [p1, c1, p2, c2] now 4 stacks
        self.card_just_played = card_just_played
        self.children = []
        self.parent = parent

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_path(self):
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]  # Inverti per avere il percorso dalla radice


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
            visible_cards[0].append(new_card)
        else:
            visible_cards[1].append(new_card)
    else:
        if is_prime(new_card):
            visible_cards[2].append(new_card)
        else:
            visible_cards[3].append(new_card)


def delta(visible_cards):
    score_p1 = len(visible_cards[0])*prime_score + len(visible_cards[1])*composite_score
    score_p2 = len(visible_cards[1])*prime_score + len(visible_cards[3])*composite_score
    return score_p1 - score_p2
    

def generate_tree(cards_p1, cards_p2, table_cards, depth):
    root = Node(cards_p1, cards_p2, visible_cards=table_cards)
    def expand(node: Node, depth):
        if depth == 0:
            return
        if node.current_player == 1:
            for c in node.cards_player1:
                
                opponent_prime = False if node.visible_cards[2][-1]==0 else node.visible_cards[2][-1]
                opponent_composite = False if node.visible_cards[3][-1]==0 else node.visible_cards[3][-1]
                my_prime = False if node.visible_cards[0][-1]==0 else node.visible_cards[0][-1]
                my_composite = False if node.visible_cards[1][-1]==0 else node.visible_cards[1][-1]
                
                # i can steal 2 cards from the opponent
                if opponent_prime and opponent_composite and is_valid_operation(c, opponent_prime, opponent_composite): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[0].append(node.visible_cards[2].pop())
                    new_visible_cards[1].append(node.visible_cards[3].pop())
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
                if opponent_prime and (my_composite and is_valid_operation(c, opponent_prime, my_composite)) or (my_prime and is_valid_operation(c, opponent_prime, my_prime)): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[0].append(node.visible_cards[2].pop())
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
                if opponent_composite and ((my_prime and is_valid_operation(c, opponent_composite, my_prime)) or (my_composite and is_valid_operation(c, opponent_composite, my_composite))): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[1].append(node.visible_cards[3].pop())
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
                
                opponent_prime = False if node.visible_cards[0][-1]==0 else node.visible_cards[0][-1]
                opponent_composite = False if node.visible_cards[3][-1]==0 else node.visible_cards[1][-1]
                my_prime = False if node.visible_cards[2][-1]==0 else node.visible_cards[2][-1]
                my_composite = False if node.visible_cards[3][-1]==0 else node.visible_cards[3][-1]
                
                # i can steal 2 cards from the opponent
                if opponent_composite and opponent_prime and is_valid_operation(c, opponent_prime, opponent_composite): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[2].append(node.visible_cards[0].pop())
                    new_visible_cards[3].append(node.visible_cards[1].pop())
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
                if opponent_prime and ((my_composite and is_valid_operation(c, opponent_prime, my_composite)) or (my_prime and is_valid_operation(c, opponent_prime, my_prime))): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[2].append(node.visible_cards[0].pop())
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
                if opponent_composite and ((my_prime and is_valid_operation(c, opponent_composite, my_prime)) or (my_composite and is_valid_operation(c, opponent_composite, my_composite))): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[3].append(node.visible_cards[1].pop())
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

    deck = np.linspace(start=2, stop=25, num=24, dtype='int')
    random.seed(seed_value)
    random.shuffle(deck)
    cards_p1 = set(deck[:12])
    cards_p2 = set(deck[12:])

    if 2 not in cards_p1:
        cards_p1, cards_p2 = cards_p2, cards_p1

    # Stato iniziale
    current_node = Node(cards_p1, cards_p2)
    all_paths = []

    for depth in depths:
        # Genera l'albero per il turno corrente
        root = generate_tree(current_node.cards_player1, current_node.cards_player2, current_node.visible_cards, depth)
        score, leaf_minimax = minimax(root, depth, float('-inf'), float('+inf'), True)

        # Aggiorna lo stato per il prossimo turno
        current_node = leaf_minimax
        path = Node.get_path(leaf_minimax)
        all_paths.append(path)
        
        print(f"End of level {depth}")

    return score, current_node, all_paths


if __name__ == "__main__":

    seed = 31
    # depths = [4, 6, 6, 8]  # Profondità per 4 turni
    depths = [4] * 6
    final_score, final_node, all_paths = match(seed, depths)

    # Stampa i percorsi
    for i, path in enumerate(all_paths):
        print(f"Path {i+1}:")
        for node in path[1:]:
            print(f"Giocatore {node.parent.current_player} ha giocato la carta {node.card_just_played} Stato del tavolo: {[node.visible_cards[i][-1] for i in range(0,4)]}. Punteggio : {node.delta_score}, Carte Giocatore 1: {node.cards_player1}, Carte Giocatore 2: {node.cards_player2}")

