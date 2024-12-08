
import random
import time

# Costanti
PRIMI = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73}
COMPOSTI = set(range(2, 74)) - PRIMI
ALL_NUMBERS = (2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25)
IS_PRIME = (True,True,False,True,False,True,False,False,False,True,False,True,False,False,False,True,False,True,False,False,False,True,False,False)
def is_prime(number):
    return IS_PRIME[number-2]
composite_score = 1
prime_score = 2

# Stupid policies, the player does not look at the cards on the table to do his move, there is no thought mid game
predetermined_policies = ('asc', 'desc', 'rand')
# each choice may change on the base of what's on the table
dynamic_policies = ('greedy_desc', 'greedy_asc')
all_policies = predetermined_policies + dynamic_policies

def is_prime_index(index):
    '''Tells if at position index of the gameboard there are prime cards (True) or composites (False)'''
    return index%2==0

def card_score(card):
    return prime_score if is_prime(card) else composite_score

def is_valid_operation(result, operand1, operand2):
    '''
    Tells if `operand1` and `operand2` can give `result` with the admitted operations.
    This function automatically checks all the possible order of operands.
    '''
    if result==operand1+operand2:
        return True
    if result==operand1-operand2 or result==operand2-operand1:
        return True
    if result==operand1*operand2:
        return True
    if operand2!=0 and result==operand1/operand2:
        return True
    if operand1!=0 and result==operand2/operand1:
        return True
    return False

# Nodo dell'albero
class Node:
    def __init__(self, cards_player1: set, cards_player2: set, current_player=1, delta_score=0, visible_cards=[0,0,0,0], card_just_played = None, parent=None):
        self.current_player = current_player # 1 or 2
        self.delta_score = delta_score # score 1 - score 2
        self.cards_player1 = cards_player1
        self.cards_player2 = cards_player2
        self.visible_cards = visible_cards # [p1, c1, p2, c2]
        self.card_just_played = card_just_played
        self.children = []
        self.parent = parent
        self.best_move = None
        self.best_move_score = None

    def add_child(self, child_node):
        self.children.append(child_node)

def best_score(visible_cards, result_card):    
    '''
    Gives the best score you can obtain by combining 2 cards among `visible_cards` to obtain `result`.
    Tries all possible combinations of operands and operations.
    Stops if the theoretical best score for that particular position is detected or when all possibilities are calculated.
    '''
    max_operation_score = 2*prime_score
    placed_card_score = card_score(result_card)
    best_operation_score = 0 # best score found so far
    
    # this nested loop chooses the couples of operands
    # the order does not matter since is_valid_operation deals with it
    for i in range(4):
        # if you uncomment the following if clause, you remove the possibility to form operations with 
        # the card that the player has just placed. In other words, by commenting the if we allow a#x=x
        if visible_cards[i] == result_card:
            continue
        
        if visible_cards[i] == 0: # no card placed in position i
            continue
        for j in range(i+1, 4):
            if visible_cards[j] == 0: # no card placed in position j
                continue
            
            if not is_valid_operation(result=result_card, operand1=visible_cards[i], operand2=visible_cards[j]):
                continue
            
            score_card_i = prime_score if is_prime_index(i) else composite_score
            score_card_j = prime_score if is_prime_index(j) else composite_score
            current_operation_score = score_card_i + score_card_j
            
            if current_operation_score > best_operation_score:
                best_operation_score = current_operation_score
            
            if max_operation_score == best_operation_score:
                return best_operation_score + placed_card_score # early stop
    
    # if no valid operation is found, it is just placed_card_score so 1 or 2
    return best_operation_score + placed_card_score


def evaluate(node: Node):
    if node.parent == None:
        return 0
    if node.current_player == 1:
        return evaluate(node.parent) - best_score(node.parent.visible_cards, node.card_just_played)
    else:
        return evaluate(node.parent) + best_score(node.parent.visible_cards, node.card_just_played)

def minimax(position, depth, alpha, beta, maximizingPlayer):

    if depth == 0: # or game over in position
        return evaluate(position)

    if maximizingPlayer:
        maxEval = float('-inf')
        for child in position.children:
            eval = minimax(child, depth - 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval = float('+inf')
        for child in position.children:
            eval = minimax(child, depth - 1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def place_card(visible_cards, new_card, player):
    new_gameboard = visible_cards[:]
    if player==1:
        if is_prime(new_card):
            new_gameboard[0] = new_card
        else: 
            new_gameboard[1] = new_card
    else:
        if is_prime(new_card):
            new_gameboard[2] = new_card
        else: 
            new_gameboard[3] = new_card
    return new_gameboard

def generate_tree(cards_p1, cards_p2, depth):
    root = Node(cards_p1, cards_p2)
    def expand(node: Node, depth):
        if depth==0:
            return
        if node.current_player == 1:
            for c in node.cards_player1:
                this_move_score = best_score(node.visible_cards, c)
                new_delta_score = node.delta_score + this_move_score
                cards_player1_copy = node.cards_player1.copy()
                cards_player1_copy.remove(c)
                new_node = Node(cards_player1_copy, node.cards_player2, 
                                current_player=2, 
                                delta_score=new_delta_score,
                                visible_cards=place_card(node.visible_cards, c, 1),
                                card_just_played=c,
                                parent=node,
                                )
                node.add_child(new_node)
                expand(new_node, depth-1)
        else:
            for c in node.cards_player2:
                this_move_score = best_score(node.visible_cards, c)
                new_delta_score = node.delta_score - this_move_score
                cards_player2_copy = node.cards_player2.copy()
                cards_player2_copy.remove(c)
                new_node = Node(node.cards_player1, cards_player2_copy, 
                                current_player=1, 
                                delta_score=new_delta_score,
                                visible_cards=place_card(node.visible_cards, c, 2),
                                card_just_played=c,
                                parent=node,
                                )
                node.add_child(new_node)
                expand(new_node, depth-1)
    expand(root, depth)
    return root
    
    

    
def match(depth):
    deck = [i for i in range(2,25)]
    random.shuffle(deck)
    cards_p1 = set(deck[:12])
    cards_p2 = set(deck[12:])
    root = generate_tree(cards_p1, cards_p2, depth)
    max = minimax(root, depth, float('-inf'), float('+inf'), True)
    # ora bisognerebbe trovare la foglia che ha portato a questo max e usarla come radice per andare avanti
    # volendo ad ogni iterazione si può aumentare la depth perché ci sono sempre meno carte e quindi l'albero è meno largo
    # print(max)
    return max

if __name__ == "__main__":
    depth_vals = [3,4,5]
    win1 = [0]*len(depth_vals)
    avg_time = [0]*len(depth_vals)
    iterations = 100
    for i, d in enumerate(depth_vals):
        win=0
        for _ in range(iterations):
            start = time.time()
            if match(d) > 0:
                win+=1
            end = time.time()
            avg_time[i]+=end-start
        win1[i]=win
        avg_time[i]/=iterations
    
    print("depths:",depth_vals)
    print("winrate p1", [x / iterations for x in win1])
    print("average time", avg_time)
            