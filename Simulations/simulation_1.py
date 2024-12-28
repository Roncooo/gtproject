import numpy as np
import random
from prettytable import PrettyTable 
from gtproject.utilities.utils import *
from gtproject.utilities.policies import *




def card_score_by_index(card_index):
    ''' Returns the score of a single card '''
    return PRIME_SCORE if is_prime_index(card_index) else COMPOSITE_SCORE

def best_score(visible_cards, result_card):    
    '''
    Gives the best score you can obtain by combining 2 cards among `visible_cards` to obtain `result`.
    Tries all possible combinations of operands and operations.
    Stops if the theoretical best score for that particular position is detected or when all possibilities are calculated.
    '''
    max_operation_score = 3*PRIME_SCORE
    placed_card_score = card_score(result_card)
    best_operation_score = 0 # best score found so far
    
    # this nested loop chooses the couples of operands
    # the order does not matter since is_valid_operation deals with it
    for i in range(4):
        # if you uncomment the following if clause, you remove the possibility to form operations with 
        # the card that the player has just placed. In other words, by commenting the if we allow a#x=x
        if visible_cards[i] == result_card:
            continue
        
        for j in range(i+1, 4):
            
            if not is_valid_operation(result=result_card, operand1=visible_cards[i], operand2=visible_cards[j]):
                continue
            
            score_card_i = PRIME_SCORE if is_prime_index(i) else COMPOSITE_SCORE
            score_card_j = PRIME_SCORE if is_prime_index(j) else COMPOSITE_SCORE
            current_operation_score = score_card_i + score_card_j
            
            if current_operation_score > best_operation_score:
                best_operation_score = current_operation_score
            
            if max_operation_score == best_operation_score:
                return best_operation_score + placed_card_score # early stop
    
    # if no valid operation is found, it is just placed_card_score so 1 or 2
    return best_operation_score + placed_card_score


def place_card_index(card, player_number):
    ''' Tells on which index (in [0,3]) to place a card '''
    return (player_number-1)*2+(0 if is_prime(card) else 1)


def sort_deck_according_to_policy(policy, player_deck):
    ''' Returns the array of cards sorted according to a policy '''
    match policy:
        case 'asc': return np.sort(player_deck)
        case 'greedy_asc': return np.sort(player_deck)
        case 'desc': return np.sort(player_deck)[::-1]
        case 'greedy_desc': return np.sort(player_deck)[::-1]
        case 'rand': return player_deck


def choose_card_by_policy(player_deck, policy, starting_index, visible_cards):
    ''' returns the player_deck with, in position `starting_index`, the next card to be played. `starting_index` is the index from which I start looking for the next card, all those before are already played. '''
    
    # policy is easy, the deck is already sorted accordingly
    if policy in PREDETERMINED_POLICIES:
        return player_deck
    
    # player_deck is already sorted accordingly
    if policy == 'greedy_desc' or policy == 'greedy_asc':
        theoretical_highest_score = 3*PRIME_SCORE
        current_high_score = 0 # the best we can obtain with all the cards (theoretical highest is 3*prime_score)
        best_card_index = starting_index # first card found with the highest score
        # I only look at cards from position `starting_index` to the end of the deck because those in positions [0:starting_index] are already played
        for i, card in enumerate(player_deck[starting_index:]):
            # suppose I want to place this card, I would obtain
            this_score = best_score(visible_cards=visible_cards, result_card=card)
            if this_score > current_high_score:
                current_high_score = this_score
                best_card_index = i + starting_index
            if this_score == theoretical_highest_score: # no need of checking other cards
                break
        
        # this swapping is needed to move to the beginning the cards already used
        # then with player_deck[starting_index:] we can iterate over just new cards
            # example: deck is [2,3,4,5,6,7], player has already played 2 (we are now at iteration 1)
            # if we decide to play 7 then we rearrange the deck to be [2,7,3,4,5,6] so that deck[starting_index] is 7
        temp = player_deck[best_card_index]
        player_deck = np.insert(np.delete(player_deck, best_card_index), starting_index, temp)

        return player_deck

    
def play_one_game(policy1, policy2, seed=None):
    
    deck = np.linspace(start=2, stop=HIGHEST_CARD, num=NUMBER_OF_CARDS, dtype='int')
    
    if seed != None:
        random.seed(seed)
    
    random.shuffle(deck)

    deck_p1 = deck[:NUM_CARDS_PER_PLAYER]
    deck_p2 = deck[NUM_CARDS_PER_PLAYER:]
    
    # player1 is the first to play: according to the rules, he must have 2 in his deck
    # if this is not the case i switch the decks
    if 2 not in deck_p1:
        deck_p1, deck_p2 = deck_p2, deck_p1
    
    # For predetermined policies, this sorting is all choose_card needs.
    # For dynamic policies, the sorting helps with the time complexity.
    deck_p1 = sort_deck_according_to_policy(policy1, deck_p1)
    deck_p2 = sort_deck_according_to_policy(policy2, deck_p2)
    
    score1 = score2 = 0
    # last card on the small decks on the table
    # [primes p1, composites p1, primes p2, composites p2]
    visible_cards = np.zeros(4, dtype='int')

    for i in range(NUM_CARDS_PER_PLAYER):
        
        # this puts in position i the card that is chosen to be played
        deck_p1 = choose_card_by_policy(deck_p1, policy1, i, visible_cards)
        # this actually picks the card
        card1 = deck_p1[i]
        card_index = place_card_index(card1, player_number=1)
        score1 += best_score(visible_cards, result_card=card1)
        # places the card in the table
        visible_cards[card_index] = card1

        deck_p2 = choose_card_by_policy(deck_p2, policy2, i, visible_cards)
        card2 = deck_p2[i]
        card_index = place_card_index(card2, player_number=2)
        score2 += best_score(visible_cards, result_card=card2)
        visible_cards[card_index] = card2

    return score1, score2, deck_p1, deck_p2


def print_game(deck_p1, deck_p2):
    table = PrettyTable()
    table.field_names = ["Player", "Played card", "Gameboard", "Score P1", "Score P2", "Deck P1", "Deck P2"]
    table.border = False
    # Set all columns to left-align
    for column in table.field_names:
        table.align[column] = "l"
    
    visible_cards = np.zeros(4, dtype=int)
    score1 = score2 = 0
    
    for i in range(NUM_CARDS_PER_PLAYER):
        card_p1, card_p2 = deck_p1[i], deck_p2[i] 
        
        score1 += best_score(visible_cards, result_card=card_p1)
        card_index = place_card_index(card_p1, player_number=1)
        visible_cards[card_index] = card_p1
        show_visible_cards = '[' + " ".join("_" if x == 0 else str(x) for x in visible_cards) + ']'
        # here deck_p2[i:] is needed (without +1) because otherwise we would show as if P2 already played his move
        table.add_row([1, card_p1, show_visible_cards, score1, score2, deck_p1[i+1:], deck_p2[i:]])

        show_visible_cards = '[' + " ".join("_" if x == 0 else str(x) for x in visible_cards) + ']'
        score2 += best_score(visible_cards, result_card=card_p2)
        card_index = place_card_index(card_p2, player_number=2)
        visible_cards[card_index] = card_p2
        table.add_row([2, card_p2, show_visible_cards, score1, score2, deck_p1[i+1:], deck_p2[i+1:]])
    
    print(table)


def play_n_games(policy1, policy2, n_games, seed=None, log_game=False):
    win_count_p1 = 0
    tie_count = 0
    tot_score1 = 0
    tot_score2 = 0
    abs_score_diff = 0
    
    for _ in range(n_games):
        score1, score2, deck_p1, deck_p2 = play_one_game(policy1, policy2, seed)
        if score1 > score2:
            win_count_p1 += 1
        if score1 == score2:
            tie_count +=1
        tot_score1 += score1
        tot_score2 += score2
        abs_score_diff += abs(score1-score2)
        if log_game:
            print(f"Game: {policy1} vs {policy2}")
            print_game(deck_p1, deck_p2)
    
    win_count_p2 = n_games-tie_count-win_count_p1
    winrate_p1 = win_count_p1 / n_games
    winrate_p2 = win_count_p2 / n_games
    tierate = tie_count / n_games
    avg_score_1 = tot_score1 / n_games
    avg_score_2 = tot_score2 / n_games
    avg_abs_score_diff = abs_score_diff / n_games
    return winrate_p1, avg_score_1, tierate, winrate_p2, avg_score_2, avg_abs_score_diff


def play_n_games_for_each_policy_combination(n_games=1000, policies=ALL_POLICIES, seed=None, log_game=False):
    results = []
    for p1 in policies:
        row = []
        for p2 in policies:
            winrate_p1, avg_score_1, tierate, winrate_p2, avg_score_2, avg_abs_score_diff = play_n_games(p1, p2, n_games, seed, log_game)
            row += [[winrate_p1, avg_score_1, tierate, winrate_p2, avg_score_2, avg_abs_score_diff]]
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

