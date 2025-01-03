from utilities.utils import PRIME_SCORE, COMPOSITE_SCORE

def current_scores(visible_cards):
    '''In the version 2 of the game, scores rely on the number of cards in the stacks on the table. 
    Each move may change both scores so it's not enough to sum the scores made by one player to get his final score.'''
    score_p1 = PRIME_SCORE * visible_cards[0].size() + COMPOSITE_SCORE * visible_cards[1].size()
    score_p2 = PRIME_SCORE * visible_cards[2].size() + COMPOSITE_SCORE * visible_cards[3].size()
    return score_p1, score_p2