import copy
import math
import pprint
import random
from board import Board

class Generator(object):
    def __init__(self, board, **kwargs):
        self.board = board


    def place_player_final(self, play_number, player_number):
        player_index = player_number - 1

        if (play_number == 1):
            coord_x = 0
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 0
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 0
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 0
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))
        elif (play_number == 2):
            coord_x = 0
            coord_y = 4
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 0
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 0
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 0
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))
        elif (play_number == 3):
            coord_x = 1
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

        elif (play_number == 4):
            coord_x = 1
            coord_y = 4
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

        elif (play_number == 5):
            coord_x = 2
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

        elif (play_number == 6):
            coord_x = 2
            coord_y = 4
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

        elif (play_number == 7):
            coord_x = 3
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

        elif (play_number == 8):
            coord_x = 1
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 0
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

        elif (play_number == 9):
            coord_x = 4
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

        elif (play_number == 10):
            coord_x = 2
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 4
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

        elif (play_number == 11):
            coord_x = 0
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))
        elif (play_number == 12):
            coord_x = 0
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))
        elif (play_number == 13):
            coord_x = 4
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

        elif (play_number == 14):
            coord_x = 0
            coord_y = 4
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 4
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 4
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 4
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

        elif (play_number == 15):
            coord_x = 0
            coord_y = 0
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

        elif (play_number == 16):
            coord_x = 1
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 4
            coord_y = 4
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

        elif (play_number == 17):
            coord_x = 0
            coord_y = 4
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 1
            coord_y = 3
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 2
            coord_y = 2
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))

            coord_x = 3
            coord_y = 1
            self.board.place_player(coord_x, coord_y, player_number)
            self.used_coords.append((coord_x, coord_y))
            self.player_used_coords[player_index].append((coord_x, coord_y))


    def place_player(self, player_number):
        ''' Used to place players in the board '''
        player_index = player_number - 1

        while len(self.player_used_coords[player_index]) < self.board.pieces:
            coord_x = random.randint(0, self.board.rows - 1)
            coord_y = random.randint(0, self.board.cols - 1)

            # Check if randomly chosen coord is already taken
            if ((coord_x, coord_y) not in self.used_coords):
                self.board.place_player(coord_x, coord_y, player_number)
                self.used_coords.append((coord_x, coord_y))
                self.player_used_coords[player_index].append((coord_x, coord_y))

    def print_current(self):
        pprint.pprint(self.board.current_board)

    def generate_board(self):
        initialized = False
        while not initialized:
            self.board.clear_board()
            self.used_coords = []
            self.player_used_coords = [[], []]
            self.place_player(1)
            self.place_player(2)
            self.board.initial_board = copy.deepcopy(self.board.current_board)
            self.board.update_attrs()
            if not self.board.is_final()['is_final']:
                initialized = True


    def generate_final_board(self,play_number, player_number):
        self.board.clear_board()
        self.used_coords = []
        self.player_used_coords = [[], []]
        self.place_player_final(play_number, player_number)
        if player_number == 1:
            player_number = 2
        else:
            player_number = 1
        self.place_player(player_number)
        self.board.initial_board = copy.deepcopy(self.board.current_board)
        self.board.update_attrs()
        final_board = copy.deepcopy(self.board.current_board)
        return final_board
    
    # ==== Test Board Generators ====
    def generate_fixed_board(self, board_number):
        if board_number == 1:
            self.generate_test_board_1()
        if board_number == 2:
            self.generate_test_board_2()
        if board_number == 3:
            self.generate_test_board_3()
        if board_number == 4:
            self.generate_test_board_4()
        if board_number == 5:
            self.generate_test_board_5()
        
    
    def generate_test_board_1(self):
        self.board.current_board[0][2], self.board.current_board[1][1], self.board.current_board[2][0], self.board.current_board[4][4] = 1, 1, 1, 1
        self.board.positions[0].append((0,2))
        self.board.positions[0].append((1,1))
        self.board.positions[0].append((2,0))
        self.board.positions[0].append((4,4))
        self.board.current_board[0][0], self.board.current_board[4][2], self.board.current_board[3][3], self.board.current_board[2][4] = 2, 2, 2, 2
        self.board.positions[1].append((0,0))
        self.board.positions[1].append((4,2))
        self.board.positions[1].append((3,3))
        self.board.positions[1].append((2,4))
        self.board.initial_board = copy.deepcopy(self.board.current_board)
        self.board.update_attrs()

    def generate_test_board_2(self):
        self.board.current_board[0][2], self.board.current_board[1][1], self.board.current_board[2][0], self.board.current_board[0][4] = 1, 1, 1, 1
        self.board.positions[0].append((0,2))
        self.board.positions[0].append((1,1))
        self.board.positions[0].append((2,0))
        self.board.positions[0].append((0,4))
        self.board.current_board[4][0], self.board.current_board[4][2], self.board.current_board[3][3], self.board.current_board[2][4] = 2, 2, 2, 2
        self.board.positions[1].append((4,0))
        self.board.positions[1].append((4,2))
        self.board.positions[1].append((3,3))
        self.board.positions[1].append((2,4))
        self.board.initial_board = copy.deepcopy(self.board.current_board)
        self.board.update_attrs()
    
    def generate_test_board_3(self):
        self.board.current_board[0][0], self.board.current_board[4][4], self.board.current_board[1][3], self.board.current_board[3][1] = 1, 1, 1, 1
        self.board.positions[0].append((0,0))
        self.board.positions[0].append((4,4))
        self.board.positions[0].append((1,3))
        self.board.positions[0].append((3,1))
        self.board.current_board[0][4], self.board.current_board[1][1], self.board.current_board[3][3], self.board.current_board[4][0] = 2, 2, 2, 2
        self.board.positions[1].append((0,4))
        self.board.positions[1].append((1,1))
        self.board.positions[1].append((3,3))
        self.board.positions[1].append((4,0))
        self.board.initial_board = copy.deepcopy(self.board.current_board)
        self.board.update_attrs()
    
    def generate_test_board_4(self):
        self.board.current_board[1][0], self.board.current_board[3][0], self.board.current_board[4][2], self.board.current_board[2][4] = 1, 1, 1, 1
        self.board.positions[0].append((1,0))
        self.board.positions[0].append((3,0))
        self.board.positions[0].append((4,2))
        self.board.positions[0].append((2,4))
        self.board.current_board[2][0], self.board.current_board[0][2], self.board.current_board[1][4], self.board.current_board[3][4] = 2, 2, 2, 2
        self.board.positions[1].append((2,0))
        self.board.positions[1].append((0,2))
        self.board.positions[1].append((1,4))
        self.board.positions[1].append((3,4))
        self.board.initial_board = copy.deepcopy(self.board.current_board)
        self.board.update_attrs()
    
    def generate_test_board_5(self):
        self.board.current_board[0][4], self.board.current_board[2][1], self.board.current_board[2][4], self.board.current_board[3][2] = 1, 1, 1, 1
        self.board.positions[0].append((0,4))
        self.board.positions[0].append((2,1))
        self.board.positions[0].append((2,4))
        self.board.positions[0].append((3,2))
        self.board.current_board[2][0], self.board.current_board[1][2], self.board.current_board[2][3], self.board.current_board[4][0] = 2, 2, 2, 2
        self.board.positions[1].append((2,0))
        self.board.positions[1].append((1,2))
        self.board.positions[1].append((2,3))
        self.board.positions[1].append((4,0))
        self.board.initial_board = copy.deepcopy(self.board.current_board)
        self.board.update_attrs()
     

