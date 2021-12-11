from board import Board
from player import Player
import constants
import random

def manual_play_set(player_parameters, print_move_values):
    board = Board()
    board.generate_default_board_0()
    manual_player = Player(player_parameters, constants.PLAYER_AE)
    manual_play(board, manual_player, print_move_values)

def manual_play(board, player, print_move_values):
    print("----NEW GAME----")
    player_turn = 0 
    turn = 1
    while board.is_final_board(board.positions_AA, board.positions_AE)['final'] == False:
        board.pp_board()
        print("\n ============TURN " +str(turn) + "============\n")
        turn +=1
        if player_turn == 0:
            valid_movement = False
            while not valid_movement:
                print("Human turn! (Player 0), Write a new movement with the following syntax: a,b->c,d \n OR: 'r' for a random Move")
                movement = input()
                if movement[0] == 'r' or movement[0] == 'R':
                    posible_positions = board.list_positions_of_possible_movements(0)
                    pos = random.choice(posible_positions)
                    initial_position = player.diff(board.positions_AA, pos[0])[0]
                    final_position = player.diff(board.positions_AA, pos[0])[1]
                    valid_movement = board.move_player(initial_position, final_position, 0)
                else:
                    initial_position = (int(movement[0]),int(movement[2]))
                    final_position = (int(movement[5]),int(movement[7]))
                    valid_movement = board.move_player(initial_position, final_position, 0)
                print("=> Human moved: " + str(initial_position) + " to: " + str(final_position) + "\n")
        else:
            print("AI Turn! (Player 1)")
            [initial_position, final_position] = player.decide_best_movement_ae(board, print_move_values, False)
            valid_movement = board.move_player(initial_position, final_position, 1)
        player_turn = (player_turn+1) % 2
    
    print("--Player " + str(board.is_final_board(board.positions_AA, board.positions_AE)['winner']) + " Wins!--")
    board.pp_board()
    return board.is_final_board(board.positions_AA, board.positions_AE)['winner']

