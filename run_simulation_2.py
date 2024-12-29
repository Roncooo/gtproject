from Primi_composti_2.play_primi_composti_2 import *
from utilities.simulations import play_n_games_for_each_policy_combination
import time


if __name__ == "__main__":
    n_games = 1 # remember to disable all the prints in play_one_game to speed up the process (a lot)
    policies = ALL_POLICIES
    
    start = time.time()
    results = play_n_games_for_each_policy_combination(n_games = n_games, policies=policies, play_one_game_function = play_one_game_2, print_game_function = print_game_2, seed=31, log_game=True)
    end = time.time()
    
    print_results(results, policies, True)
    print(f"{n_games} games for each combination, total time: {end-start:.2f} seconds")
