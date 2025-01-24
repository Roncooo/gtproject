from utilities.policies import ALL_POLICIES, SIMPLE_POLICIES
import numpy as np
from multiprocessing import Pool
import time

def sort_deck_according_to_policy(policy, player_deck):
    ''' Returns the array of cards sorted according to a policy '''
    match policy:
        case 'asc': return np.sort(player_deck)
        case 'greedy_asc': return np.sort(player_deck)
        case 'desc': return np.sort(player_deck)[::-1]
        case 'greedy_desc': return np.sort(player_deck)[::-1]
        case _: return player_deck

def play_n_games(policy1, policy2, n_games, play_one_game_function, print_game_function, seed=None, log_game=False):
    '''Plays `n_games` times a match with `policy_1` vs `policy_2`. If `n_games` is greater than 1 then `seed` is ignored (otherwise the games would be identical). This function parallelizes the execution of the different matches, creating one process for each game (up to `max_n_processes`).'''
    
    assert policy1 in ALL_POLICIES
    assert policy2 in ALL_POLICIES
    
    if n_games>1:
        seed = None
    
    win_count_p1 = 0
    tie_count = 0
    tot_score1 = 0
    tot_score2 = 0
    abs_score_diff = 0

    results = []
    for _ in range(n_games):
        results.append(play_one_game_function(policy1, policy2, seed))
    
    for score1, score2, deck_p1, deck_p2 in results:
        if score1 > score2:
            win_count_p1 += 1
        if score1 == score2:
            tie_count += 1
        tot_score1 += score1
        tot_score2 += score2
        abs_score_diff += abs(score1 - score2)
        if log_game:
            print(f"Game: {policy1} vs {policy2}")
            print_game_function(deck_p1, deck_p2)

    win_count_p2 = n_games - tie_count - win_count_p1
    winrate_p1 = win_count_p1 / n_games
    winrate_p2 = win_count_p2 / n_games
    tierate = tie_count / n_games
    avg_score_1 = tot_score1 / n_games
    avg_score_2 = tot_score2 / n_games
    avg_abs_score_diff = abs_score_diff / n_games
    return winrate_p1, avg_score_1, tierate, winrate_p2, avg_score_2, avg_abs_score_diff


def distribute_total(tot, n):
    '''Returns an array of n almost equal elements in such a way that their sum is equal to `tot`.
    
    Example: distribute_total(100, 3) returns [34,33,33]'''
    base_value = tot // n
    remainder = tot % n
    array = [base_value] * n
    for i in range(remainder):
        array[i] += 1
    # remove final zeros if any (may happen if n<tot)
    while array[-1]==0:
        array.pop()
    return array

def weighted_average(list_of_tuples, weights):
    assert len(list_of_tuples)==len(weights)
    weight_sum = sum(weights)
    weighted_list = [0]*len(list_of_tuples[0])
    for i in range(len(list_of_tuples)):
        # element wise multiplication
        weighted_list += np.array(list_of_tuples[i])*(weights[i]/weight_sum)
    return weighted_list

def play_n_games_for_each_policy_combination(play_one_game_function, print_game_function, n_games=1000, policies=SIMPLE_POLICIES, seed=None, log_game=False, max_n_processes=1):
    '''Does what the name says. Uses process parallelization to run simultaneously `max_n_processes` batches of games of the same combination of policies. Set `max_n_policies=0` if you don't want to parallelize. There is some relevant overhead for smaller values of `n_games`.
    
    If you intend to simulate a lot of games, please remember to set log_game=False to speed up the process (a lot)
    '''
    
    parallelize = False if max_n_processes==0 else True
    
    results = []
    for p1 in policies:
        row = []
        for p2 in policies:
            start = time.time()
            if parallelize:
                # idea: each process does k=n_games/n_process games
                k_arr = distribute_total(n_games, max_n_processes)
                with Pool(processes=max_n_processes) as pool:
                    # list of tuples, i-th tuple contains the results (winrate_1, ...) of k_arr[i] games
                    partial_results = pool.starmap(play_n_games, [(p1, p2, k, play_one_game_function, print_game_function, seed, log_game) for k in k_arr])
                winrate_p1, avg_score_1, tierate, winrate_p2, avg_score_2, avg_abs_score_diff = weighted_average(partial_results, k_arr) 
            else:
                winrate_p1, avg_score_1, tierate, winrate_p2, avg_score_2, avg_abs_score_diff = play_n_games(p1, p2, n_games,play_one_game_function, print_game_function, seed, log_game)
            # append the cell of the table to the current row
            row += [[winrate_p1, avg_score_1, tierate, winrate_p2, avg_score_2, avg_abs_score_diff]]
            end = time.time()
            print(f"done {p1} vs {p2} in {end-start:.3f} s")
        results += [row]
    return results