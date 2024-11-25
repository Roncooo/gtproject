import numpy as np
import sympy as sp
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

def is_prime_index(index):
    # knowing that gameboard is built like this
    # [primes p1, composites p1, primes p2, composites p2]
    # we can easily tell if in a position there is a prime or not
    return index%2==0

# tells if operand1 and operand2 can give result with the admitted operations
# this function automatically checks all the possible order of operands
def is_valid_operation(result, operand1, operand2):
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

def max_operation_score(result_index):
    # if we do NOT allow a#x=x then
        # if we have a prime result then we can have at best an operation with one prime and one composite: 3 points
        # if we have a composite result then we can have at best an operation with two primes: 4 points
        # if is_prime_index(result_index):
        #     return prime_score + composite_score
        # else:
        #     return 2 * prime_score
        
    # if we DO allow it then we can always (at best) have 2 prime operands
    return 2 * prime_score

# score given just by the placed card
def card_score(result_index):
    return prime_score if is_prime_index(result_index) else composite_score

# Gives the best score you can obtain by combining 2 cards in the gameboard to obtain the card in position result_index
# Tries all possible combinations of operands and operations 
# Stops if the theoretical best score for that particular position is detected or when all possibilities are calculated
def best_score(gb, result_index):    
    max_op_score = max_operation_score(result_index)
    placed_card_score = card_score(result_index)
    best_operation_score = 0 # best score found so far
    
    # this nested loop chooses the couples of operands
    # the order does not matter since is_valid_operation deals with it
    for i in range(4):
        # if you uncomment the following if clause, you remove the possibility to form operations with 
        # the card that the player has just placed. In other words, by commenting the if we allow a#x=x
        # if i == result_index:
        #     continue
        
        if gb[i] == 0: # no card placed in position i
            continue
        for j in range(i+1, 4):
            if gb[j] == 0: # no card placed in position j
                continue
            
            if not is_valid_operation(result=gb[result_index], operand1=gb[i], operand2=gb[j]):
                continue
            
            score_card_i = prime_score if is_prime_index(i) else composite_score
            score_card_j = prime_score if is_prime_index(j) else composite_score
            score_of_this_couple = score_card_i + score_card_j
            
            if score_of_this_couple > best_operation_score:
                best_operation_score = score_of_this_couple
            
            if max_op_score == best_operation_score:
                return best_operation_score + placed_card_score # early stop
    
    # if no valid operation is found, it is just placed_card_score so 1 or 2
    return best_operation_score + placed_card_score

# tells on which index to place a card
def place_card_index(card, player_number):
    return (player_number-1)*2+(0 if sp.isprime(card) else 1)

# returns the array of cards sorted according to a policy
def sort_deck_according_to_policy(policy, player_deck):
    match policy:
        case 'asc': return np.sort(player_deck)
        case 'greedy_asc': return np.sort(player_deck)
        case 'desc': return np.sort(player_deck)[::-1]
        case 'greedy_desc': return np.sort(player_deck)[::-1]
        case 'rand': return player_deck

# returns the player_deck with, in position iteration, the text card to be played
def choose_card(player_deck, player_number, policy, iteration, gameboard):
    if policy in predetermined_policies:
        return player_deck
    
    # player_deck is already sorted accordingly
    if policy == 'greedy_desc' or policy == 'greedy_asc':
        highest_score = 0 # the best we can obtain with all the cards (theoretical highest is 3*prime_score)
        best_card_index = iteration # first card found with the highest score
        for i, card in enumerate(player_deck[iteration:]):
            # suppose i want to place this card, the position would be
            card_index = place_card_index(card, player_number)
            # pretend to place the card: then immediately restored
            temp = gameboard[card_index]
            gameboard[card_index] = card
            this_score = best_score(gameboard, card_index)
            gameboard[card_index] = temp
            if this_score > highest_score:
                highest_score = this_score
                best_card_index = i + iteration
        
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
        
        player1 = choose_card(player1, 1, policy1, i, gb)
        card1 = player1[i]
        card_index = place_card_index(card1, player_number=1)
        gb[card_index] = card1
        score1 += best_score(gb, card_index)
        
        player2 = choose_card(player2, 2, policy2, i, gb)
        card2 = player2[i]
        card_index = place_card_index(card2, player_number=2)
        gb[card_index] = card2
        score2 += best_score(gb, card_index)
    
    return score1, score2


def play_n_games(policy1, policy2, n_games):
    win1 = 0
    ties = 0
    tot_score1 = 0
    tot_score2 = 0
    for i in range(n_games):
        score1, score2 = play_one_game(policy1, policy2)
        tot_score1 += score1
        tot_score2 += score2
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
    return win1, avg_score_1, ties, win2, avg_score_2


def play_n_games_for_each_policy_combination(n_games=1000, show_scores=False, policies=all_policies):
    myTable = PrettyTable(["P1\\P2"] + list(policies))
    start = time.time()
    for p1 in policies:
        row = [p1]
        for p2 in policies:
            win1, avg_score_1, ties, win2, avg_score_2 = play_n_games(p1, p2, n_games)
            if show_scores:
                row += [f"{(win1*100):05.2f}% ({avg_score_1:05.2f}) | {(ties*100):05.2f}% | {(win2*100):05.2f}% ({avg_score_2:05.2f})"]
            else:
                row += [f"{(win1*100):05.2f}% | {(ties*100):05.2f}% | {(win2*100):05.2f}%"]
        myTable.add_row(row)
    end = time.time()
    print("For each cell, win rate p1 (average score p1) | tie rate | win rate p2 (average score p2)")
    print(myTable)
    print(f"{n_games} games for each combination, total time: {end-start:.2f} seconds")


if __name__ == "__main__":
    play_n_games_for_each_policy_combination(n_games=10000, show_scores=True)
