import numpy as np
import sympy as sp
import random
from prettytable import PrettyTable 

max_card = 25
num_card = 24
composite_score = 1
prime_score = 2

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


def best_score(gb, result_index):    
    # if we have a prime result then we can have at best an operation with one prime and one composite: 3 points
    # if we have a composite result then we can have at best an operation with two primes: 4 points
    if is_prime_index(result_index):
        max_operation_score = prime_score + composite_score
        placed_card_score = prime_score
    else:
        max_operation_score = 2 * prime_score
        placed_card_score = composite_score
    best_operation_score = 0 # best score found so far
    
    # this nested loop chooses the couples of operands
    # the order does not matter since is_valid_operation deals with it
    for i in range(4):
        if i == result_index:
            continue
        for j in range(i+1, 4):
            if not is_valid_operation(result=gb[result_index], operand1=gb[i], operand2=gb[j]):
                continue
            
            score_card_i = prime_score if is_prime_index(i) else composite_score
            score_card_j = prime_score if is_prime_index(j) else composite_score
            score_of_this_couple = score_card_i + score_card_j
            
            if score_of_this_couple > best_operation_score:
                best_operation_score = score_of_this_couple
            
            if max_operation_score == best_operation_score:
                return best_operation_score + placed_card_score # early stop
    
    # if no valid operation is found, it is just placed_card_score so 1 or 2
    return best_operation_score + placed_card_score
    

# Policies can be 'asc', 'desc', 'rand' (todo, add other policies, ex. primes first etc)
# Those are stupid policies, the player does not look at the cards on the table to do his move
def play_one_game(policy1, policy2):
    cards_per_player = int(num_card/2)
    deck = np.linspace(start=2, stop=max_card, num=num_card, dtype='int')
    random.shuffle(deck)

    player1 = deck[:cards_per_player]
    player2 = deck[ cards_per_player:]
    
    # player1 is the first to play: according to the rules, he must have 2 in his deck
    # if this is not the case i switch the decks
    if 2 not in player1:
        player1, player2 = player2, player1
    
    score1 = 0
    score2 = 0

    # last card on the small decks on the table
    # [primes p1, composites p1, primes p2, composites p2]
    gb = np.zeros(4, dtype='int')

    # policy: sort player1 and player2 decks according to some rule
    # example: player 1 plays lows first and player 2 highs first
    if policy1=='asc':
        player1 = np.sort(player1)
    if policy2=='asc':
        player2 = np.sort(player2)
    if policy1=='desc':
        player1 = np.sort(player1)[::-1]
    if policy2=='desc':
        player2 = np.sort(player2)[::-1]
    if policy1=='rand':
        player1 = player1
    if policy2=='rand':
        player2 = player2

    for i in range(cards_per_player):
        # pick a card
        card1 = player1[i]
        if sp.isprime(card1):
            # place it on your mini deck of primes
            gb[0] = card1
            # calculate the best score you can achieve with the cards already on the table (and not the one you've just placed)
            score1 += best_score(gb, result_index=0)
        else:
            gb[1] = card1
            score1 += best_score(gb, result_index=1)
        
        card2 = player2[i]
        if sp.isprime(card2):
            gb[2] = card2
            score2 += best_score(gb, result_index=2)
        else:
            gb[3] = card2
            score2 += best_score(gb, result_index=3)
    
    return score1, score2


def play_n_games(policy1, policy2, n_games=1000):
    win1 = 0
    ties = 0
    for i in range(n_games):
        score1, score2 = play_one_game(policy1, policy2)
        if score1 > score2:
            win1 += 1
        if score1 == score2:
            ties +=1
    win2 = n_games-ties-win1
    win1/=n_games
    win2/=n_games
    ties/=n_games
    return f"{(win1*100):.2f}% | {(ties*100):.2f}% | {(win2*100):.2f}%"


policies = ['asc', 'desc', 'rand']
myTable = PrettyTable(["P1\\P2"] + policies) 
# now try 1000 games for each combination of policies
for p1 in policies:
    row = [p1]
    for p2 in policies:
        row += [play_n_games(p1, p2, n_games=100000)]
    myTable.add_row(row)

print("For each cell, win rate p1 | tie rate | win rate p2")
print(myTable)
