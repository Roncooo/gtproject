import numpy as np
import sympy as sp
import random
import itertools
import operator
import time
from prettytable import PrettyTable 

max_card = 25
num_card = 24

import warnings
# Suppress some numerical useless errors 
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*divide by zero.*")
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*invalid value encountered in scalar divide.*")
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*invalid value encountered in scalar multiply.*")


# Returns, if it exists, the tuple like (num op num op num) that gives as output result, otherwise []
# It tries all the possible permutations of numbers and operations
# In our game we are happy if we find one expression with 3 numbers that gives the result. If we find it,
# it means that we used all the possible numbers, thus getting the maximum score in that case
# So we do not care about different permutations of the 3 operands or operations
def find_combination_of_3(numbers, result):
    if len(numbers) != 3:
        raise ValueError("The function supports exactly 3 numbers.")
    
    # Define the operations
    operations = [operator.add, operator.sub, operator.mul, operator.truediv]
    operation_symbols = ['+', '-', '*', '/']
    
    # Generate all permutations of numbers
    for num_order in itertools.permutations(numbers):
        # Generate all combinations of operations
        for op1_index, op1 in enumerate(operations):
            for op2_index, op2 in enumerate(operations):
                try:
                    # Compute results with all combinations of numbers and operations
                    res1 = op1(num_order[0], num_order[1])
                    res2 = op2(res1, num_order[2])
                    if res2==result:
                        return (num_order[0], 
                                    operation_symbols[op1_index], 
                                    num_order[1],
                                    operation_symbols[op2_index], 
                                    num_order[2], 
                                    res2)
                except ZeroDivisionError or ValueError:
                    continue
    return []

# Returns, if existing, an array of all the possible tuples (num op num = result), otherwise []
# In the case of operations with two cards, we do care about all possible combinations, because some
# of them may have a different number of primes and composites, and so different score
def find_combinations_of_2(numbers):
    if len(numbers) != 2:
        raise ValueError("The function supports exactly 2 numbers.")
    
    # Define the operations
    operations = [operator.add, operator.sub, operator.mul, operator.truediv]
    operation_symbols = ['+', '-', '*', '/']
    
    results = []
    
    # Generate all permutations of numbers
    for num_order in itertools.permutations(numbers):
        # Generate all combinations of operations
        for op_index, op in enumerate(operations):
            try:
                # Compute results with all combinations of numbers and operations
                res = op(num_order[0], num_order[1])
                results.append((num_order[0], 
                                operation_symbols[op_index], 
                                num_order[1],
                                res))
            except ZeroDivisionError or ValueError:
                continue
    return results

def score(comb):
    score = 0
    prime_points = 2
    composite_points = 1
    # this works both for comb2 and comb3
    for n in comb[0::2]:
        if sp.isprime(n):
            score += prime_points
        else:
            score += composite_points
    return score

def best_score(gb, result_index):
    cards = np.delete(gb, result_index)
    result = gb[result_index]
    
    comb3 = find_combination_of_3(cards, result)
    if comb3!=[]:
        # in this case the score is unique because the computation uses all the three remaining cards
        return score(comb3)
          
    comb2 = (find_combinations_of_2((cards[0], cards[1])) + 
             find_combinations_of_2((cards[0], cards[2])) + 
             find_combinations_of_2((cards[1], cards[2])) )
    # only the combinations that have as result the wanted number
    valid_comb2 = [comb for comb in comb2 if comb[3]==result]
    if len(valid_comb2)==0:
        # no combinations of 3 nor of 2 found -> 0 points
        return 0
    
    # there is at least one combination of two that gives result 
    return max([score(comb) for comb in valid_comb2])


# Policies can be 'asc', 'desc', 'rand' (todo, add other policies, ex. primes first etc)
# Those are stupid policies, the player does not look at the cards on the table to do his move
def play_one_game(policy1, policy2):
    cards_per_player = int(num_card/2)
    deck = np.linspace(start=2, stop=max_card, num=num_card, dtype='int')
    random.shuffle(deck)

    player1 = deck[:cards_per_player]
    player2 = deck[ cards_per_player:]
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
    start_time = time.time()
    for i in range(n_games):
        score1, score2 = play_one_game(policy1, policy2)
        if score1 > score2:
            win1 += 1
        if score1 == score2:
            ties +=1
    win2 = n_games-ties-win1
    end_time = time.time()
 
    myTable = PrettyTable(["Player", "Policy", "Win rate"]) 
    myTable.add_row(["P1", policy1, win1/n_games]) 
    myTable.add_row(["P2", policy2, win2/n_games]) 
    myTable.add_row(["Tie", "", ties/n_games])
    print(f"Played {n_games} games in {end_time-start_time:.3f} s")
    print(myTable)


# now try 1000 games for each combination of policies
policies = ['asc', 'desc', 'rand']
for p1 in policies:
    for p2 in policies:
        play_n_games(p1, p2)

