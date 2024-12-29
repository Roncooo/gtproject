from utilities.Stack import Stack
from utilities.utils import *
from utilities.policies import *
from utilities.simulations import sort_deck_according_to_policy
import copy
from utilities.solve_tree import minimax
from Primi_composti_2.tree_primi_composti_2 import generate_tree_2

def best_score(visible_cards, result_card, current_player):
    '''
    Gives the best score you can obtain by combining 2 cards among `visible_cards` to obtain `result`, possibly stealing cards from the opponent. This changes the system of points. 
    Tries all possible combinations of operands and operations.
    Stops if the theoretical best score for that particular position is detected or when all possibilities are calculated.
    '''
    max_operation_score = 3 # in the best case I can steal one prime and one composite
    placed_card_score = card_score(result_card)
    best_operation_score = 0 # best score found so far
    
    # this nested loop chooses the couples of operands
    # the order does not matter since is_valid_operation deals with it
    for i in range(4):
        
        for j in range(i+1, 4):
            
            operand_1 = False if visible_cards[i].is_empty() else visible_cards[i].top()
            operand_2 = False if visible_cards[j].is_empty() else visible_cards[j].top()
            
            if not operand_1 or not operand_2:
                continue
            
            if not is_valid_operation(result=result_card, operand1=operand_1, operand2=operand_2):
                continue
            
            score_card_i = PRIME_SCORE if is_prime_index(i) else COMPOSITE_SCORE
            score_card_j = PRIME_SCORE if is_prime_index(j) else COMPOSITE_SCORE
            # if i make an operation with a card of the opponent, i get those points
            current_operation_score  = score_card_i if whose_card_is_this(i)!=current_player else 0
            current_operation_score += score_card_j if whose_card_is_this(j)!=current_player else 0
            
            if current_operation_score > best_operation_score:
                best_operation_score = current_operation_score
            
            if max_operation_score == best_operation_score:
                total_best_score = best_operation_score + placed_card_score
                return total_best_score
    
    # if no valid operation is found, it is just placed_card_score so 1 or 2
    total_best_score = best_operation_score + placed_card_score
    return total_best_score


def find_stolen_card_indexes(played_card, points_made, player):
    '''
    Given `played_card`, `poins_made` and `player`, returns the indexes (among the visible_cards) of the cards stolen to my opponent in the best action possible. Returns, in order and possibly -1, the index of the stolen PRIME card and then the index of the COMPOSITE card.
    '''
    # points made just from the stolen cards
    operands_points = points_made - card_score(played_card)
        
    match operands_points:
        case 0: return -1, -1
        case 1: return -1, opponent_composite_index(player)
        case 2: return opponent_prime_index(player), -1
        case 3: return opponent_prime_index(player), opponent_composite_index(player)
    

def choose_card_by_policy_2(my_deck, opponent_deck, policy, my_starting_index, opponent_starting_index, visible_cards, current_player):
    ''' returns the my_deck with, in position `my_starting_index`, the next card to be played. `my_starting_index` is the index from which I start looking for the next card, all those before are already played. 
    opponent_deck and opponent_starting_index are needed only for MINIMAX_POLICIES
    '''
    
    # policy is easy, the deck is already sorted accordingly
    if policy in PREDETERMINED_POLICIES:
        return my_deck
    
    # player_deck is already sorted accordingly
    if policy == 'greedy_desc' or policy == 'greedy_asc' or policy == 'greedy_rand':
        theoretical_highest_score = 5 # I steal a prime and a composite and i place my prime
        current_high_score = 0 # the best we can obtain with all the cards
        best_card_index = my_starting_index # first card found with the highest score
        
        # I only look at cards from position `my_starting_index` to the end of the deck because those in positions [0:my_starting_index] are already played
        for i, card in enumerate(my_deck[my_starting_index:]):
            # suppose I want to place this card, I would obtain
            this_score = best_score(visible_cards=visible_cards, result_card=card, current_player=current_player)
            if this_score > current_high_score:
                current_high_score = this_score
                best_card_index = i + my_starting_index
            if this_score == theoretical_highest_score: # no need of checking other cards
                break
        
        # this swapping is needed to move to the beginning the cards already used
        # then with player_deck[my_starting_index:] we can iterate over just new cards
            # example: deck is [2,3,4,5,6,7], player has already played 2 (we are now at iteration 1)
            # if we decide to play 7 then we rearrange the deck to be [2,7,3,4,5,6] so that deck[starting_index] is 7
        temp = my_deck[best_card_index]
        my_deck = np.insert(np.delete(my_deck, best_card_index), my_starting_index, temp)

        return my_deck
    
    if policy in MINIMAX_POLICIES:
        # minimax policies only have depths that are one digit values and so i can take the last char and convert it to int
        depth = int(policy[-1])
        root = generate_tree_2(set(my_deck[my_starting_index:]), set(opponent_deck[opponent_starting_index:]), copy.deepcopy(visible_cards), depth)
        am_i_p1 = 2 in my_deck
        val, leaf = minimax(root, depth, am_i_p1)
        
        # find the next card to be played
        path = leaf.get_path()
        card_played = path[1].card_just_played
        best_card_index = np.where(my_deck == card_played)[0]
        return shift_element(my_deck, best_card_index, my_starting_index)


def steal_and_place_cards(visible_cards, played_card, move_score, player):
    '''
    Manages the stealing of cards from the opponent and the placement of the played card.
    '''
    stolen_prime_index, stolen_composite_index = find_stolen_card_indexes(played_card, move_score, player)
    if stolen_prime_index!=-1:
        stolen_prime_card = visible_cards[stolen_prime_index].pop()
        visible_cards[my_prime_index(player)].push(stolen_prime_card)
    if stolen_composite_index!=-1:
        stolen_composite_card = visible_cards[stolen_composite_index].pop()
        visible_cards[my_composite_index(player)].push(stolen_composite_card)
        
    # places the card on the table
    card_index = place_card_index(played_card, player)
    visible_cards[card_index].push(played_card)


def play_one_game_2(policy1, policy2, seed=None):
    
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
    visible_cards = [Stack(), Stack(), Stack(), Stack()]

    for i in range(NUM_CARDS_PER_PLAYER):
        
        # this puts in position i the card that is chosen to be played
        deck_p1 = choose_card_by_policy_2(deck_p1, deck_p2, policy1, i, i, visible_cards, current_player=1)
        # this actually picks the card
        card_p1 = deck_p1[i]
        move_score = best_score(visible_cards, result_card=card_p1, current_player=1)
        steal_and_place_cards(visible_cards, card_p1, move_score, 1)  
        score1 += move_score

        # here opponent_starting_index is i+1 because p1 has already played his i-th card and the next he will play is the (i+1)-th
        deck_p2 = choose_card_by_policy_2(deck_p2, deck_p1, policy2, i, i+1, visible_cards, current_player=2)
        card_p2 = deck_p2[i]
        move_score = best_score(visible_cards, result_card=card_p2, current_player=2)
        steal_and_place_cards(visible_cards, card_p2, move_score, 2)  
        score2 += move_score 

    return score1, score2, deck_p1, deck_p2


def print_game_2(deck_p1, deck_p2):
    table = PrettyTable()
    table.field_names = ["Player", "Played card", "Gameboard", "Score P1", "Score P2", "Deck P1", "Deck P2"]
    table.border = False
    # Set all columns to left-align
    for column in table.field_names:
        table.align[column] = "l"
    
    visible_cards = [Stack(), Stack(), Stack(), Stack()]
    score1 = score2 = 0
    
    for i in range(NUM_CARDS_PER_PLAYER):
        card_p1, card_p2 = deck_p1[i], deck_p2[i] 
        
        move_score = best_score(visible_cards, result_card=card_p1, current_player=1)
        steal_and_place_cards(visible_cards, card_p1, move_score, 1)  
        score1 += move_score
        show_visible_cards = '[' + " ".join("_" if x == 0 else str(x.safe_top_just_for_print()) for x in visible_cards) + ']'
        # here deck_p2[i:] is needed (without +1) because otherwise we would show as if P2 already played his move
        table.add_row([1, card_p1, show_visible_cards, score1, score2, deck_p1[i+1:], deck_p2[i:]])

        move_score = best_score(visible_cards, result_card=card_p2, current_player=2)
        steal_and_place_cards(visible_cards, card_p2, move_score, 2)  
        score2 += move_score
        show_visible_cards = '[' + " ".join("_" if x == 0 else str(x.safe_top_just_for_print()) for x in visible_cards) + ']'
        table.add_row([2, card_p2, show_visible_cards, score1, score2, deck_p1[i+1:], deck_p2[i+1:]])

    print(table)



