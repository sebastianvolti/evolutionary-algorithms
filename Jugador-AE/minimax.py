import copy
from board import Board
from anytree import Node, RenderTree

def minimaxFather():
    board = Board()
    board.generate_test_board_1()
    board.preety_print_board()
    print('')
    movement = {}
    root = Node({"board": board.current_board, "value": float('-inf'), "player": "MAX"})
    res = minimaxWithAlphaBetaPruning(board, board.current_board, movement, 3, True, float('-inf'), float('inf'), root)
    root.name['value'] = res
    
    cont = 0
    for pre, fill, node in RenderTree(root):
        cont += 1
        print("%s%s" % (pre, node.name))
        
    print("jugadas evaluladas: " + str(cont))
    
# Retorna un entero que simboliza que tan bueno sera el tablero para el Jugador 1 en 'depth' jugadas
# Asuminedo que cada jugador hace el movimineto que maximiza su ganancia
# Ganancia: sum(attrs_p1) - sum(attrs_p2)  
def minimaxWithAlphaBetaPruning(board, position, movements, depth, maximizingPlayer, alpha, beta, tree):
    if depth == 0 or board.is_final_position(position)['is_final']:
        attrs_p1 = board.get_attrs_from_movement(position, 1)
        attrs_p2 = board.get_attrs_from_movement(position, 2)
        return sum(attrs_p1) - sum(attrs_p2)
    if maximizingPlayer:
        maxEval = float('-inf')
        for newBoard in board.possible_movements(1):
            board.update_board_and_positions(newBoard)
            hijo = Node({"board": newBoard, "value": float('-inf'), "player": "MIN"}, parent=tree)
            newEval = minimaxWithAlphaBetaPruning(board, newBoard, movements, depth-1, False, alpha, beta, hijo)
            board.update_board_and_positions(newBoard)
            maxEval = max(maxEval, newEval)
            alpha = max(alpha, newEval)
            hijo.name['value'] = maxEval
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for newBoard in board.possible_movements(2):
            board.update_board_and_positions(newBoard)
            hijo = Node({"board": newBoard, "value": float('-inf'), "player": "MAX"}, parent=tree)
            newEval = minimaxWithAlphaBetaPruning(board, newBoard, movements, depth-1, True, alpha, beta, hijo)
            board.update_board_and_positions(newBoard)
            minEval = min(minEval, newEval)
            beta = min(beta, newEval)
            hijo.name['value'] = minEval
            if beta <= alpha:
                break
        return minEval