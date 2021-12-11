import copy
import math
import pprint
import random

class Board(object):
    def __init__(self, **kwargs):
        self.rows = kwargs.get('rows', 5)
        self.cols = kwargs.get('cols', 5)
        self.pieces = kwargs.get('pieces', 4)   # Max amount of pieces per player
        self.initial_board = [[0 for j in range(self.cols)] for i in range(self.rows)]
        self.current_board = copy.deepcopy(self.initial_board)
        self.attrs_aa = [0] * 9
        self.attrs_ae = [0] * 10
        self.min_attr_vals = [1] + ([0] * 8)
        self.max_attr_vals = [1] + ([3] * 8)
        self.last_move = [(-1, -1), (-1, -1)]
        # Players placed pieces positions
        self.positions = [[], []]
        self.lesser_left_diagonals = {(0,0), (0,1), (0,2), (1,0), (1,1), (2,0), (4,2), (4,3), (4,4), (3,3), (3,4), (2,4)}
        self.lesser_right_diagonals = {(0,2), (0,3), (0,4), (1,4), (1,3), (2,4), (2,0), (3,0), (3,1), (4,0), (4,1), (4,2)}
    
    def place_player(self, coord_x, coord_y, player_number):
        player_index = player_number - 1
        self.current_board[coord_x][coord_y] = player_number
        self.positions[player_index].append((coord_x, coord_y))

    def normalize_attrs(self, attrs):
        aux_attrs = copy.deepcopy(attrs)
        for i, attr in enumerate(aux_attrs):
            diff = (self.max_attr_vals[i] - self.min_attr_vals[i])
            if diff != 0:
                attrs[i] = (attr - self.min_attr_vals[i]) / diff
            else:
                attrs[i] = 1

    def get_attrs_from_movement(self, board, player):
        h_counter = 0
        v_counter = 0
        d_left_counter = 0
        d_right_counter = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == player:
                    if j < self.cols - 1 and board[i][j] == board[i][j + 1]:
                        h_counter+= 1
                    if i < self.rows - 1 and board[i][j] == board[i + 1][j]:
                        v_counter+= 1
                    if i < self.rows - 1:
                        if j > 0 and board[i][j] == board[i + 1][j - 1]:
                            d_left_counter+= 1
                        if j < self.cols - 1 and board[i][j] == board[i + 1][j + 1]:
                            d_right_counter+= 1

        res = [h_counter, v_counter, d_left_counter, d_right_counter]
        return res 

    def get_attrs_from_board_aa(self, board):
        h_counter = []
        v_counter = []
        d_left_counter = []
        d_right_counter = []
        v_counter.append(0)
        h_counter.append(0)
        d_left_counter.append(0)
        d_right_counter.append(0)
        h_counter.append(0)
        v_counter.append(0)
        d_left_counter.append(0)
        d_right_counter.append(0)

        player_numbers = [1, 2]

        for i in range(len(board)):
            for j in range(len(board[i])):
                for p in player_numbers:
                    if board[i][j] == p:
                        player_index = p - 1
                        if j < self.cols - 1 and board[i][j] == board[i][j + 1]:
                            h_counter[player_index] += 1
                        if i < self.rows - 1 and board[i][j] == board[i + 1][j]:
                            v_counter[player_index] += 1
                        if i < self.rows - 1:
                            if j > 0 and board[i][j] == board[i + 1][j - 1]:
                                d_left_counter[player_index] += 1
                            if j < self.cols - 1 and board[i][j] == board[i + 1][j + 1]:
                                d_right_counter[player_index] += 1

        res = [1, h_counter[0], v_counter[0], d_left_counter[0], d_right_counter[0],
               h_counter[1], v_counter[1], d_left_counter[1], d_right_counter[1]]
        
        self.normalize_attrs(res)

        return res


    def get_attrs_from_board_ae(self):
        h_counter = []
        v_counter = []
        d_left_counter = []
        d_right_counter = []

        v_counter.append(0)
        h_counter.append(0)
        d_left_counter.append(0)
        d_right_counter.append(0)

        h_counter.append(0)
        v_counter.append(0)
        d_left_counter.append(0)
        d_right_counter.append(0)

        player_numbers = [1, 2]

        for p in player_numbers:
            player_index = p - 1
            for x_coord, y_coord in self.positions[player_index]:
                if (x_coord + 1, y_coord) in self.positions[player_index]:
                    v_counter[player_index] += 1
                if (x_coord, y_coord + 1) in self.positions[player_index]:
                    h_counter[player_index] += 1
                if (x_coord + 1, y_coord + 1) in self.positions[player_index] and (x_coord, y_coord) not in self.lesser_right_diagonals and (x_coord + 1, y_coord + 1) not in self.lesser_right_diagonals:
                    d_right_counter[player_index] += 1
                if (x_coord - 1, y_coord + 1) in self.positions[player_index] and (x_coord, y_coord) not in self.lesser_left_diagonals and (x_coord - 1, y_coord + 1) not in self.lesser_left_diagonals:
                    d_left_counter[player_index] += 1
        
        #si tablero no es ganador para jugador AE, y existe posible posición ganadora para jugador AA, activo alerta
        #attr_alert = 0 activa alerta
        attr_alert = 3
        if (h_counter[1] < 3 and v_counter[1] < 3 and d_left_counter[1] < 3 and d_right_counter[1] < 3 and (h_counter[1] < 2 or v_counter[1] < 2)):
            if (h_counter[0] == 2 or v_counter[0] == 2 or d_left_counter[0] == 2 or d_right_counter[0] == 2 or (h_counter[0] == 1 and v_counter[0] == 1 and (d_right_counter[0] == 1 or d_left_counter[0] == 1))):
                if self.verify_possible_loss():
                    attr_alert = 0
        res = [1, h_counter[0], v_counter[0], d_left_counter[0], d_right_counter[0],
               h_counter[1], v_counter[1], d_left_counter[1], d_right_counter[1], attr_alert]

        return res
    
    def verify_possible_loss(self):
        activate_alert = False
        player_aa = 1
        movements_aa = self.possible_movements(player_aa)
        for movement in movements_aa:
            h_adjs, v_adjs, d_l_adjs, d_r_adjs = self.get_attrs_from_movement(movement, 1)
            if h_adjs == 3 or v_adjs == 3 or d_r_adjs == 3 or d_l_adjs == 3 or (h_adjs == 2 and v_adjs == 2):
                activate_alert = True
                break
        return activate_alert

    def is_final(self):
        h_adjs_1, v_adjs_1, d_r_adjs_1, d_l_adjs_1 = self.count_adjacencies(1)
        h_adjs_2, v_adjs_2, d_r_adjs_2, d_l_adjs_2 = self.count_adjacencies(2)
        # Player 1 is the winner
        if h_adjs_1 == 3 or v_adjs_1 == 3 or d_r_adjs_1 == 3 or d_l_adjs_1 == 3 or (h_adjs_1 == 2 and v_adjs_1 == 2):
            return {'winner': 1, 'is_final': True}
        # Player 2 is the winner
        if h_adjs_2 == 3 or v_adjs_2 == 3 or d_r_adjs_2 == 3 or d_l_adjs_2 == 3 or (h_adjs_2 == 2 and v_adjs_2 == 2):
            return {'winner': 2, 'is_final': True}
        # It's not a final board
        return {'winner': 0, 'is_final': False}
    
    def is_final_ae(self):
        one, h_adjs_1, v_adjs_1, d_l_adjs_1, d_r_adjs_1, h_adjs_2, v_adjs_2, d_l_adjs_2, d_r_adjs_2, alert = self.get_attrs_from_board_ae()
        # Player 1 is the winner
        if h_adjs_1 == 3 or v_adjs_1 == 3 or d_r_adjs_1 == 3 or d_l_adjs_1 == 3 or (h_adjs_1 == 2 and v_adjs_1 == 2):
            return {'winner': 1, 'is_final': True}
        # Player 2 is the winner
        if h_adjs_2 == 3 or v_adjs_2 == 3 or d_r_adjs_2 == 3 or d_l_adjs_2 == 3 or (h_adjs_2 == 2 and v_adjs_2 == 2):
            return {'winner': 2, 'is_final': True}
        # It's not a final board
        return {'winner': 0, 'is_final': False}

    # Recive position matriz de tablero y retorna si es final o no y quien gano
    def is_final_position(self, position):
        h_adjs_1, v_adjs_1, d_l_adjs_1, d_r_adjs_1 = self.get_attrs_from_movement(position, 1)
        h_adjs_2, v_adjs_2, d_l_adjs_2, d_r_adjs_2 = self.get_attrs_from_movement(position, 2)
        if h_adjs_1 == 3 or v_adjs_1 == 3 or d_r_adjs_1 == 3 or d_l_adjs_1 == 3 or (h_adjs_1 == 2 and v_adjs_1 == 2):
            return {'winner': 1, 'is_final': True}
        # Player 2 is the winner
        if h_adjs_2 == 3 or v_adjs_2 == 3 or d_r_adjs_2 == 3 or d_l_adjs_2 == 3 or (h_adjs_2 == 2 and v_adjs_2 == 2):
            return {'winner': 2, 'is_final': True}
        # It's not a final board
        return {'winner': 0, 'is_final': False}
    
    def update_board(self, new_board, player_number):
        player_index = player_number - 1

        for i in range(self.rows):
            for j in range(self.cols):
                if self.current_board[i][j] != new_board[i][j]:
                    # If the old coord has the player number -> delete that coord
                    if self.current_board[i][j] == player_number:
                        self.positions[player_index].remove((i, j))
                        self.last_move[0] = (i, j)
                    # If the old coord has 0 -> add that coord
                    else:
                        self.positions[player_index].append((i, j))
                        self.last_move[1] = (i, j)

        self.current_board = new_board
        self.update_attrs()
        
    # Recive newBoard matriz de tablero y actualiza el tablero de la clase y las positions
    def update_board_and_positions(self, newBoard):
        self.clear_board()
        self.current_board = newBoard
        for i in range(self.rows):
            for j in range(self.cols):
                if(newBoard[i][j] == 1):
                    self.positions[0].append((i,j))
                if(newBoard[i][j] == 2):
                    self.positions[1].append((i,j))

    def clear_board(self):
        self.positions = [[], []]
        self.initial_board = [[0 for j in range(self.cols)] for i in range(self.rows)]
        self.current_board = self.initial_board
        self.attrs_aa = [0] * 9
        self.last_move = [(-1, -1), (-1, -1)]

    def update_attrs(self):
        self.attrs_aa = self.get_attrs_from_board_aa(self.current_board)

    def count_adjacencies(self, player_number):
        h_adjs = 0
        v_adjs = 0
        d_r_adjs = 0
        d_l_adjs = 0
        player_index = player_number - 1
        for x_coord, y_coord in self.positions[player_index]:
            if (x_coord + 1, y_coord) in self.positions[player_index]:
                v_adjs += 1
            if (x_coord, y_coord + 1) in self.positions[player_index]:
                h_adjs += 1
            if (x_coord + 1, y_coord + 1) in self.positions[player_index] and (x_coord, y_coord) not in self.lesser_right_diagonals and (x_coord + 1, y_coord + 1) not in self.lesser_right_diagonals:
                d_r_adjs += 1
            if (x_coord - 1, y_coord + 1) in self.positions[player_index] and (x_coord, y_coord) not in self.lesser_left_diagonals and (x_coord - 1, y_coord + 1) not in self.lesser_left_diagonals:
                d_l_adjs += 1
        return [h_adjs, v_adjs, d_r_adjs, d_l_adjs]
    
    # ==== Preety Print board ====
    def preety_print_board(self):
        for rows in range(self.rows):
            print(" | " + str(self.current_board[rows][0]) + " " + str(self.current_board[rows][1]) + " " + str(self.current_board[rows][2]) + " " + str(self.current_board[rows][3]) + " " + str(self.current_board[rows][4]) + " | ")

    def preety_print_position(self, position):
        for rows in range(self.rows):
            print(" | " + str(position[rows][0]) + " " + str(position[rows][1]) + " " + str(position[rows][2]) + " " + str(position[rows][3]) + " " + str(position[rows][4]) + " | ")
    
    def possible_movements(self, player_number):
        player_index = player_number - 1
        possible_movements = []
        current_positions = self.positions[player_index]

        # print("Player number :", player_number)

        for i in range(len(current_positions)):
            pos = current_positions[i]
            coord_x, coord_y = pos

            # print("Tuple :", pos)

            x_valid_inf = 1
            x_valid_sup = 1
            y_valid_inf = 1
            y_valid_sup = 1

            if (coord_x - 1 < 0):
                x_valid_inf = 0
            if (coord_x + 1 > 4):
                x_valid_sup = 0
            if (coord_y - 1 < 0):
                y_valid_inf = 0
            if (coord_y + 1 > 4):
                y_valid_sup = 0

            possible_positions = []

            # En cuadrado formado por las 9 coordenadas centrales
            if (x_valid_inf) and (x_valid_sup) and (y_valid_inf) and (y_valid_sup):
                # print("8 valid positions")
                possible_positions.append((coord_x, coord_y - 1))
                possible_positions.append((coord_x, coord_y + 1))
                possible_positions.append((coord_x - 1, coord_y - 1))
                possible_positions.append((coord_x - 1, coord_y))
                possible_positions.append((coord_x - 1, coord_y + 1))
                possible_positions.append((coord_x + 1, coord_y - 1))
                possible_positions.append((coord_x + 1, coord_y))
                possible_positions.append((coord_x + 1, coord_y + 1))
            # En 3 coordenadas centrales con y = 0.
            if (x_valid_inf) and (x_valid_sup) and (not y_valid_inf):
                # print("5 valid positions")
                possible_positions.append((coord_x, coord_y + 1))
                possible_positions.append((coord_x - 1, coord_y))
                possible_positions.append((coord_x - 1, coord_y + 1))
                possible_positions.append((coord_x + 1, coord_y))
                possible_positions.append((coord_x + 1, coord_y + 1))
            # En 3 coordenadas centrales con y = 4.
            if (x_valid_inf) and (x_valid_sup) and (not y_valid_sup):
                # print("5 valid positions")
                possible_positions.append((coord_x, coord_y - 1))
                possible_positions.append((coord_x - 1, coord_y - 1))
                possible_positions.append((coord_x - 1, coord_y))
                possible_positions.append((coord_x + 1, coord_y - 1))
                possible_positions.append((coord_x + 1, coord_y))
            # En 3 coordenadas centrales con x = 0.
            if (not x_valid_inf) and (y_valid_inf) and (y_valid_sup):
                # print("5 valid positions")
                possible_positions.append((coord_x, coord_y - 1))
                possible_positions.append((coord_x, coord_y + 1))
                possible_positions.append((coord_x + 1, coord_y - 1))
                possible_positions.append((coord_x + 1, coord_y))
                possible_positions.append((coord_x + 1, coord_y + 1))
            # En 3 coordenadas centrales con x = 4.
            if (not x_valid_sup) and (y_valid_inf) and (y_valid_sup):
                # print("5 valid positions")
                possible_positions.append((coord_x, coord_y - 1))
                possible_positions.append((coord_x, coord_y + 1))
                possible_positions.append((coord_x - 1, coord_y - 1))
                possible_positions.append((coord_x - 1, coord_y))
                possible_positions.append((coord_x - 1, coord_y + 1))
            #En (0,0)
            if (not x_valid_inf) and (not y_valid_inf):
                # print("3 valid positions")
                possible_positions.append((coord_x, coord_y + 1))
                possible_positions.append((coord_x + 1, coord_y))
                possible_positions.append((coord_x + 1, coord_y + 1))
            #En (0,4)
            if (not x_valid_inf) and (not y_valid_sup):
                # print("3 valid positions")
                possible_positions.append((coord_x, coord_y - 1))
                possible_positions.append((coord_x + 1, coord_y))
                possible_positions.append((coord_x + 1, coord_y - 1))
            #En (4,4)
            if (not x_valid_sup) and (not y_valid_sup):
                # print("3 valid positions")
                possible_positions.append((coord_x, coord_y - 1))
                possible_positions.append((coord_x - 1, coord_y - 1))
                possible_positions.append((coord_x - 1, coord_y))
            #En (4,0)
            if (not x_valid_sup) and (not y_valid_inf):
                # print("3 valid positions")
                possible_positions.append((coord_x, coord_y + 1))
                possible_positions.append((coord_x - 1, coord_y + 1))
                possible_positions.append((coord_x - 1, coord_y))

            aux_coord_x = 0
            aux_coord_y = 0

            # print("Positions size :", len(possible_positions))
            for cp in range(len(possible_positions)):
                # print(possible_positions[cp])
                aux_coord_x, aux_coord_y = possible_positions[cp]
                possible_board = copy.deepcopy(self.current_board)
                if (possible_board[aux_coord_x][aux_coord_y] == 0):
                    possible_board[aux_coord_x][aux_coord_y] = player_number
                    possible_board[coord_x][coord_y] = 0
                    possible_movements.append(possible_board)
                    # pprint.pprint(possible_board)
                    # print("\n")

        return possible_movements


