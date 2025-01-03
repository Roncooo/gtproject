from Primi_composti_1.play_primi_composti_1 import *
from utilities.simulations import play_n_games_for_each_policy_combination
from utilities.utils import print_results
import time
import os

if __name__ == "__main__":
    n_games = 10 # remember to disable all the prints in play_one_game to speed up the process (a lot)
    policies = ['asc', 'minimax_4']
    
    start = time.time()
    results = play_n_games_for_each_policy_combination(n_games = n_games, policies=policies, play_one_game_function = play_one_game_1, print_game_function = print_game_1, seed=None, log_game=False, max_n_processes=os.cpu_count())
    end = time.time()
    
    print_results(results, policies, True)
    print(f"{n_games} games for each combination, total time: {end-start:.2f} seconds")
