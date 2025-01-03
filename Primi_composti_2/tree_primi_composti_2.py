import copy
from  utilities.Node import Node
from  utilities.utils import PRIME_SCORE, COMPOSITE_SCORE, is_prime, is_valid_operation, remove


def delta(visible_cards):
    score_p1 = visible_cards[0].size()*PRIME_SCORE + visible_cards[1].size()*COMPOSITE_SCORE
    score_p2 = visible_cards[2].size()*PRIME_SCORE + visible_cards[3].size()*COMPOSITE_SCORE
    return score_p1 - score_p2

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

def generate_tree_2(cards_p1, cards_p2, table_cards, depth, current_player):
    root = Node(cards_p1, cards_p2, visible_cards=table_cards, current_player=current_player)
    def expand(node: Node, depth):
        if depth == 0:
            return
        if node.current_player == 1:
            for c in node.cards_player1:
                
                opponent_prime = False if node.visible_cards[2].is_empty() else node.visible_cards[2].top()
                opponent_composite = False if node.visible_cards[3].is_empty() else node.visible_cards[3].top()
                my_prime = False if node.visible_cards[0].is_empty() else node.visible_cards[0].top()
                my_composite = False if node.visible_cards[1].is_empty() else node.visible_cards[1].top()
                
                # I can steal 2 cards from the opponent
                if opponent_prime and opponent_composite and (
                    is_valid_operation(c, opponent_prime, opponent_composite)
                ): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[0].push(new_visible_cards[2].pop())
                    new_visible_cards[1].push(new_visible_cards[3].pop())
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player1_copy = remove(node.cards_player1, c)
                    new_node = Node(cards_player1_copy, node.cards_player2,
                                current_player=2,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                
                # I can steal your prime with my composite or my prime
                elif opponent_prime and (
                    (my_composite and is_valid_operation(c, opponent_prime, my_composite)) or
                    (my_prime and is_valid_operation(c, opponent_prime, my_prime))
                ):
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[0].push(new_visible_cards[2].pop())
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player1_copy = remove(node.cards_player1, c)
                    new_node = Node(cards_player1_copy, node.cards_player2,
                                current_player=2,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                    
                # I can steal your composite with my composite or my prime
                elif opponent_composite and (
                    (my_prime and is_valid_operation(c, opponent_composite, my_prime)) or 
                    (my_composite and is_valid_operation(c, opponent_composite, my_composite))
                ): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[1].push(new_visible_cards[3].pop())
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player1_copy = remove(node.cards_player1, c)
                    new_node = Node(cards_player1_copy, node.cards_player2,
                                current_player=2,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                
                # I cannot steal cards
                else:
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player1_copy = remove(node.cards_player1, c)
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
                
                # I can steal 2 cards from the opponent
                if opponent_composite and opponent_prime and (
                    is_valid_operation(c, opponent_prime, opponent_composite)
                ): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[2].push(new_visible_cards[0].pop())
                    new_visible_cards[3].push(new_visible_cards[1].pop())
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player2_copy = remove(node.cards_player2, c)
                    new_node = Node(node.cards_player1, cards_player2_copy,
                                current_player=1,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                
                # I can steal your prime with my composite or my prime
                elif opponent_prime and (
                    (my_composite and is_valid_operation(c, opponent_prime, my_composite)) or
                    (my_prime and is_valid_operation(c, opponent_prime, my_prime))
                ):
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[2].push(new_visible_cards[0].pop())
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player2_copy = remove(node.cards_player2, c)
                    new_node = Node(node.cards_player1, cards_player2_copy,
                                current_player=1,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                    
                # I can steal your composite with my composite or my prime
                elif opponent_composite and (
                    (my_prime and is_valid_operation(c, opponent_composite, my_prime)) or 
                    (my_composite and is_valid_operation(c, opponent_composite, my_composite))
                ): 
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    new_visible_cards[3].push(new_visible_cards[1].pop())
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player2_copy = remove(node.cards_player2, c)
                    new_node = Node(node.cards_player1, cards_player2_copy,
                                current_player=1,
                                delta_score=new_delta,
                                visible_cards=new_visible_cards,
                                card_just_played=c,
                                parent=node,
                                )
                    node.add_child(new_node)
                    expand(new_node, depth - 1)
                
                # I cannot steal cards
                else:
                    new_visible_cards = copy.deepcopy(node.visible_cards)
                    place_card(new_visible_cards, c, node.current_player)
                    new_delta = delta(new_visible_cards)
                    cards_player2_copy = remove(node.cards_player2, c)
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

