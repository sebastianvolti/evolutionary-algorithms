import time
import train_aa
import constants
from board import Board
from player import Player

# Dado un objeto board y dos objetos player, simula una partida entre ellos
def auto_play(board, player1, player2, print_boards, print_move_values, print_winner, full_random_player, do_minimax):
    if print_boards:
        print("----NEW GAME----\n")
    count_move = 0
    aa_board_attrs_history = []
    ae_board_attrs_history = []
    turn = 1
    if print_boards:
        board.pp_board()
    while board.is_final_board(board.positions_AA, board.positions_AE)['final'] == False:
        if print_move_values:
            board.pp_board()
            print("\n =================TURN " +str(turn) + "=================\n")
            turn += 1
        if (count_move % 2 == 0):
            if full_random_player:
                [initial_position, final_position], board_attrs = player1.decide_best_movement_aa(board, print_move_values, count_move % 2 == 0) # Siempre random
            else:    
                [initial_position, final_position], board_attrs = player1.decide_best_movement_aa(board, print_move_values, count_move % 5 == 0)
            valid_movement = board.move_player(initial_position, final_position, player1.player_id)
            if (board_attrs != []):
                aa_board_attrs_history.append(board_attrs)
        else:
            [initial_position, final_position], board_attrs = player2.decide_best_movement_ae(board, print_move_values, count_move % 5 == 0, do_minimax)
            valid_movement = board.move_player(initial_position, final_position, player2.player_id)
            if (board_attrs != []):
                ae_board_attrs_history.append(board_attrs)
        count_move+=1
    if print_winner:
        print("--Player " + str(board.is_final_board(board.positions_AA, board.positions_AE)['winner']) + " Wins!--")
  
    # Actualizo coeficientes de Jugador AA, en base a mínimos cuadrados 
    new_coefficients = train_aa.update_coefficients(player1.parameters, aa_board_attrs_history)
    player1.update_parameters(new_coefficients)

    winner = board.is_final_board(board.positions_AA, board.positions_AE)['winner']
    result = (winner,count_move/2)

    # Solo queremos guardar historial de tableros para Jugador AE cuando gana la partida
    if winner != constants.PLAYER_AE:
        ae_board_attrs_history = []
 
    return result, ae_board_attrs_history
