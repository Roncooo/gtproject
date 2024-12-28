# Nodo dell'albero
class Node:
    def __init__(self, cards_player1: set, cards_player2: set, current_player=1, delta_score=0,
                 visible_cards=[]*4, card_just_played=None, parent=None):
        self.current_player = current_player  # 1 or 2, it's who has to move next (not who has just played)
        self.delta_score = delta_score  # score 1 - score 2
        self.cards_player1 = cards_player1
        self.cards_player2 = cards_player2
        self.visible_cards = visible_cards  # [p1, c1, p2, c2] now 4 stacks
        self.card_just_played = card_just_played
        self.children = []
        self.parent = parent

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_path(self):
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]  # Inverti per avere il percorso dalla radice