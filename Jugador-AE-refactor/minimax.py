import copy
from board import Board
from anytree import Node, RenderTree
import constants
    
# Retorna un entero que simboliza que tan bueno sera el tablero para el Jugador 1 en 'depth' jugadas
# Asuminedo que cada jugador hace el movimineto que maximiza su ganancia
# Ganancia: sum(attrs_p1)
def minimaxWithAlphaBetaPruning(board, position, depth, maximizingPlayer, alpha, beta, tree):
    if depth == 0 or board.is_final_board(board.positions_AA, board.positions_AE)['final']:
        res = 0
        if board.is_final_board(board.positions_AA, board.positions_AE)['final']: # Si corte por tablero final, vale mas
           res += 1 
        adj_list = board.count_adjacencies(board.positions_AA, board.positions_AE)
        return res + sum(adj_list[1])
    if maximizingPlayer == constants.PLAYER_AE:
        maxEval = float('-inf')
        possible_movements = board.possible_movements(constants.PLAYER_AE) 
        for origin in possible_movements:
            for destiny in possible_movements[origin]:
                copy_board = copy.deepcopy(board)
                copy_board.move_player(origin, destiny, constants.PLAYER_AE)
                hijo = Node({"board": copy_board.create_matrix_board(copy_board.positions_AA, copy_board.positions_AE), "value": float('-inf'), "player": "MIN"}, parent=tree)
                newEval = minimaxWithAlphaBetaPruning(copy_board, copy_board.create_matrix_board(copy_board.positions_AA, copy_board.positions_AE), depth-1, constants.PLAYER_AA, alpha, beta, hijo)
                maxEval = max(maxEval, newEval)
                alpha = max(alpha, newEval)
                hijo.name['value'] = maxEval
                if beta <= alpha:
                    break
        return maxEval
    else:
        minEval = float('inf')
        possible_movements = board.possible_movements(constants.PLAYER_AA) 
        for origin in possible_movements:
            for destiny in possible_movements[origin]:
                copy_board = copy.deepcopy(board)
                copy_board.move_player(origin, destiny, constants.PLAYER_AA)
                hijo = Node({"board": copy_board.create_matrix_board(copy_board.positions_AA, copy_board.positions_AE), "value": float('-inf'), "player": "MAX"}, parent=tree)
                newEval = minimaxWithAlphaBetaPruning(copy_board, copy_board.create_matrix_board(copy_board.positions_AA, copy_board.positions_AE), depth-1, constants.PLAYER_AE, alpha, beta, hijo)
                minEval = min(minEval, newEval)
                beta = min(beta, newEval)
                hijo.name['value'] = minEval
                if beta <= alpha:
                    break
        return minEval

# Retorna un entero que simboliza que tan bueno sera el tablero para el Jugador 1 en 'depth' jugadas
# Asuminedo que cada jugador hace el movimineto que maximiza su ganancia
# Ganancia: sum(attrs_p1) - sum(attrs_p2)  
def minimaxWithAlphaBetaPruningSinArbol(board, depth, player_turn, alpha, beta):
    if depth == 0 or board.is_final_board(board.positions_AA, board.positions_AE)['final']:
        res = 0
        if board.is_final_board(board.positions_AA, board.positions_AE)['final']: # Si corte por tablero final, vale mas
           res += 0.5 
        adj_list = board.count_adjacencies(board.positions_AA, board.positions_AE)
        return res + sum(adj_list[1])
    if player_turn == constants.PLAYER_AE:
        maxEval = float('-inf')
        possible_movements = board.possible_movements(constants.PLAYER_AE) 
        for origin in possible_movements:
            for destiny in possible_movements[origin]:
                copy_board = copy.deepcopy(board)
                copy_board.move_player(origin, destiny, constants.PLAYER_AE)
                newEval = minimaxWithAlphaBetaPruningSinArbol(copy_board, depth-1, constants.PLAYER_AA, alpha, beta)
                maxEval = max(maxEval, newEval)
                alpha = max(alpha, newEval)
                if beta <= alpha:
                    break
        return maxEval
    else:
        minEval = float('inf')
        possible_movements = board.possible_movements(constants.PLAYER_AA)
        for origin in possible_movements:
            for destiny in possible_movements[origin]:
                copy_board = copy.deepcopy(board)
                copy_board.move_player(origin, destiny, constants.PLAYER_AA)
                newEval = minimaxWithAlphaBetaPruningSinArbol(copy_board, depth-1, constants.PLAYER_AE, alpha, beta)
                minEval = min(minEval, newEval)
                beta = min(beta, newEval)
                if beta <= alpha:
                    break
        return minEval