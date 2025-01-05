from Primi_composti_1.play_primi_composti_1 import *
from utilities.policies import SIMPLE_POLICIES
from utilities.simulations import play_n_games_for_each_policy_combination
from utilities.utils import print_results
import time
import os

if __name__ == "__main__":
    n_games = 200000 # remember to disable all the prints in play_one_game to speed up the process (a lot)
    policies = SIMPLE_POLICIES
    max_n_processes = os.cpu_count() # set to 0 if you don't want parallelization (useful for small values of n_games)
    
    start = time.time()
    results = play_n_games_for_each_policy_combination(n_games = n_games, policies=policies, play_one_game_function = play_one_game_1, print_game_function = print_game_1, seed=None, log_game=False, max_n_processes=max_n_processes)
    end = time.time()
    
    print_results(results, policies, True)
    print(f"{n_games} games for each combination, total time: {end-start:.2f} seconds. Ran over {max_n_processes} cpu cores.")
