import numpy as np
import random
# Useful to save some computation: this gives the answer in O(1)
IS_PRIME = (
True , True , False, True , False, 
True , False, False, False, True , 
False, True , False, False, False, 
True , False, True , False, False, 
False, True , False, False)

COMPOSITE_SCORE = 1
''' Score associated to a composite card. '''
PRIME_SCORE = 2
''' Score associated to a prime card. '''
HIGHEST_CARD = 25
LOWEST_CARD = 2
NUMBER_OF_CARDS = 24
NUM_CARDS_PER_PLAYER = int(NUMBER_OF_CARDS/2)

def is_prime(number: int):
    ''' returns `True` if `number` is prime, `False` otherwise. The implementation allows O(1) answer for all the positive integers in [2,25] and raises error for the other numbers. '''
    return IS_PRIME[number - 2]

def is_prime_index(index: int):
    ''' Tells if at position index of the visible cards there is a stack of prime cards (`True`) or composites (`False`). '''
    return index % 2 == 0

def card_score(card: int):
    '''returns `PRIME_SCORE` if the card is prime, otherwise `COMPOSITE_SCORE`. '''
    return PRIME_SCORE if is_prime(card) else COMPOSITE_SCORE

def place_card_index(card_to_place: int, player_number: int):
    ''' Tells on which index of the visible cards (in [0,3]) the player should place the card. '''
    return (player_number-1)*2+(0 if is_prime(card_to_place) else 1)

def my_prime_index(player: int):
    ''' returns the index of the visible cards (in [0,3]) where player finds his prime cards. '''
    return 0 if player==1 else 2
    
def my_composite_index(player: int):
    ''' returns the index of the visible cards (in [0,3]) where player finds his composite cards. '''
    return 1 if player==1 else 3

def opponent_prime_index(player: int):
    ''' returns the index of the visible cards (in [0,3]) where player finds the prime cards of his opponent. '''
    return 2 if player==1 else 0

def opponent_composite_index(player: int):
    ''' returns the index of the visible cards (in [0,3]) where player finds the composite cards of his opponent. '''
    return 3 if player==1 else 1

def card_score_by_index(card_index: int):
    ''' returns the score of a single card given its index. '''
    return PRIME_SCORE if is_prime_index(card_index) else COMPOSITE_SCORE

def whose_card_is_this(index: int):
    ''' returns the number of the player ([1,2]) that 'owns' the cards placed at `index`.'''
    return 1 if index<=1 else 2

def is_valid_operation(result: int, operand1: int, operand2: int):
    '''
    Tells if `operand1` and `operand2` can give `result` with the admitted operations.
    This function automatically checks all the possible order of operands.
    This function automatically checks that operands and result are not 0.
    '''
    
    if operand1==0 or operand2==0 or result==0:
        return False
    
    if result == operand1 + operand2:
        return True
    if result == operand1 - operand2 or result == operand2 - operand1:
        return True
    if result == operand1 * operand2:
        return True
    if result == operand1 / operand2:
        return True
    if result == operand2 / operand1:
        return True
    return False


def set_initial_players_deck(seed_value):
    deck = np.linspace(start=LOWEST_CARD, stop=HIGHEST_CARD, num=NUMBER_OF_CARDS, dtype='int')

    if seed_value != None:
        random.seed(seed_value)

    random.shuffle(deck)
    cards_p1 = set(deck[:NUM_CARDS_PER_PLAYER])
    cards_p2 = set(deck[NUM_CARDS_PER_PLAYER:])

    return cards_p1, cards_p2