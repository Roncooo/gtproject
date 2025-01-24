from Primi_composti_2.play_primi_composti_2 import *
from utilities.policies import SIMPLE_POLICIES, DYNAMIC_POLICIES, MINIMAX_POLICIES, ALL_POLICIES
from utilities.simulations import play_n_games_for_each_policy_combination
from utilities.utils import print_results
import time
import os

if __name__ == "__main__":
    
    # You can significantly increase n_games when simulating simple policies, but when dealing with minimax algorithms, we recommend keeping the number low to ensure computing time remains reasonable
    n_games = 1000 
    policies = SIMPLE_POLICIES # you can also try something like ['minimax_5', 'minimax_6']
    max_n_processes = os.cpu_count() # set to 0 if you don't want parallelization (useful for small values of n_games)
    print(f"Starting to play {n_games} of game 2 for each combination of {policies} with {max_n_processes} parallel processes")
    
    start = time.time()
    results = play_n_games_for_each_policy_combination(n_games = n_games, policies=policies, play_one_game_function = play_one_game_2, print_game_function = print_game_2, seed=None, log_game=False,max_n_processes=max_n_processes)
    end = time.time()
    
    print_results(results, policies, True)
    print(f"{n_games} games for each combination, total time: {end-start:.2f} seconds. Ran over {max_n_processes} cpu cores.")

