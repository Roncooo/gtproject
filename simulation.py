import numpy as np
import random
import time
from prettytable import PrettyTable 

max_card = 25
num_card = 24
cards_per_player = int(num_card/2)
composite_score = 1
prime_score = 2

# Stupid policies, the player does not look at the cards on the table to do his move, there is no thought mid game
predetermined_policies = ('asc', 'desc', 'rand')
# each choice may change on the base of what's on the table
dynamic_policies = ('greedy_desc', 'greedy_asc')
all_policies = predetermined_policies + dynamic_policies

IS_PRIME = (True,True,False,True,False,True,False,False,False,True,False,True,False,False,False,True,False,True,False,False,False,True,False,False)
def is_prime(number):
    return IS_PRIME[number-2]

def is_prime_index(index):
    '''Tells if at position index there are prime cards (True) or composites (False)'''
    return index%2==0

def is_valid_operation(result, operand1, operand2):
    '''
    Tells if `operand1` and `operand2` can give `result` with the admitted operations.
    This function automatically checks all the possible order of operands.
    '''
    if result==operand1+operand2:
        return True
    if result==operand1-operand2 or result==operand2-operand1:
        return True
    if result==operand1*operand2:
        return True
    if operand2!=0 and result==operand1/operand2:
        return True
    if operand1!=0 and result==operand2/operand1:
        return True
    return False

def card_score_by_index(card_index):
    ''' Returns the score of a single card '''
    return prime_score if is_prime_index(card_index) else composite_score

def card_score(card):
    return prime_score if is_prime(card) else composite_score

def best_score(visible_cards, result_card):    
    '''
    Gives the best score you can obtain by combining 2 cards among `visible_cards` to obtain `result`.
    Tries all possible combinations of operands and operations.
    Stops if the theoretical best score for that particular position is detected or when all possibilities are calculated.
    '''
    max_operation_score = 3*prime_score
    placed_card_score = card_score(result_card)
    best_operation_score = 0 # best score found so far
    
    # this nested loop chooses the couples of operands
    # the order does not matter since is_valid_operation deals with it
    for i in range(4):
        # if you uncomment the following if clause, you remove the possibility to form operations with 
        # the card that the player has just placed. In other words, by commenting the if we allow a#x=x
        if visible_cards[i] == result_card:
            continue
        
        if visible_cards[i] == 0: # no card placed in position i
            continue
        for j in range(i+1, 4):
            if visible_cards[j] == 0: # no card placed in position j
                continue
            
            if not is_valid_operation(result=result_card, operand1=visible_cards[i], operand2=visible_cards[j]):
                continue
            
            score_card_i = prime_score if is_prime_index(i) else composite_score
            score_card_j = prime_score if is_prime_index(j) else composite_score
            current_operation_score = score_card_i + score_card_j
            
            if current_operation_score > best_operation_score:
                best_operation_score = current_operation_score
            
            if max_operation_score == best_operation_score:
                return best_operation_score + placed_card_score # early stop
    
    # if no valid operation is found, it is just placed_card_score so 1 or 2
    return best_operation_score + placed_card_score

def place_card_index(card, player_number):
    ''' Tells on which index to place a card '''
    return (player_number-1)*2+(0 if is_prime(card) else 1)

def sort_deck_according_to_policy(policy, player_deck):
    ''' Returns the array of cards sorted according to a policy '''
    match policy:
        case 'asc': return np.sort(player_deck)
        case 'greedy_asc': return np.sort(player_deck)
        case 'desc': return np.sort(player_deck)[::-1]
        case 'greedy_desc': return np.sort(player_deck)[::-1]
        case 'rand': return player_deck

def choose_card(player_deck, policy, iteration, gameboard):
    ''' returns the player_deck with, in position `iteration`, the text card to be played '''
    if policy in predetermined_policies:
        return player_deck
    
    # player_deck is already sorted accordingly
    if policy == 'greedy_desc' or policy == 'greedy_asc':
        theoretical_highest_score = 3*prime_score
        highest_score = 0 # the best we can obtain with all the cards (theoretical highest is 3*prime_score)
        best_card_index = iteration # first card found with the highest score
        for i, card in enumerate(player_deck[iteration:]):
            # suppose i want to place this card, I would obtain
            this_score = best_score(visible_cards=gameboard, result_card=card)
            if this_score > highest_score:
                highest_score = this_score
                best_card_index = i + iteration
            if this_score == theoretical_highest_score: # no need of checking other cards
                break
        
        # this swapping is needed to move to the beginning the cards already used
        # then with player_deck[iteration:] we can iterate over just new cards
            # example: deck is [2,3,4,5,6,7], player has already played 2 (we are now at iteration 1)
            # if we decide to play 7 then we rearrange the deck to be [2,7,3,4,5,6] so that deck[iteration] is 7
        temp = player_deck[best_card_index]
        player_deck = np.insert(np.delete(player_deck, best_card_index), iteration, temp)

        return player_deck

    
def play_one_game(policy1, policy2):    
    # assert(policy1 in predetermined_policies or policy1 in dynamic_policies)
    # assert(policy2 in predetermined_policies or policy2 in dynamic_policies)
    
    deck = np.linspace(start=2, stop=max_card, num=num_card, dtype='int')
    random.shuffle(deck)

    player1 = deck[:cards_per_player]
    player2 = deck[ cards_per_player:]
    
    # player1 is the first to play: according to the rules, he must have 2 in his deck
    # if this is not the case i switch the decks
    if 2 not in player1:
        player1, player2 = player2, player1
    
    # For predetermined policies, this sorting is all choose_card needs.
    # For dynamic policies, the sorting helps with the time complexity.
    player1 = sort_deck_according_to_policy(policy1, player1)
    player2 = sort_deck_according_to_policy(policy2, player2)
    
    score1 = score2 = 0
    # last card on the small decks on the table
    # [primes p1, composites p1, primes p2, composites p2]
    gb = np.zeros(4, dtype='int')
    
    for i in range(cards_per_player):
        
        player1 = choose_card(player1, policy1, i, gb)
        card1 = player1[i]
        card_index = place_card_index(card1, player_number=1)
        gb[card_index] = card1
        score1 += best_score(visible_cards=gb, result_card=card1)
        
        player2 = choose_card(player2, policy2, i, gb)
        card2 = player2[i]
        card_index = place_card_index(card2, player_number=2)
        gb[card_index] = card2
        score2 += best_score(visible_cards=gb, result_card=card2)
    
    return score1, score2


def play_n_games(policy1, policy2, n_games):
    win1 = 0
    ties = 0
    tot_score1 = 0
    tot_score2 = 0
    abs_score_diff = 0
    for i in range(n_games):
        score1, score2 = play_one_game(policy1, policy2)
        tot_score1 += score1
        tot_score2 += score2
        abs_score_diff += abs(score1-score2)
        if score1 > score2:
            win1 += 1
        if score1 == score2:
            ties +=1
    win2 = n_games-ties-win1
    win1/=n_games
    win2/=n_games
    ties/=n_games
    avg_score_1 = tot_score1/n_games
    avg_score_2 = tot_score2/n_games
    avg_abs_score_diff = abs_score_diff/n_games
    return win1, avg_score_1, ties, win2, avg_score_2, avg_abs_score_diff


def play_n_games_for_each_policy_combination(n_games=1000, policies=all_policies):
    results = []
    for p1 in policies:
        row = []
        for p2 in policies:
            win1, avg_score_1, ties, win2, avg_score_2, avg_abs_score_diff = play_n_games(p1, p2, n_games)
            row += [[win1, avg_score_1, ties, win2, avg_score_2, avg_abs_score_diff]]
        results += [row]
    return results
        
def print_results(results, policies, show_scores=False):
    myTable = PrettyTable(["P1\\P2"] + list(policies))
    f = '05.2f'
    for i, results_row in enumerate(results):
        table_row = [policies[i]]
        for result_cell in results_row:
            win1, avg_score_1, ties, win2, avg_score_2, avg_abs_score_diff = result_cell
            if show_scores:
                table_row += [f"{(win1*100):{f}}% ({avg_score_1:{f}}) | {(ties*100):{f}}% | {(win2*100):{f}}% ({avg_score_2:{f}}) | {avg_abs_score_diff:{f}}"]
            else:
                table_row += [f"{(win1*100):{f}}% | {(ties*100):{f}}% | {(win2*100):{f}}% | {avg_abs_score_diff:{f}}"]
        myTable.add_row(table_row)
    print("For each cell, win rate p1 (average score p1) | tie rate | win rate p2 (average score p2) | abs average score difference")
    print(myTable)


if __name__ == "__main__":
    n_games = 10000
    policies = all_policies
    start = time.time()
    results = play_n_games_for_each_policy_combination(n_games = n_games, policies=policies)
    end = time.time()
    print_results(results, policies, True)
    print(f"{n_games} games for each combination, total time: {end-start:.2f} seconds")

