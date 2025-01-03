from utilities.policies import *
import numpy as np
from multiprocessing import Pool


def sort_deck_according_to_policy(policy, player_deck):
    ''' Returns the array of cards sorted according to a policy '''
    match policy:
        case 'asc': return np.sort(player_deck)
        case 'greedy_asc': return np.sort(player_deck)
        case 'desc': return np.sort(player_deck)[::-1]
        case 'greedy_desc': return np.sort(player_deck)[::-1]
        case _: return player_deck

def play_n_games(policy1, policy2, n_games, play_one_game_function, print_game_function, seed=None, log_game=False, max_n_processes=1):
    '''Plays `n_games` times a match with `policy_1` vs `policy_2`. If `n_games` is greater than 1 then `seed` is ignored (otherwise the games would be identical). This function parallelizes the execution of the different matches, creating one process for each game (up to `max_n_processes`).'''
    
    if n_games>1:
        seed = None
    
    win_count_p1 = 0
    tie_count = 0
    tot_score1 = 0
    tot_score2 = 0
    abs_score_diff = 0

    # This context manager automatically handles the joining of processes once the block of code is completed (so no need to explicitly wait for the processes to end)
    with Pool(processes=max_n_processes) as pool:
        results = pool.starmap(play_one_game_function, [(policy1, policy2, seed) for _ in range(n_games)])

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

def play_n_games_for_each_policy_combination(play_one_game_function, print_game_function, n_games=1000, policies=SIMPLE_POLICIES, seed=None, log_game=False, max_n_processes=1):
    results = []
    for p1 in policies:
        row = []
        for p2 in policies:
            winrate_p1, avg_score_1, tierate, winrate_p2, avg_score_2, avg_abs_score_diff = play_n_games(p1, p2, n_games,play_one_game_function, print_game_function, seed, log_game, max_n_processes)
            row += [[winrate_p1, avg_score_1, tierate, winrate_p2, avg_score_2, avg_abs_score_diff]]
        results += [row]
    return results