from utilities.utils import NUM_CARDS_PER_PLAYER, set_initial_players_deck, show_visible_cards, shift_element
from utilities.policies import ALL_POLICIES
import numpy as np
from Primi_composti_2.play_primi_composti_2 import choose_card_by_policy_2, steal_and_place_cards, current_scores, best_score_2
from utilities.simulations import sort_deck_according_to_policy
from utilities.Stack import Stack

def ask_player():
    ''' Asks the user the number of player he wants to play as. Returns 1 or 2 according to user answer. '''
    prompt = "Do you want to play as player 1? (y/n) "
    valid_positive_answers = ('yes', 'y')
    valid_negative_answers = ('no', 'n')
    while True:
        ans = input(prompt)
        if ans.lower() in valid_positive_answers:
            return 1
        if ans.lower() in valid_negative_answers:
            return 2
        print(f"{ans} is not a valid answer, please retry")

def ask_cpu_policy():
    ''' Asks the user the policy he wants to play against. Returns the name of the policy. '''
    prompt = f"Which policy do you want the CPU to play? Choose among the following:\n" \
             + "\n".join(f"- {p}" for p in ALL_POLICIES) + "\n"
    while True:
        cpu_policy = input(prompt)
        if cpu_policy.lower() in ALL_POLICIES:
            return cpu_policy.lower()
        print(f"{cpu_policy} is not a valid policy, please try again.")
    
def ask_card(human_deck):
    ''' Asks the user which card he wants to play among those he has in hand. Returns the value of the card. '''
    prompt = f"Which card do you want to play? Choose among {human_deck} "
    while True:
        card = input(prompt)
        try:
            if int(card) in human_deck:
                return int(card)
            print(f"{card} is not a valid card in you deck, please try again.")
        except:
            print(f"{card} is not a valid card in you deck, please try again.")


def turn(player_type, current_player_deck, visible_cards, player_starting_index, opponent_starting_index = None , cpu_policy=None, opponent_deck=None, player_num=1):
    """Handles a single turn for a player: human or cpu.
    """

    if player_type == 'human':

        print(f"The visible cards are {show_visible_cards(visible_cards)}")
        # print(f"CPU cards are {cards_p1}")
        card = ask_card(current_player_deck[player_starting_index:])
        # move the card in the correct spot of your deck
        card_deck_index = np.where(current_player_deck == card)[0]
        current_player_deck = shift_element(current_player_deck, card_deck_index, player_starting_index)

    else:
        current_player_deck = choose_card_by_policy_2(current_player_deck, opponent_deck, cpu_policy, player_starting_index, opponent_starting_index, visible_cards, player_num)
        card = current_player_deck[player_starting_index]
        print(f"The CPU chose card {card}")


    # place the card on the table
    move_score = best_score_2(visible_cards, card, current_player=player_num)
    steal_and_place_cards(visible_cards, card, move_score, player=player_num)

    return current_player_deck, visible_cards

if __name__ == '__main__':
    
    seed = 31
    # here cards_p1 and cards_p2 are ndarrays used as in play_primi_composti_1
    cards_p1, cards_p2 = set_initial_players_deck(seed)
    visible_cards = [Stack(), Stack(), Stack(), Stack()]
    human_score = cpu_score = 0
    
    human_player = ask_player()
    cpu_policy = ask_cpu_policy()
    
    print("\nSTART\n")
    
    if human_player==1:
        
        cards_p1 = sort_deck_according_to_policy('asc', cards_p1) # this is just to make the gameplay easier, no impact on the logic
        cards_p2 = sort_deck_according_to_policy(cpu_policy, cards_p2)
        
        for i in range(NUM_CARDS_PER_PLAYER):

            # Human turn
            cards_p1, visible_cards = turn('human', cards_p1, visible_cards, i, i, player_num=1)
            human_score, cpu_score = current_scores(visible_cards)
            print(f"Now the visible cards are {show_visible_cards(visible_cards)} and your deck {cards_p1[i + 1:]} ")
            print(f"Scores are now: human {human_score} - CPU {cpu_score} \n")

            # CPU turn
            cards_p2, visible_cards = turn('cpu', cards_p2, visible_cards, i, i+1,  cpu_policy=cpu_policy , opponent_deck=cards_p1,  player_num=2)
            human_score, cpu_score = current_scores(visible_cards)
            print(f"Scores are now: human {human_score} - CPU {cpu_score} \n")

    # human player chose to be player 2  
    else:
        
        cards_p1 = sort_deck_according_to_policy(cpu_policy, cards_p1)
        cards_p2 = sort_deck_according_to_policy('asc', cards_p2) # this is just to make the gameplay easier, no impact on the logic
        
        for i in range(NUM_CARDS_PER_PLAYER):

            # CPU turn
            cards_p1, visible_cards = turn('cpu', cards_p1, visible_cards, i, i, cpu_policy=cpu_policy, opponent_deck=cards_p2, player_num=1)
            human_score, cpu_score = current_scores(visible_cards)
            print(f"Scores are now: human {human_score} - CPU {cpu_score}\n")

            # Human turn
            cards_p2, visible_cards = turn('human', cards_p2, visible_cards, i, player_num=2)
            human_score, cpu_score = current_scores(visible_cards)
            print(f"Now the visible cards are {show_visible_cards(visible_cards)} and your deck {cards_p2[i + 1:]} ")
            print(f"Scores are now: human {human_score} - CPU {cpu_score} \n")

        
    print("\nGAME OVER\n")
    print(f"Results: your score {human_score}, cpu score {cpu_score}")
    if human_score>cpu_score:
        print("Congratulations, you won!!!")
    elif human_score == cpu_score:
        print("That's a tie, try again")
    else:
        print("Not your day, but champions are forged in the fire of failure. Rise, train, and reclaim your glory!")

