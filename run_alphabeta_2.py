from primi_composti_2.alphabeta_primi_composti_2 import *
from prettytable import PrettyTable 

if __name__ == "__main__":

    seed = 31
    depths = [4, 4, 6, 8]  # Profondità per 4 turni
    final_score, final_node, all_paths = match(seed, depths)

    # Print the path
    table = PrettyTable()
    table.field_names = ["Player", "Played card", "Gameboard", "Delta", "Deck P1", "Deck P2"]
    table.border = False
    # Set all columns to left-align
    for column in table.field_names:
        table.align[column] = "l"
    for i, path in enumerate(all_paths):
        print(f"Path {i+1}:")
        for node in path[1:]:
            table.add_row([node.parent.current_player, node.card_just_played, [node.visible_cards[i].safe_top_just_for_print() for i in range(0,4)], node.delta_score, node.cards_player1, node.cards_player2])
    print(table)
    
