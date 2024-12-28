from primi_composti_1.alphabeta_primi_composti_1 import *
from prettytable import PrettyTable 

if __name__ == "__main__":

    seed = 31
    depths = [6, 6, 12]  # Profondità per 4 turni
    final_score, final_node, all_paths = match(seed, depths)

    # Print the path
    table = PrettyTable()
    table.field_names = ["Player", "Played card", "Gameboard", "Delta", "Deck P1", "Deck P2"]
    table.border = False
    # Set all columns to left-align
    for column in table.field_names:
        table.align[column] = "l"
    for i, path in enumerate(all_paths):
        for node in path[1:]:
            table.add_row([node.parent.current_player, node.card_just_played, node.visible_cards, node.delta_score, node.cards_player1, node.cards_player2])
    print(table)
