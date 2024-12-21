import itertools
from graphviz import Digraph
import numpy as np
import sympy as sp
import random
import itertools
import operator
from collections import deque


# Costanti
PRIMI = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73}
COMPOSTI = set(range(2, 74)) - PRIMI

# Funzione per determinare il numero di STEP da fare sul tabellone di gioco (Nota: c'è sempre un solo risultato, ossia il migliore
def calcola_step(card, visible_cards):
    if card in PRIMI:
        primi = True
    else:
        primi = False

    for visible_card_1, visible_card_2 in itertools.combinations(visible_cards, 2): # tutte le coppie nelle 4 carte visibili

        # in queste posizioni non ci sono carte
        if visible_card_1 is None or visible_card_2 is None:
            continue

        for op in ('+', '-', '*', '/'):
            try:
                if eval(f"{visible_card_1} {op} {visible_card_2}") == card:
                    if primi:
                        if visible_card_1 in PRIMI and visible_card_2 in PRIMI:
                            return 6
                        else:
                            return 5
                    else:
                        if visible_card_1 in PRIMI or visible_card_2 in PRIMI:
                            return 4
                        else:
                            return 3
            except ZeroDivisionError:
                continue
    return 2 if primi else 1


# Nodo dell'albero
class Node:
    def __init__(self, positions, cards_player1, cards_player2, visible_cards, current_player):
        self.positions = positions # posizione nel tabellone dei giocatori (pay-off finale)
        self.cards_player1 = cards_player1
        self.cards_player2 = cards_player2
        self.visible_cards = visible_cards # [p1, c1, p2, c2]
        self.current_player = current_player
        self.children = []
        self.best_move = None
        self.payoff = None

    def add_child(self, child_node):
        self.children.append(child_node)

# Genera l'albero delle mosse
def genera_albero(positions, cards_player1, cards_player2, visible_cards, current_player):

    # radice dell'albero. Il current player è chi ha un due.
    root = Node(positions, cards_player1, cards_player2, visible_cards, current_player)

    def expand(node):

        # prende le carte del giocatore corrente
        current_cards = node.cards_player1 if node.current_player == 0 else node.cards_player2

        # Se non ci sono carte da giocare, siamo in un nodo terminale
        if not current_cards:
            return

        # Genera un figlio per ogni mossa che può fare il giocatore corrente (può fare tante mosse quante carte ha in mano in questa versione)
        for card in current_cards:

            new_positions = list(node.positions)
            step = calcola_step(card, node.visible_cards)
            # Viene calcolata la posizione del giocatore corrente aggiungendo il numero di passi da fare per la carta giocata.
            new_positions[node.current_player] += step

            # Aggiorna la mano di gioco del figlio che non avrà la carta giocata
            new_cards_p1 = node.cards_player1 - {card} if node.current_player == 0 else node.cards_player1
            new_cards_p2 = node.cards_player2 - {card} if node.current_player == 1 else node.cards_player2

            # Aggiorna visible_cards in base al tipo di carta giocata e al giocatore corrente
            new_visible_cards = list(node.visible_cards)  # Copia delle carte visibili
            if node.current_player == 0:  # Giocatore 1
                if card in PRIMI:
                    new_visible_cards[0] = card  # Aggiorna P1
                else:
                    new_visible_cards[1] = card  # Aggiorna C1
            else:  # Giocatore 2
                if card in PRIMI:
                    new_visible_cards[2] = card  # Aggiorna P2
                else:
                    new_visible_cards[3] = card  # Aggiorna C2

            # Cambia giocatore
            next_player = 1 - node.current_player

            # Crea un nuovo nodo
            child = Node(new_positions, new_cards_p1, new_cards_p2, new_visible_cards, next_player)
            node.children.append(child)

            # Espande ricorsivamente
            expand(child)

    #tutto i nodi fatti nel for vengono messi nella radice
    expand(root)
    return root

def crea_nodo(positions, cards_player1, cards_player2, visible_cards, current_player):
    return Node(positions, cards_player1, cards_player2, visible_cards, current_player)

def aggiungi_figli(node, lista_figli):
    for child in lista_figli:
        node.add_child(child)


def backward_induction(node):
    # Nodo terminale: il payoff è determinato dalla posizione attuale
    if not node.children:
        node.payoff = tuple(node.positions)
        return node

    # Determina il giocatore corrente
    player = node.current_player

    # Caso Giocatore 2: sa quello che giocarà giocatore 1
    if player == 1:
        best_child = None
        best_payoff = float('-inf')
        for child in node.children:
            child_node = backward_induction(child)
            # Giocatore 2 cerca di massimizzare il proprio payoff
            if best_child is None or child_node.payoff[1] > best_payoff:
                best_child = child_node
                best_payoff = child_node.payoff[1]
        node.payoff = best_child.payoff
        node.best_move = best_child
        return node

    # Caso Giocatore 1: sa quello che giocarà giocatore 2
    if player == 0:
        best_child = None
        best_payoff = float('-inf')
        for child in node.children:
            child_node = backward_induction(child)
            # Giocatore 1 cerca di massimizzare il proprio payoff, considerando la reazione di Giocatore 2
            if best_child is None or child_node.payoff[0] > best_payoff:
                best_child = child_node
                best_payoff = child_node.payoff[0]
        node.payoff = best_child.payoff
        node.best_move = best_child
        return node


if __name__ == "__main__":
    # Crea la radice
    radice = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)

    # Crea i figli della radice
    figlio1 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 1)
    figlio2 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 1)
    figlio3 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 1)

    # Aggiungi figli alla radice
    aggiungi_figli(radice, [figlio1, figlio2])

    # Crea figli di figlio1
    figlio1_1 = crea_nodo([9, 1], {0, 0}, {0, 0}, [None, None, None, None], 0)
    figlio2_1 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)

    figlio1_2 = crea_nodo([5, 5], {0, 0}, {0, 0}, [None, None, None, None], 0)
    figlio2_2 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)

    figlio1_3 = crea_nodo([2, 8], {0, 0}, {0, 0}, [None, None, None, None], 0)
    figlio2_3 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)

    # Aggiungi figli a figlio1
    aggiungi_figli(figlio1, [figlio1_1, figlio2_1])

    # Aggiungi figli a figlio1
    aggiungi_figli(figlio2, [figlio1_2, figlio2_2])

    # Aggiungi figli a figlio1
    aggiungi_figli(figlio3, [figlio1_3, figlio2_3])

    # Risolve l'albero con backward induction
    print("Esecuzione di backward induction...")
    result = backward_induction(radice)
    print("Backward induction completata!")

    # Stampa il risultato finale
    print("Payoff finale:", result.payoff)
    print("Mossa iniziale ottimale (stato successivo):", result.best_move)

    radice2 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)

    # Crea i figli della radice
    figlio1 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 1)
    figlio2 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 1)

    # Aggiungi figli alla radice
    aggiungi_figli(radice, [figlio1, figlio2])


    figlio1_1 = crea_nodo([1, 5], {0, 0}, {0, 0}, [None, None, None, None], 1)
    figlio2_1 = crea_nodo([3, 0], {0, 0}, {0, 0}, [None, None, None, None], 1)


    aggiungi_figli(figlio1, [figlio1_1, figlio2_1])

    figlio1_2 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)
    figlio2_2 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)

    aggiungi_figli(figlio2, [figlio1_2, figlio2_2])

    figlio1_21 = crea_nodo([4, 1], {0, 0}, {0, 0}, [None, None, None, None], 0)
    figlio2_21 = crea_nodo([0, 2], {0, 0}, {0, 0}, [None, None, None, None], 0)

    aggiungi_figli(figlio1_2, [figlio1_21, figlio2_21])

    figlio1_22 = crea_nodo([0, 2], {0, 0}, {0, 0}, [None, None, None, None], 0)
    figlio2_22 = crea_nodo([4, 1], {0, 0}, {0, 0}, [None, None, None, None], 0)

    aggiungi_figli(figlio2_2, [figlio1_22, figlio2_22])


    # Risolve l'albero con backward induction
    print("Esecuzione di backward induction...")
    result = backward_induction(radice2)
    print("Backward induction completata!")

    # Stampa il risultato finale
    print("Payoff finale:", result.payoff)
    print("Mossa iniziale ottimale (stato successivo):", result.best_move)

    radice3 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)

    # Crea i figli della radice
    figlio1 = crea_nodo([2, 0], {0, 0}, {0, 0}, [None, None, None, None], 1)
    figlio2 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 1)

    # Aggiungi figli alla radice
    aggiungi_figli(radice3, [figlio1, figlio2])

    figlio1_2 = crea_nodo([1, 1], {0, 0}, {0, 0}, [None, None, None, None], 0)
    figlio2_2 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)

    aggiungi_figli(figlio2, [figlio1_2, figlio2_2])

    figlio1_21 = crea_nodo([5, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)
    figlio1_22 = crea_nodo([3, 2], {0, 0}, {0, 0}, [None, None, None, None], 0)

    aggiungi_figli(figlio2_2, [figlio1_21, figlio2_22])


    # Risolve l'albero con backward induction
    print("Esecuzione di backward induction...")
    result = backward_induction(radice3)
    print("Backward induction completata!")

    # Stampa il risultato finale
    print("Payoff finale:", result.payoff)

    # Crea la radice
    radice4 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)

    # Crea i figli della radice
    figlio1 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 1)
    figlio2 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 1)

    # Aggiungi figli alla radice
    aggiungi_figli(radice4, [figlio1, figlio2])

    # Crea figli di figlio1
    figlio1_1 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)
    figlio2_1 = crea_nodo([3, -3], {0, 0}, {0, 0}, [None, None, None, None], 0)

    aggiungi_figli(figlio1, [figlio1_1, figlio2_1])

    figlio1_11 = crea_nodo([9, -9], {0, 0}, {0, 0}, [None, None, None, None], 0)
    figlio2_11 = crea_nodo([6, -1], {0, 0}, {0, 0}, [None, None, None, None], 0)

    aggiungi_figli(figlio1_1, [figlio1_11, figlio2_11])

    figlio1_2 = crea_nodo([0, 0], {0, 0}, {0, 0}, [None, None, None, None], 0)
    figlio2_2 = crea_nodo([2, 3], {0, 0}, {0, 0}, [None, None, None, None], 0)

    aggiungi_figli(figlio2, [figlio1_2, figlio2_2])


    figlio1_21 = crea_nodo([6, 9], {0, 0}, {0, 0}, [None, None, None, None], 0)
    figlio2_21 = crea_nodo([4, 11], {0, 0}, {0, 0}, [None, None, None, None], 0)

    aggiungi_figli(figlio1_2, [figlio1_21, figlio2_21])

    # Risolve l'albero con backward induction
    print("Esecuzioneee di backward induction...")
    result = backward_induction(radice4)
    print("Backward induction completata!")

    # Stampa il risultato finale
    print("Payoff finale:", result.payoff)

'''


'''