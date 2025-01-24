from utilities.utils import PRIME_SCORE, NUM_CARDS_PER_PLAYER, NUMBER_OF_CARDS, shift_element, set_initial_players_deck, place_card_index
from utilities.policies import PREDETERMINED_POLICIES, MINIMAX_POLICIES
from utilities.simulations import sort_deck_according_to_policy
from Primi_composti_1.tree_primi_composti_1 import generate_tree_1
from utilities.solve_tree import minimax
from Primi_composti_1.score import best_score_1
import numpy as np
from prettytable import PrettyTable

def choose_card_by_policy_1(my_deck, opponent_deck, policy, my_starting_index, opponent_starting_index, visible_cards, current_player):
    ''' 
    returns a copy of `my_deck` with, in position `my_starting_index`, the next card to be played. `my_starting_index` is the index from which I (current player) start looking for the next card, all those before are already played. `opponent_deck` and `opponent_starting_index` are needed only for `MINIMAX_POLICIES`.
    '''
    
    # policy is easy, the deck is already sorted accordingly
    if policy in PREDETERMINED_POLICIES:
        return my_deck
    
    # player_deck is already sorted accordingly
    if policy == 'greedy_desc' or policy == 'greedy_asc' or policy == 'greedy_rand':
        theoretical_highest_score = 3*PRIME_SCORE
        current_high_score = 0 # the best we can obtain with all the cards (theoretical highest is 3*prime_score)
        best_card_index = my_starting_index # first card found with the highest score
        # I only look at cards from position `starting_index` to the end of the deck because those in positions [0:starting_index] are already played
        for i, card in enumerate(my_deck[my_starting_index:]):
            # suppose I want to place this card, I would obtain
            this_score = best_score_1(visible_cards=visible_cards, result_card=card)
            if this_score > current_high_score:
                current_high_score = this_score
                best_card_index = i + my_starting_index
            if this_score == theoretical_highest_score: # no need of checking other cards
                break
        
        # this swapping is needed to move to the beginning the cards already used
        # then with player_deck[starting_index:] we can iterate over just new cards
            # example: deck is [2,3,4,5,6,7], player has already played 2 (we are now at iteration 1)
            # if we decide to play 7 then we rearrange the deck to be [2,7,3,4,5,6] so that deck[starting_index] is 7
        return shift_element(my_deck, best_card_index, my_starting_index)
    
    if policy in MINIMAX_POLICIES:
        # minimax policies only have depths that are one digit values and so i can take the last char and convert it to int
        depth = int(policy[-1])
        maximizing_player = True if current_player==1 else False
        cards_p1 = my_deck[my_starting_index:] if current_player==1 else opponent_deck[opponent_starting_index:]
        cards_p2 = my_deck[my_starting_index:] if current_player==2 else opponent_deck[opponent_starting_index:]
        
        root = generate_tree_1(cards_p1, cards_p2, visible_cards.copy(), depth, current_player)
        val, leaf = minimax(root, depth, maximizing_player)
        
        # find the next card to be played
        path = leaf.get_path()
        # root has always at least a child, so at least one valid card to be used
        card_played = path[1].card_just_played
        best_card_index = np.where(my_deck == card_played)[0]
        return shift_element(my_deck, best_card_index, my_starting_index)

def play_one_game_1(policy1, policy2, seed=None):
    '''Returns the score of player 1, score of player 2, deck of player 1 and deck of player 2. The decks are returned for the logging and printing of the game since they are sorted from the first card played to the last.'''
    deck_p1, deck_p2 = set_initial_players_deck(number_of_cards=NUMBER_OF_CARDS, seed=seed)

    # For predetermined policies, this sorting is all choose_card needs.
    # For dynamic policies, the sorting helps with the time complexity.
    deck_p1 = sort_deck_according_to_policy(policy1, deck_p1)
    deck_p2 = sort_deck_according_to_policy(policy2, deck_p2)
    
    score1: int = 0
    score2: int = 0
    # last card on the small decks on the table
    # [primes p1, composites p1, primes p2, composites p2]
    visible_cards = np.zeros(4, dtype='int')

    for i in range(NUM_CARDS_PER_PLAYER):
        
        # this puts in position i the card that is chosen to be played
        deck_p1 = choose_card_by_policy_1(deck_p1, deck_p2, policy1, my_starting_index=i, opponent_starting_index=i, visible_cards=visible_cards, current_player=1)
        # this actually picks the card
        card1 = deck_p1[i]
        card_index = place_card_index(card1, player_number=1)
        score1 += best_score_1(visible_cards, result_card=card1)
        # places the card in the table
        visible_cards[card_index] = card1

        # here opponent_starting_index is i+1 because p1 has already played his i-th card and the next he will play is the (i+1)-th
        deck_p2 = choose_card_by_policy_1(deck_p2, deck_p1, policy2, my_starting_index=i, opponent_starting_index=i+1, visible_cards=visible_cards, current_player=2)
        card2 = deck_p2[i]
        card_index = place_card_index(card2, player_number=2)
        score2 += best_score_1(visible_cards, result_card=card2)
        visible_cards[card_index] = card2

    return score1, score2, deck_p1, deck_p2


def print_game_1(deck_p1, deck_p2):
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
        
        score1 += best_score_1(visible_cards, result_card=card_p1)
        card_index = place_card_index(card_p1, player_number=1)
        visible_cards[card_index] = card_p1
        show_visible_cards = '[' + " ".join("_" if x == 0 else str(x) for x in visible_cards) + ']'
        # here deck_p2[i:] is needed (without +1) because otherwise we would show as if P2 already played his move
        table.add_row([1, card_p1, show_visible_cards, score1, score2, deck_p1[i+1:], deck_p2[i:]])

        show_visible_cards = '[' + " ".join("_" if x == 0 else str(x) for x in visible_cards) + ']'
        score2 += best_score_1(visible_cards, result_card=card_p2)
        card_index = place_card_index(card_p2, player_number=2)
        visible_cards[card_index] = card_p2
        table.add_row([2, card_p2, show_visible_cards, score1, score2, deck_p1[i+1:], deck_p2[i+1:]])
    
    print(table)
