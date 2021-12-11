from player import Player
from auto_play import auto_play
from board import Board
import constants
import numpy as np
import matplotlib.pyplot as plt

# Dado indiviudos del hof, c/u juega contra random y contra AA pesos fijos y se grafican resultados
def hof_tournament(hof, n_matches, print_matches, do_minimax):
    re_index_individual = 0
    matchs_against_random = {}
    matchs_against_aa = {}
    for individual in hof:
        print("individual hof:")
        print(individual[0][0])
        # Re identifico los individuos (ids repetidos)
        individual[0] = (individual[0][0], re_index_individual)
        re_index_individual += 1
        
        player1 = Player([-0.3245326346849934, 0.1693042050134686, 0.16953670371976523, 0.22783655225690969, 0.22793136193535615, 0.3166528358145293, 0.3143485967442448, 0.35530630208678404, 0.3464082778644509], constants.PLAYER_AA)
        player2 = Player(individual[0][0], constants.PLAYER_AE)
        board = Board()
        
        match_results = []
        for i in range(500): # partidas contra random
            board.generate_random_board()
            result, ae_board_attrs_history = auto_play(board, player1, player2, print_matches, False, print_matches, True, do_minimax)
            if result[0] == constants.PLAYER_AE:
                match_results.append(result)
        matchs_against_random[individual[0][1]] = match_results
        
        match_results = []
        for i in range(500): # partidas contra aa
            board.generate_random_board()
            result, ae_board_attrs_history = auto_play(board, player1, player2, print_matches, False, print_matches, False, do_minimax)
            if result[0] == constants.PLAYER_AE:
                match_results.append(result)
        matchs_against_aa[individual[0][1]] = match_results

    
    # Ploteo Resultados
    data = [[len(matchs_against_random[0]),len(matchs_against_random[1]),len(matchs_against_random[2]),len(matchs_against_random[3]),len(matchs_against_random[4])],
            [len(matchs_against_aa[0]),len(matchs_against_aa[1]),len(matchs_against_aa[2]),len(matchs_against_aa[3]),len(matchs_against_aa[4])]]

    avgRandom=(len(matchs_against_random[0])+len(matchs_against_random[1])+len(matchs_against_random[2])+len(matchs_against_random[3])+len(matchs_against_random[4]))/5
    avgAA=(len(matchs_against_aa[0])+len(matchs_against_aa[1])+len(matchs_against_aa[2])+len(matchs_against_aa[3])+len(matchs_against_aa[4]))/5
    
    fig, ax = plt.subplots()
    index = np.arange(5)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, data[0], bar_width,
    alpha=opacity,
    color='b',
    label='VS Random')

    rects2 = plt.bar(index + bar_width, data[1], bar_width,
    alpha=opacity,
    color='g',
    label='VS AA')

    plt.xlabel('Individuos Hall of Fame')
    plt.ylabel('Partidas Ganadas')
    plt.title('Partidas ganadas con pesos fijos \n AVG. Wins Vs.Random: ' + str(avgRandom) + ' / AVG. Wins Vs.AA: ' + str(avgAA))
    plt.xticks(index + bar_width, ('Ind 0', 'Ind 1', 'Ind 2', 'Ind 3', 'Ind 4'))
    plt.legend()

    plt.tight_layout()
    plt.show()
    
                
            
            