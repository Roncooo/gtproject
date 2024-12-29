PREDETERMINED_POLICIES = ('asc', 'desc', 'rand')
''' Simple policies: strategies where the player does not look at the cards on the table to do his move, there is no thought mid game.

    `asc` consists in playing always the lowest card in hand
    
    `desc` consists in playing always the highest card in hand
    
    `rand` consists in playing completely at random
    '''

DYNAMIC_POLICIES = ('greedy_asc', 'greedy_desc', 'greedy_rand')
''' Policies that involve also the current state of the table (visible cards) and require some mid game logic.

    `greedy_asc` consists in playing always, among the cards that give the maximum amount of points in that move, the one with lowest value

    `greedy_desc` consists in playing always, among the cards that give the maximum amount of points in that move, the one with highest value
    
    `greedy_rand` consists in playing a random card among those that give the maximum amount of points in that move
        
'''

SIMPLE_POLICIES = PREDETERMINED_POLICIES + DYNAMIC_POLICIES
''' Contains all the implemented policies that can be played by a player in a simulation '''

MINIMAX_POLICIES = ('minimax_2', 'minimax_3', 'minimax_4', 'minimax_5', 'minimax_6')
'''
    minimax policies only have depths that are one digit values and so i can take the last char and convert it to int
    
    `minimax_n` consists in playing the best card solving the tree with the alpha-beta pruning algorithm by looking at n levels into the game
'''

ALL_POLICIES = SIMPLE_POLICIES + MINIMAX_POLICIES