import copy
import math
import pprint
import random
import constants
import minimax

class Player(object):
    def __init__(self, parameters, player):
        self.parameters = parameters
        self.fitness = 0
        self.player_id = player
    
    # Dado un obj tablero, decide cual es el mejor movimiento basado en sus parameters y en las posiciones del tablero, para jugador ae
    def decide_best_movement_ae(self, board, print_value, choose_random, do_minimax):
        initial_position = []
        final_position = []
        posible_positions = board.list_positions_of_possible_movements(self.player_id)
        max_value = float('-inf')
        max_attrs = []
        if choose_random:
            pos = random.choice(posible_positions)
            initial_position, final_position, move_value, max_value, max_attrs = self.decide_movement_ae(pos, board, max_value, max_attrs, initial_position, final_position, do_minimax)
        else:
            for pos in posible_positions: # Para cada movimiento posible, calculo su valor
                initial_position, final_position, move_value, max_value, max_attrs = self.decide_movement_ae(pos, board, max_value, max_attrs, initial_position, final_position, do_minimax)
        if print_value:
            print("----Player "+ str(self.player_id) +" Turn!----")
            print("Player "+ str(self.player_id) +" moved: " + str(initial_position) + " to: " + str(final_position))
            print("Move value: " + str(move_value))
            print("-------------------------------\n")
        return [initial_position, final_position], max_attrs
    
    def decide_movement_ae(self, pos, board, max_value, max_attrs, initial_position, final_position, minimax):
        initial_position_temp = self.diff(board.positions_AE, pos[self.player_id])[0]
        final_position_temp = self.diff(board.positions_AE, pos[self.player_id])[1]
        move_adj = board.count_adjacencies(pos[0], pos[1])
        
        move_value =  sum([x*y for x,y in zip(self.parameters[0:3:1], move_adj[self.player_id])]) # 1) Calculo el valor de las adyacencias
        alert_value = self.calculate_alert_value(board, pos[0], pos[1]) * self.parameters[4] # 2) Evaluo si el movimineto me lleva a ganar
        minimax_value = self.calculate_minimax_value(copy.deepcopy(board), self.player_id, minimax) * self.parameters[5] # 3) Evaluo el valor del futuro de la jugada con minimax
        adj_value_Lshape = self.calculate_ae_adj_Lshape(copy.deepcopy(board), pos, self.player_id, initial_position_temp, final_position_temp) * self.parameters[6] # 4) Si el movimiento acerca una ficha a la adyacencia faltante prinicipal 
        adj_value_line = self.calculate_ae_adj_line(copy.deepcopy(board), pos, self.player_id, initial_position_temp, final_position_temp) * self.parameters[7] # 5) Si el movimiento acerca una ficha a la adyacencia faltante prinicipal 
        rival_adj_value_Lshape = self.calculate_rival_adj_Lshape(copy.deepcopy(board), pos, self.player_id, initial_position_temp, final_position_temp) * self.parameters[8] # 6) Si el movimiento acerca una ficha a la adyacencia faltante del rival
        rival_adj_value_line = self.calculate_rival_adj_line(copy.deepcopy(board), pos, self.player_id, initial_position_temp, final_position_temp) * self.parameters[9] # 7) Si el movimiento acerca una ficha a la adyacencia faltante del rival 
        
        final_move_value = move_value + alert_value + minimax_value + adj_value_Lshape + adj_value_line + rival_adj_value_Lshape + rival_adj_value_line # Valor final del movimiento 
        
        normalized_move_adj_ae = self.normalize_attrs_ae(move_adj[self.player_id]+ [alert_value] + [minimax_value] + [adj_value_Lshape] + [adj_value_line] + [rival_adj_value_Lshape] + [rival_adj_value_line]) # Jugador AE utiliza attrs normalizados solamente para guardar historial de tableros
        if final_move_value > max_value: # Si encontre un movimiento mejor lo reescribo
            max_value = final_move_value
            max_attrs = normalized_move_adj_ae
            initial_position = initial_position_temp
            final_position = final_position_temp
        return initial_position, final_position, final_move_value, max_value, max_attrs
        
    # Dado un obj tablero, decide cual es el mejor movimiento basado en sus parameters y en las posiciones del tablero, para jugador aa
    def decide_best_movement_aa(self, board, print_value, choose_random):
        initial_position = []
        final_position = []
        posible_positions = board.list_positions_of_possible_movements(self.player_id)
        max_value = float('-inf')
        max_attrs = []
        if choose_random:
            pos = random.choice(posible_positions)
            initial_position, final_position, move_value, max_value, max_attrs = self.decide_movement_aa(pos, board, max_value, max_attrs, initial_position, final_position)
        else:
            for pos in posible_positions: # Para cada movimiento posible, calculo su valor
                initial_position, final_position, move_value, max_value, max_attrs = self.decide_movement_aa(pos, board, max_value, max_attrs, initial_position, final_position)
        if print_value:
            print("----Player "+ str(self.player_id) +" Turn!----")
            print("Player "+ str(self.player_id) +" moved: " + str(initial_position) + " to: " + str(final_position))
            print("Move value: " + str(move_value))
            print("-------------------------------\n")
        return [initial_position, final_position], max_attrs
    
    def decide_movement_aa(self, pos, board, max_value, max_attrs, initial_position, final_position):
        move_adj = board.count_adjacencies(pos[0], pos[1])
        move_adj_aa = [1] + move_adj[constants.PLAYER_AA] + move_adj[constants.PLAYER_AE] # Jugador AA utiliza un attr dummy = 1, y los 8 attrs de adj
        normalized_move_adj_aa = self.normalize_attrs_aa(move_adj_aa) # Jugador AA utiliza attrs normalizados
        move_value =  sum([x*y for x,y in zip(self.parameters, normalized_move_adj_aa)])  # 1) Calculo el valor de las adyacencias
        if move_value > max_value: # Si encontre un movimiento mejor
            max_value = move_value
            max_attrs = normalized_move_adj_aa
            initial_position = self.diff(board.positions_AA, pos[self.player_id])[0]
            final_position = self.diff(board.positions_AA, pos[self.player_id])[1]
        return initial_position, final_position, move_value, max_value, max_attrs

    # Si el movimiento lleva a un tablero final retorna 1, sino 0
    def calculate_alert_value(self, board, positions_player1, positions_player2):
        alert_value = 1 if board.is_final_board(positions_player1, positions_player2)['final'] else 0
        return alert_value
    
    # Retorna el valor minimax de board para el jugador player_id
    def calculate_minimax_value(self, board, player_id, do_minimax):
        if do_minimax:
            return minimax.minimaxWithAlphaBetaPruningSinArbol(copy.deepcopy(board), 2, 0, float('-inf'), float('inf'))
        else:
            return 0
    
    # Retorna 1 si el movimiento acerca una ficha a ciertas posiciones objetivo que completan las adyacencias ganadoras
    # Ej: si hay 1 ady horiz y 1 adj vertic (hay una 'L' de fichas) -> la posicion objetivo es la que completa el cuadrado
    def calculate_ae_adj_Lshape(self, board, pos, player_id, initial_position, final_position):
        res = 0
        move_adj = board.count_adjacencies(board.positions_AA, board.positions_AE)
        
        if move_adj[self.player_id][0] == 1 and move_adj[self.player_id][1] == 1: # Caso 1) Hay una 'L' de fichas
            (objective_position, L_positions) = board.get_objective_position_from_L(board.positions_AE)
            initial_distance = board.distance_between_positions(initial_position, objective_position)
            final_distance = board.distance_between_positions(final_position, objective_position)
            if initial_distance > final_distance and initial_distance > 1 and objective_position not in board.positions_AA: # Si el movimineto me acerca a la 'L'
                # print(str(initial_position) + str(final_position) + " movimiento acercador a " + str(objective_position))
                res = 1
        return res
    
    # Retorna 1 si el movimiento acerca una ficha a ciertas posiciones objetivo que completan las adyacencias ganadoras
    # Ej: si hay 2 ady horiz, verticales o diag -> la posicion objetivo es la que completa la fila de ady
    def calculate_ae_adj_line(self, board, pos, player_id, initial_position, final_position):  
        res = 0
        move_adj = board.count_adjacencies(board.positions_AA, board.positions_AE)
        
        if move_adj[self.player_id][0] == 2 or move_adj[self.player_id][1] == 2 or move_adj[self.player_id][2] == 2 or move_adj[self.player_id][3] == 2: # Caso 2) Hay 3 fichas en linea
            type_of_line = move_adj[self.player_id].index(2)
            (objective_position, line_positions)  = board.get_objective_position_from_line(board.positions_AE,type_of_line)
            for obj_pos in objective_position: # Para ambas puntas de la linea de ady
                initial_distance = board.distance_between_positions(initial_position, obj_pos)
                final_distance = board.distance_between_positions(final_position, obj_pos)
                if initial_distance > final_distance and initial_distance >= 1 and obj_pos not in board.positions_AA and initial_position not in line_positions:
                    # print(str(initial_position) + str(final_position) + " movimiento acercador a " + str(obj_pos))
                    res = 1
        return res
    
    # Retorna 1 si el movimiento acerca una ficha a ciertas posiciones objetivo que bloquean las adyacencias ganadoras del rival
    def calculate_rival_adj_Lshape(self, board, pos, player_id, initial_position, final_position):
        res = 0
        move_adj = board.count_adjacencies(board.positions_AA, board.positions_AE)
        
        if move_adj[0][0] == 1 and move_adj[0][1] == 1: # Caso 1) Hay una 'L' de fichas
            (objective_position, L_positions) = board.get_objective_position_from_L(board.positions_AA)
            initial_distance = board.distance_between_positions(initial_position, objective_position)
            final_distance = board.distance_between_positions(final_position, objective_position)
            if initial_distance > final_distance and initial_distance >= 1 and objective_position not in board.positions_AE: # Si el movimineto me acerca a la 'L'
                #print("L: " +  str(initial_position) + str(final_position) + " movimiento acercador a " + str(objective_position))
                res = 1
        return res
    
    # Retorna 1 si el movimiento acerca una ficha a ciertas posiciones objetivo que bloquean las adyacencias ganadoras del rival
    def calculate_rival_adj_line(self, board, pos, player_id, initial_position, final_position):  
        res = 0
        move_adj = board.count_adjacencies(board.positions_AA, board.positions_AE)
        
        if move_adj[0][0] == 2 or move_adj[0][1] == 2 or move_adj[0][2] == 2 or move_adj[0][3] == 2: # Caso 2) Hay 3 fichas en linea
            type_of_line = move_adj[0].index(2)
            (objective_position, line_positions) = board.get_objective_position_from_line(board.positions_AA,type_of_line)
            for obj_pos in objective_position: # Para ambas puntas de la linea de ady
                initial_distance = board.distance_between_positions(initial_position, obj_pos)
                final_distance = board.distance_between_positions(final_position, obj_pos)
                if initial_distance > final_distance and initial_distance >= 1 and obj_pos not in board.positions_AE:
                    #print("LINEA: " + str(initial_position) + str(final_position) + " movimiento acercador a " + str(obj_pos))
                    res = 1
        return res
    
    def diff(self, li1, li2):
        return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

    def update_parameters(self, new_parameters):
        self.parameters = new_parameters
    
    def normalize_attrs_aa(self, attrs):
        min_attr_vals = [1] + ([0] * 8)
        max_attr_vals = [1] + ([3] * 8)
        aux_attrs = copy.deepcopy(attrs)
        for i, attr in enumerate(aux_attrs):
            diff = (max_attr_vals[i] - min_attr_vals[i])
            if diff != 0:
                attrs[i] = (attr - min_attr_vals[i]) / diff
            else:
                attrs[i] = 1
        return aux_attrs


    def normalize_attrs_ae(self, attrs):
        min_attr_vals = ([0] * 4) + [0] + [0] + [0] + [0] + [0] + [0]
        max_attr_vals = ([3] * 4) + [1] + [5] + [1] + [1] + [1] + [1]
        aux_attrs = copy.deepcopy(attrs)
        for i, attr in enumerate(aux_attrs):
            diff = (max_attr_vals[i] - min_attr_vals[i])
            if diff != 0:
                attrs[i] = (attr - min_attr_vals[i]) / diff
            else:
                attrs[i] = 1
        return aux_attrs