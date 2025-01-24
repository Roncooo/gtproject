from utilities.utils import PRIME_SCORE, card_score_by_value, is_valid_operation, card_score_by_index

def best_score_1(visible_cards, result_card):    
    '''
    Gives the best score you can obtain by combining 2 cards among `visible_cards` to obtain `result`.
    Tries all possible combinations of operands and operations.
    Stops if the theoretical best score for that particular position is detected or when all possibilities are calculated.
    '''
    max_operation_score = 3*PRIME_SCORE
    placed_card_score = card_score_by_value(card_value=result_card)
    best_operation_score = 0 # best score found so far
    
    # this nested loop chooses the couples of operands
    # the order does not matter since is_valid_operation deals with it
    for i in range(4):
        
        for j in range(i+1, 4):
            
            if not is_valid_operation(result=result_card, operand1=visible_cards[i], operand2=visible_cards[j]):
                continue
            
            current_operation_score = card_score_by_index(card_index=i) + card_score_by_index(card_index=j)
            
            if current_operation_score > best_operation_score:
                best_operation_score = current_operation_score
            
            if max_operation_score == best_operation_score:
                return best_operation_score + placed_card_score # early stop
    
    # if no valid operation is found, it is just placed_card_score so 1 or 2
    return best_operation_score + placed_card_score
