from utilities.utils import NUM_CARDS_PER_PLAYER, set_initial_players_deck, place_card_index, shift_element
from utilities.policies import ALL_POLICIES
import numpy as np
from Primi_composti_1.score import best_score
from Primi_composti_1.play_primi_composti_1 import choose_card_by_policy_1
from utilities.simulations import sort_deck_according_to_policy

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

if __name__ == '__main__':
    
    seed = 31
    # here cards_p1 and cards_p2 are ndarrays used as in play_primi_composti_1
    cards_p1, cards_p2 = set_initial_players_deck(seed)
    visible_cards = np.zeros(4, dtype='int')
    human_Score = cpu_score = 0
    
    human_player = ask_player()
    cpu_policy = ask_cpu_policy()
    
    print("\nSTART\n")
    
    if human_player==1:
        
        cards_p1 = sort_deck_according_to_policy('asc', cards_p1) # this is just to make the gameplay easier, no impact on the logic
        cards_p2 = sort_deck_according_to_policy(cpu_policy, cards_p2)
        
        for i in range(NUM_CARDS_PER_PLAYER):
            
            print(f"The visible cards are {visible_cards}")
            # print(f"CPU cards are {cards_p2}")
            card = ask_card(cards_p1[i:])
            score = best_score(visible_cards, card)
            human_Score += score
            print(f"You made {score} points, you now have {human_Score} points")
            # move the card in the correct spot of your deck
            card_deck_index = np.where(cards_p1==card)[0]
            cards_p1 = shift_element(cards_p1, card_deck_index, i)
            # place the card on the table
            card_placement_index = place_card_index(card, 1)
            visible_cards[card_placement_index] = card
            print(f"Now the visible cards are {visible_cards} and your deck {cards_p1[i+1:]}")
            
            cards_p2 = choose_card_by_policy_1(cards_p2, cards_p1, cpu_policy, i, i+1, visible_cards, 2)
            card = cards_p2[i]
            score = best_score(visible_cards, card)
            cpu_score += score
            print(f"The CPU chose card {card} and made {score} points, now it has {cpu_score} points")            
            # place the card on the table
            card_placement_index = place_card_index(card, 2)
            visible_cards[card_placement_index] = card
            # print(f"Now the visible cards are {visible_cards}")
        
        print("\nGAME OVER\n")
        print(f"Results: your score {human_Score}, cpu score {cpu_score}")
        if human_Score>cpu_score:
            print("Congratulations, you won!!!")
        elif human_Score == cpu_score:
            print("That's a tie, try again")
        else:
            print("Not your day, but champions are forged in the fire of failure. Rise, train, and reclaim your glory!")
    
    # human player chose to be player 2  
    else:
        
        cards_p1 = sort_deck_according_to_policy(cpu_policy, cards_p1)
        cards_p2 = sort_deck_according_to_policy('asc', cards_p2) # this is just to make the gameplay easier, no impact on the logic
        
        for i in range(NUM_CARDS_PER_PLAYER):
            
            cards_p1 = choose_card_by_policy_1(cards_p1, cards_p2, cpu_policy, i, i, visible_cards, 1)
            card = cards_p1[i]
            score = best_score(visible_cards, card)
            cpu_score += score
            print(f"The CPU chose card {card} and made {score} points, now it has {cpu_score} points")            
            # place the card on the table
            card_placement_index = place_card_index(card, 1)
            visible_cards[card_placement_index] = card
            # print(f"Now the visible cards are {visible_cards}")

            print(f"The visible cards are {visible_cards}")
            # print(f"CPU cards are {cards_p1}")
            card = ask_card(cards_p2[i:])
            score = best_score(visible_cards, card)
            human_Score += score
            print(f"You made {score} points, you now have {human_Score} points")
            # move the card in the correct spot of your deck
            card_deck_index = np.where(cards_p2==card)[0]
            cards_p2 = shift_element(cards_p2, card_deck_index, i)
            # place the card on the table
            card_placement_index = place_card_index(card, 2)
            visible_cards[card_placement_index] = card
            print(f"Now the visible cards are {visible_cards} and your deck {cards_p2[i+1:]}")
        
        print("\nGAME OVER\n")
        print(f"Results: your score {human_Score}, cpu score {cpu_score}")
        if human_Score>cpu_score:
            print("Congratulations, you won!!!")
        elif human_Score == cpu_score:
            print("That's a tie, try again")
        else:
            print("Not your day, but champions are forged in the fire of failure. Rise, train, and reclaim your glory!")

