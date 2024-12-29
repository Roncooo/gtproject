from utilities.Node import Node
from utilities.utils import *

def best_score(visible_cards, result_card):
    '''
    Gives the best score you can obtain by combining 2 cards among `visible_cards` to obtain `result`.
    Tries all possible combinations of operands and operations.
    Stops if the theoretical best score for that particular position is detected or when all possibilities are calculated.
    '''
    max_operation_score = 2 * PRIME_SCORE
    placed_card_score = card_score(result_card)
    best_operation_score = 0  # best score found so far

    # this nested loop chooses the couples of operands
    # the order does not matter since is_valid_operation deals with it
    for i in range(4):

        for j in range(i + 1, 4):

            if visible_cards[j] == 0:  # no card placed in position j
                continue

            if not is_valid_operation(result=result_card, operand1=visible_cards[i], operand2=visible_cards[j]):
                continue

            score_card_i = PRIME_SCORE if is_prime_index(i) else COMPOSITE_SCORE
            score_card_j = PRIME_SCORE if is_prime_index(j) else COMPOSITE_SCORE
            current_operation_score = score_card_i + score_card_j

            if current_operation_score > best_operation_score:
                best_operation_score = current_operation_score

            if max_operation_score == best_operation_score:
                return best_operation_score + placed_card_score  # early stop

    # if no valid operation is found, it is just placed_card_score so 1 or 2
    return best_operation_score + placed_card_score


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



