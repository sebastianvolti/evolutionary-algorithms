from player import Player
from board import Board
from auto_play import auto_play
import constants
first_limit_movements = 20
second_limit_movements = 40

def init_game(individual_coef, n_matches, p_mutation, print_matches, print_movements, full_random, do_minimax):
    board = Board()
    results = []
    ae_board_attrs_history_list = []
    if print_movements:
        print("==Init Game==")
    
    cont_aa_wins = 0
    cont_ae_wins = 0
    
    for match in range(n_matches):
        if print_matches:
            print("=====================================GAME " + str(match+1) + "=====================================")
        select_board(match, board)
        player1 = Player([-0.3245326346849934, 0.1693042050134686, 0.16953670371976523, 0.22783655225690969, 0.22793136193535615, 0.3166528358145293, 0.3143485967442448, 0.35530630208678404, 0.3464082778644509], constants.PLAYER_AA)
        player2 = Player(individual_coef, constants.PLAYER_AE)
        result, ae_board_attrs_history = auto_play(board, player1, player2, print_matches, print_movements, print_matches, full_random, do_minimax)
        if result[0] == 0:
            cont_aa_wins += 1
        elif result[0] == 1:
            cont_ae_wins += 1
        results.append(result) 
        if (ae_board_attrs_history != []):
            ae_board_attrs_history_list.append(ae_board_attrs_history)

    if print_movements:   
        print("  AA player won: " + str(cont_aa_wins) + " / AE player won: " + str(cont_ae_wins) + "\n  (" + str(individual_coef) + ")\n")
    return calculateFitness(results, n_matches), ae_board_attrs_history_list

# Si gana antes de 10 movs: 10 puntos
# Si gana antes de 50 movs: 7.5 puntos
# Si gana despues de 50 movs: 5 puntos
def calculateFitness(results, n_matches):
    fitness = 0
    for (winner, movements) in results:
        if (winner == 1):
            if (movements <= first_limit_movements): # si gano en 10 movs, suma 10
                fitness += 10
            else:
                if (movements >= second_limit_movements): # si gano en mas de 20 movs, solo sumo 5
                    fitness += 5
                else:
                    round_fitness = 10 - ((movements-20)*0.75) # entre 10 y 20 sumo en relacion a la cantidad de movimientos
                    fitness += round_fitness
    return fitness/(10*n_matches)

# Para las primeras 5 partidas, se devuelven tableros pre armados, para las ultimas 5 partidas tableros aleatorios
def select_board(iter_num, board):
    if iter_num == 0:
        board.generate_default_board_0()
    elif iter_num == 1:
        board.generate_default_board_1()
    elif iter_num == 2:
        board.generate_default_board_2()
    elif iter_num == 3:
        board.generate_default_board_3()
    elif iter_num == 4:
        board.generate_default_board_4()
    elif iter_num == 5:
        board.generate_default_board_5()
    elif iter_num == 6:
        board.generate_default_board_6()
    elif iter_num == 7:
        board.generate_default_board_7()
    elif iter_num == 8:
        board.generate_default_board_8()
    elif iter_num == 9:
        board.generate_default_board_9()
    else:
        board.generate_random_board()
    