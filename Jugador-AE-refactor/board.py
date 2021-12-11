import copy
import math
import pprint
import random
import constants

class Board(object):
    def __init__(self, **kwargs):
        self.attrs_AE = [0] * 10
        self.current_board = []
        self.initial_positions_AA = []
        self.initial_positions_AE = []
        self.positions_AE = []
        self.positions_AA = []
        self.lesser_left_diagonals = {(0,0), (0,1), (0,2), (1,0), (1,1), (2,0), (4,2), (4,3), (4,4), (3,3), (3,4), (2,4)}
        self.lesser_right_diagonals = {(0,2), (0,3), (0,4), (1,4), (1,3), (2,4), (2,0), (3,0), (3,1), (4,0), (4,1), (4,2)}
    
    # Retorna una lista donde el primer elemento es una lista con las adyacencias del jugador AA
    # el segundo elemento es una lista con las adyacencias del jugador AE
    def count_adjacencies(self, positions_player1, positions_player2):
        h_adjs_aa, v_adjs_aa, d_r_adjs_aa, d_l_adjs_aa = 0, 0, 0, 0
        h_adjs_ae, v_adjs_ae, d_r_adjs_ae, d_l_adjs_ae = 0, 0, 0, 0
        for x_coord, y_coord in positions_player1:
            if (x_coord + 1, y_coord) in positions_player1:
                v_adjs_aa += 1
            if (x_coord, y_coord + 1) in positions_player1:
                h_adjs_aa += 1
            if (x_coord + 1, y_coord + 1) in positions_player1:
                d_r_adjs_aa += 1
            if (x_coord - 1, y_coord + 1) in positions_player1:
                d_l_adjs_aa += 1
        for x_coord, y_coord in positions_player2:
            if (x_coord + 1, y_coord) in positions_player2:
                v_adjs_ae += 1
            if (x_coord, y_coord + 1) in positions_player2:
                h_adjs_ae += 1
            if (x_coord + 1, y_coord + 1) in positions_player2 and (x_coord, y_coord) not in self.lesser_right_diagonals and (x_coord + 1, y_coord + 1) not in self.lesser_right_diagonals:
                d_r_adjs_ae += 1
            if (x_coord - 1, y_coord + 1) in positions_player2 and (x_coord, y_coord) not in self.lesser_left_diagonals and (x_coord - 1, y_coord + 1) not in self.lesser_left_diagonals:
                d_l_adjs_ae += 1
        return [[h_adjs_aa, v_adjs_aa, d_r_adjs_aa, d_l_adjs_aa], [h_adjs_ae, v_adjs_ae, d_r_adjs_ae, d_l_adjs_ae]]
    
    # retorna un dict con info sobre si es un tablero final    
    def is_final_board(self, positions_player1, positions_player2):
        [[h_adjs_aa, v_adjs_aa, d_r_adjs_aa, d_l_adjs_aa], [h_adjs_ae, v_adjs_ae, d_r_adjs_ae, d_l_adjs_ae]] = self.count_adjacencies(positions_player1, positions_player2)
        if h_adjs_aa == 3 or v_adjs_aa == 3 or d_r_adjs_aa == 3 or d_l_adjs_aa == 3 or (h_adjs_aa == 2 and v_adjs_aa == 2):
            return {'final': True, 'winner': 0}
        elif h_adjs_ae == 3 or v_adjs_ae == 3 or d_r_adjs_ae == 3 or d_l_adjs_ae == 3 or (h_adjs_ae == 2 and v_adjs_ae == 2):
            return {'final': True, 'winner': 1}
        else:
            return {'final': False, 'winner': -1}
    
    # Mueve la ficha de initial_position a final_position del jugador player, retorna True si el movimiento fue valido
    def move_player(self, initial_position, final_position, player):
        if player == constants.PLAYER_AA:
            # si el jugador tiene una ficha en initial_position y final_position esta libre
            if initial_position in self.positions_AA and final_position not in self.positions_AE + self.positions_AA and final_position in self.possible_movements(constants.PLAYER_AA)[initial_position]:
                self.positions_AA.remove(initial_position)
                self.positions_AA.append(final_position)
                self.last_move_AA = final_position
                self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
                return True
            else:
                print("-Invalid movement for player " + str(constants.PLAYER_AA) + ". Move: " + str(initial_position) + "->" + str(final_position) + "-")
                return False
        elif player == constants.PLAYER_AE:
            # si el jugador tiene una ficha en initial_position y final_position esta libre
            if initial_position in self.positions_AE and final_position not in self.positions_AE + self.positions_AA and final_position in self.possible_movements(constants.PLAYER_AE)[initial_position]:
                self.positions_AE.remove(initial_position)
                self.positions_AE.append(final_position)
                self.last_move_AE = final_position
                self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
                return True
            else:
                print("-Invalid movement for player " + str(constants.PLAYER_AE) + " - " + str(initial_position) + "->" + str(final_position) + "-")
                return False
        else:
            print("-Invalid player for movement-")
            return False
    
    # Crea matriz tablero a partir de las positions actuales
    def create_matrix_board(self, positions_player1, positions_player2):
        matrix_board = [['-']*5,['-']*5,['-']*5,['-']*5,['-']*5]
        for x_coord, y_coord in positions_player1:
            matrix_board[x_coord][y_coord] = str(constants.PLAYER_AA)
        for x_coord, y_coord in positions_player2:
            matrix_board[x_coord][y_coord] = str(constants.PLAYER_AE)
        return matrix_board
    
    # Retorna una lista de listas con los posibles movimientos para cada ficha del jugador player
    def possible_movements(self, player):
        if player == constants.PLAYER_AA:
            current_positions = self.positions_AA
        elif player == constants.PLAYER_AE:
            current_positions = self.positions_AE
        else: 
            print("--Invalid Player--")
            pass
    
        possible_movements = {}
        for i in range(len(current_positions)):
            coord_x, coord_y = current_positions[i]
            possible_movements[(coord_x,coord_y)] = []
            # posibles movimientos verticales
            if coord_x + 1 < 5 and (coord_x+1, coord_y) not in self.positions_AE + self.positions_AA:
                possible_movements[(coord_x,coord_y)].append((coord_x+1, coord_y))
            if coord_x - 1 >= 0 and (coord_x-1, coord_y) not in self.positions_AE + self.positions_AA:
                possible_movements[(coord_x,coord_y)].append((coord_x-1, coord_y))
            # posibles movimientos horizontales
            if coord_y + 1 < 5 and (coord_x, coord_y+1) not in self.positions_AE + self.positions_AA:
                possible_movements[(coord_x,coord_y)].append((coord_x, coord_y+1))
            if coord_y - 1 >= 0 and (coord_x, coord_y-1) not in self.positions_AE + self.positions_AA:
                possible_movements[(coord_x,coord_y)].append((coord_x, coord_y-1))
            # posibles movimientos diagonales derechos
            if coord_x + 1 < 5 and coord_y + 1 < 5 and (coord_x+1, coord_y+1) not in self.positions_AE + self.positions_AA:
                possible_movements[(coord_x,coord_y)].append((coord_x+1, coord_y+1))
            if coord_x -1 >= 0 and coord_y - 1 >= 0 and (coord_x-1, coord_y-1) not in self.positions_AE + self.positions_AA:
                possible_movements[(coord_x,coord_y)].append((coord_x-1, coord_y-1))
            # posibles movimientos diagonales izq
            if coord_x + 1 < 5 and coord_y - 1 >= 0 and (coord_x+1, coord_y-1) not in self.positions_AE + self.positions_AA:
                possible_movements[(coord_x,coord_y)].append((coord_x+1, coord_y-1))
            if coord_x - 1 >= 0 and coord_y + 1 < 5 and (coord_x-1, coord_y+1) not in self.positions_AE + self.positions_AA:
                possible_movements[(coord_x,coord_y)].append((coord_x-1, coord_y+1))
        return possible_movements
    
    # Retorna una lista [[a,b],..,[c,d]] con las positions resultantes de aplicar todos los movimientos posibles
    def list_positions_of_possible_movements(self, player):
        possible_movements = self.possible_movements(player)
        res = []
        for initial in possible_movements:
            for final in possible_movements[initial]:
                if player == constants.PLAYER_AA:
                    copy_positions = copy.deepcopy(self.positions_AA)
                else:
                    copy_positions = copy.deepcopy(self.positions_AE)
                copy_positions.remove(initial)
                copy_positions.append(final)
                if player == constants.PLAYER_AA:
                    new_position = [copy_positions, copy.deepcopy(self.positions_AE)]
                else:
                    new_position = [copy.deepcopy(self.positions_AA), copy_positions]
                res.append(new_position)
        return res
                   
    # Preety print del tablero basado en las positions actuales
    def pp_board(self):
        pp_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
        print("    0 1 2 3 4  ")
        for rows in range(constants.ROWS):
            print(str(rows) + " | " + str(pp_board[rows][0]) + " " + str(pp_board[rows][1]) + " " + str(pp_board[rows][2]) + " " + str(pp_board[rows][3]) + " " + str(pp_board[rows][4]) + " | ")
 
    
    # ----- Funciones Para el Parametro calculate_main_adj_closeup ------   
    # Dadas dos posiciones del tablero (a,b), calcula la distancia entre estas
    def distance_between_positions(self, pos1, pos2):
        if pos1 == pos2: # Si son la misma posicion
            return -1
        elif pos1[0] == pos2[0]: # Si estan en la misma fila
            return abs(pos1[1] - pos2[1])
        elif pos1[1] == pos2[1]: # Si estan en la misma columna
            return abs(pos1[0] - pos2[0])
        elif abs(pos1[0] - pos2[0]) == abs(pos1[1] - pos2[1]): # Si estan en la misma diagonal
            return abs(pos1[0] - pos2[0])
        else: # Estan en distintas filas y columnas
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) - min(abs(pos1[0] - pos2[0]),abs(pos1[1] - pos2[1]))
    
    # Retorna True si pos es una ficha aislada en el tablero
    def is_isolated_position(self, pos):
        res = True
        for positions in self.positions_AE:
            if self.distance_between_positions(positions, pos) <= 1 and self.distance_between_positions(positions, pos) >= 0:
                res = False
        print("-----")
        return res

    # Retorna la posicion faltante para ganar cuando en el tablero hay una 'L' de fichas y las posiciones de la "L"
    def get_objective_position_from_L(self, positions_player):
        main_adj = set([])
        for x_coord, y_coord in positions_player:
            if (x_coord + 1, y_coord) in positions_player:
                main_adj.add((x_coord + 1, y_coord))
                main_adj.add((x_coord, y_coord))
            if (x_coord, y_coord + 1) in positions_player:
                main_adj.add((x_coord, y_coord+1))
                main_adj.add((x_coord, y_coord))
        
        # De aca para abajo son todo cuentas para hallar cual es la posicion faltante en la 'L' de fichas
        x_ocurrences, y_ocurrences = {}, {}
        for (x_coord, y_coord) in list(main_adj):
            if x_coord in x_ocurrences:
                x_ocurrences[x_coord] += 1
            else:
                x_ocurrences[x_coord] = 1
            if y_coord in y_ocurrences:
                y_ocurrences[y_coord] += 1
            else:
                y_ocurrences[y_coord] = 1
        
        for x in x_ocurrences:
            if x_ocurrences[x] == 1:
                objective_x = x
        for y in y_ocurrences:
            if y_ocurrences[y] == 1:
                objective_y = y
        return ((objective_x, objective_y), main_adj)

    # Retorna las posiciones faltantes para ganar cuando en el tablero hay 3 fichas horizontales y las posiciones de la horizontal
    def get_objective_position_from_line(self, positions_player, type_of_line):
        main_adj = set([])
        res = []
        
        if type_of_line == 0: # Son ady horizontales
            for x_coord, y_coord in positions_player:
                if (x_coord, y_coord + 1) in positions_player:
                    main_adj.add((x_coord, y_coord + 1))
                    main_adj.add((x_coord, y_coord))
            for (x_coord, y_coord) in list(main_adj):
                if (x_coord, y_coord+1) not in main_adj and y_coord+1 <= 4:
                    res.append((x_coord, y_coord+1))
                if (x_coord, y_coord-1) not in main_adj and y_coord-1 >= 0:
                    res.append((x_coord, y_coord-1))
                    
        elif type_of_line == 1: # Son ady verticales
            for x_coord, y_coord in positions_player:
                if (x_coord + 1, y_coord) in positions_player:
                    main_adj.add((x_coord+1, y_coord))
                    main_adj.add((x_coord, y_coord))
            for (x_coord, y_coord) in list(main_adj):
                if (x_coord+1, y_coord) not in main_adj and x_coord+1 <= 4:
                    res.append((x_coord+1, y_coord))
                if (x_coord-1, y_coord) not in main_adj and x_coord-1 >= 0:
                    res.append((x_coord-1, y_coord))
                    
        elif type_of_line == 2: # Son ady diagonales der
            for x_coord, y_coord in positions_player:
                if (x_coord+1, y_coord+1) in positions_player:
                    main_adj.add((x_coord + 1, y_coord + 1))
                    main_adj.add((x_coord, y_coord))
            for (x_coord, y_coord) in list(main_adj):
                if (x_coord+1, y_coord+1) not in main_adj and x_coord+1 <= 4 and y_coord+1 <= 4:
                    res.append((x_coord+1, y_coord+1))
                if (x_coord-1, y_coord-1) not in main_adj and x_coord-1 >= 0 and y_coord-1 >= 0:
                    res.append((x_coord-1, y_coord-1))
                    
        elif type_of_line == 3: # Son ady diagonales izq
            for x_coord, y_coord in positions_player:
                if (x_coord-1, y_coord+1) in positions_player:
                    main_adj.add((x_coord - 1, y_coord + 1))
                    main_adj.add((x_coord, y_coord))
            for (x_coord, y_coord) in list(main_adj):
                if (x_coord-1, y_coord+1) not in main_adj and x_coord >= 0 and y_coord+1 <= 4:
                    res.append((x_coord-1, y_coord+1))
                if (x_coord+1, y_coord-1) not in main_adj and x_coord <= 4 and y_coord-1 >= 0:
                    res.append((x_coord+1, y_coord-1))
        return (res, main_adj)
    
    # Genera tablero aleatorio simetrico y no final
    def generate_random_board(self):
        final = True
        while final:
            self.positions_AA = []
            self.positions_AE = []
            rand = random.random()
            while len(self.positions_AE) < 4:
                x_coord = random.randint(0, 4)
                y_coord = random.randint(0, 4)
                while (x_coord, y_coord) not in self.positions_AE + self.positions_AA and (x_coord, y_coord) != (2,2):
                    # Sorteo si simetrizo vertical horizontal o diagonal
                    if rand < 0.33 and y_coord != 2: 
                        self.positions_AE.append((x_coord,y_coord))
                        self.positions_AA.append((x_coord,4-y_coord))
                    elif rand >= 0.33 and rand < 0.66 and x_coord != 2:
                        self.positions_AE.append((x_coord,y_coord))
                        self.positions_AA.append((4-x_coord,y_coord))
                    elif rand >= 0.66:
                        self.positions_AE.append((x_coord,y_coord))
                        self.positions_AA.append((4-x_coord,4-y_coord))
                    else:
                        break
            self.initial_positions_AA = self.positions_AA
            self.initial_positions_AE = self.positions_AE
            self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
            if not self.is_final_board(self.positions_AA, self.positions_AE)['final']:
                final = False
        
    def generate_default_board_0(self):
        self.positions_AA = []
        self.positions_AE = []
        self.positions_AA.append((2,0))
        self.positions_AA.append((1,1))
        self.positions_AA.append((0,2))
        self.positions_AA.append((4,4))
        
        self.positions_AE.append((0,0))
        self.positions_AE.append((4,2))
        self.positions_AE.append((3,3))
        self.positions_AE.append((2,4))
        self.initial_positions_AA = self.positions_AA
        self.initial_positions_AE = self.positions_AE
        self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
    
    def generate_default_board_1(self):
        self.positions_AA = []
        self.positions_AE = []
        self.positions_AA.append((0,0))
        self.positions_AA.append((0,1))
        self.positions_AA.append((1,0))
        self.positions_AA.append((0,4))
        
        self.positions_AE.append((4,0))
        self.positions_AE.append((4,3))
        self.positions_AE.append((4,4))
        self.positions_AE.append((3,4))
        self.initial_positions_AA = self.positions_AA
        self.initial_positions_AE = self.positions_AE
        self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
    
    def generate_default_board_2(self):
        self.positions_AA = []
        self.positions_AE = []
        self.positions_AA.append((1,1))
        self.positions_AA.append((1,3))
        self.positions_AA.append((2,1))
        self.positions_AA.append((3,2))
        
        self.positions_AE.append((1,2))
        self.positions_AE.append((2,3))
        self.positions_AE.append((3,1))
        self.positions_AE.append((3,3))
        self.initial_positions_AA = self.positions_AA
        self.initial_positions_AE = self.positions_AE
        self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
        
    def generate_default_board_3(self):
        self.positions_AA = []
        self.positions_AE = []
        self.positions_AA.append((0,0))
        self.positions_AA.append((1,3))
        self.positions_AA.append((3,1))
        self.positions_AA.append((4,4))
        
        self.positions_AE.append((0,4))
        self.positions_AE.append((1,1))
        self.positions_AE.append((4,0))
        self.positions_AE.append((3,3))
        self.initial_positions_AA = self.positions_AA
        self.initial_positions_AE = self.positions_AE
        self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
        
    def generate_default_board_4(self):
        self.positions_AA = []
        self.positions_AE = []
        self.positions_AA.append((0,1))
        self.positions_AA.append((0,2))
        self.positions_AA.append((0,3))
        self.positions_AA.append((3,2))
        
        self.positions_AE.append((4,1))
        self.positions_AE.append((4,2))
        self.positions_AE.append((4,3))
        self.positions_AE.append((1,2))
        self.initial_positions_AA = self.positions_AA
        self.initial_positions_AE = self.positions_AE
        self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
    
    def generate_default_board_5(self):
        self.positions_AA = []
        self.positions_AE = []
        self.positions_AA.append((0,0))
        self.positions_AA.append((0,4))
        self.positions_AA.append((2,1))
        self.positions_AA.append((3,2))
        
        self.positions_AE.append((1,2))
        self.positions_AE.append((2,3))
        self.positions_AE.append((4,0))
        self.positions_AE.append((4,4))
        self.initial_positions_AA = self.positions_AA
        self.initial_positions_AE = self.positions_AE
        self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
    
    def generate_default_board_6(self):
        self.positions_AA = []
        self.positions_AE = []
        self.positions_AA.append((1,3))
        self.positions_AA.append((2,0))
        self.positions_AA.append((3,1))
        self.positions_AA.append((2,3))
        
        self.positions_AE.append((1,1))
        self.positions_AE.append((2,1))
        self.positions_AE.append((2,4))
        self.positions_AE.append((3,3))
        self.initial_positions_AA = self.positions_AA
        self.initial_positions_AE = self.positions_AE
        self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
    
    def generate_default_board_7(self):
        self.positions_AA = []
        self.positions_AE = []
        self.positions_AA.append((0,0))
        self.positions_AA.append((1,0))
        self.positions_AA.append((0,1))
        self.positions_AA.append((4,4))
        
        self.positions_AE.append((4,0))
        self.positions_AE.append((0,4))
        self.positions_AE.append((4,3))
        self.positions_AE.append((3,4))
        self.initial_positions_AA = self.positions_AA
        self.initial_positions_AE = self.positions_AE
        self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
        
    def generate_default_board_8(self):
        self.positions_AA = []
        self.positions_AE = []
        self.positions_AA.append((4,0))
        self.positions_AA.append((0,4))
        self.positions_AA.append((4,3))
        self.positions_AA.append((3,4))
        
        self.positions_AE.append((0,0))
        self.positions_AE.append((1,0))
        self.positions_AE.append((0,1))
        self.positions_AE.append((4,4))
        self.initial_positions_AA = self.positions_AA
        self.initial_positions_AE = self.positions_AE
        self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)
        
    def generate_default_board_9(self):
        self.positions_AA = []
        self.positions_AE = []
        self.positions_AA.append((1,0))
        self.positions_AA.append((3,0))
        self.positions_AA.append((1,4))
        self.positions_AA.append((3,4))
        
        self.positions_AE.append((0,1))
        self.positions_AE.append((0,3))
        self.positions_AE.append((4,1))
        self.positions_AE.append((4,3))
        self.initial_positions_AA = self.positions_AA
        self.initial_positions_AE = self.positions_AE
        self.current_board = self.create_matrix_board(self.positions_AA, self.positions_AE)