PREDETERMINED_POLICIES = ('asc', 'desc', 'rand')
''' Simple policies: strategies where the player does not look at the cards on the table to do his move, there is no thought mid game.

    `asc` consists in playing always the lowest card in hand
    
    `desc` consists in playing always the highest card in hand
    
    `rand` consists in playing completely at random
    '''

DYNAMIC_POLICIES = ('greedy_asc', 'greedy_desc')
''' Policies that involve also the current state of the table (visible cards) and require some mid game logic.

    `greedy_asc` consists in playing always, among the cards that give the maximum amount of points in that move, the one with lowest value

    `greedy_desc` consists in playing always, among the cards that give the maximum amount of points in that move, the one with highest value
'''

ALL_POLICIES = PREDETERMINED_POLICIES + DYNAMIC_POLICIES
''' Contains all the implemented policies that can be played by a player in a simulation '''