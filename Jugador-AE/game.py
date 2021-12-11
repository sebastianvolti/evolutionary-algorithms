import copy
import logging
import math
import pprint
import statistics

from generator import Generator
from board import Board
from performance_system import PerformanceSystem
from critic import Critic
from generalizer import Generalizer


def calculate_percentages(p_wins, draws):
    pass


def initial_training(board, generator, generalizer):
    # Winner finals
    for i in range(17):
       board.clear_board()
       if i < 17: 
           x = i
       else: 
           x = i % 17
       final_board = copy.deepcopy(generator.generate_final_board(x + 1, 1))
       logging.debug(pprint.pformat(final_board))
       training_set = [(final_board, 1)]
       generalizer.lms(training_set)
       logging.debug(generalizer.weights)

    # Loser finals
    for i in range(17):
       board.clear_board()
       if i < 17: 
           x = i
       else: 
           x = i % 17
       final_board = copy.deepcopy(generator.generate_final_board(x + 1, 2))
       logging.debug(pprint.pformat(final_board))
       training_set = [(final_board, -1)]
       generalizer.lms(training_set)
       logging.debug((generalizer.weights))


# "Fixed" parameters
mu_factor = 0.8 # Factor para enfriar
enfriamiento_por_ronda = False # Sisi, la unica variable en español. No se como se dice enfriamiento.
use_gamma = True # Si critic usa gamma o no
gamma = 0.9 
use_v = True # Si critic usa v o usa valores 1 y -1
do_initial_training = True
trainings = 1 # Cantidad de entrenamientos
rounds = 1 # Cantidad de rondas por entrenamiento
matches_per_round = 10 # Cantidad de partidas por ronda
draws_limit_movements = 100 # Cantidad de movimientos antes de decir que es empate

# Parameters
initial_mu = 0.1
initial_weights_p1 = [-0.3245326346849934, 0.1693042050134686, 0.16953670371976523, 0.22783655225690969, 0.22793136193535615, 0.3166528358145293, 0.3143485967442448, 0.35530630208678404, 0.3464082778644509]
fixed_weights_p1 = [-0.01870055657485548, 0.03074003071666052, 0.031318934572842926, -0.08270074674927273, -0.07011917467007431, -7.162670732412986e-05, 0.0008689605180341086, -0.002650084442916412, 0.003135239438228969]
random_every_x_moves_p1 = 3 # Cada cuantos movimientos el p1 hace uno random (1 = siempre random, 0 = nunca random)
random_every_x_moves_p2 = 3 # Cada cuantos movimientos el p2 hace uno random (1 = siempre random, 0 = nunca random)
player_1_random = False  # True si jugador 2 juega con sus propios pesos 
player_2_plays = True  # True si jugador 2 juega con sus propios pesos
play_with_fixed_weights = False # True si ambos jugadores juegan con pesos fijos
DEBUG = False # Imprime mensajes de debug si está en true


def play(individual, n_matches, fixed_boards):
    matches_per_round = n_matches
    if DEBUG:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logging.basicConfig(level=logging_level, format='%(message)s')
    global initial_weights_p1
    ### STATS ###
    draws = []
    p_wins = []

    if (play_with_fixed_weights == True):
        initial_weights_p1 = fixed_weights_p1

    results = []
    # Para cada entrenamiento
    for x in range(trainings):

        # Instanciar clases básicas
        count_matches = 0
        mu = initial_mu
        board = Board(rows=5, cols=5, pieces=4)
        generator = Generator(board)
        generator.generate_board()
        generalizer = Generalizer(board, initial_weights_p1, individual, mu)
        perf = PerformanceSystem(board, draws_limit_movements, random_every_x_moves_p1, random_every_x_moves_p2)

        # Hacer entrenamiento incial si corresponde
        if do_initial_training:
            initial_training(board, generator, generalizer)

        # Para cada ronda
        for i in range(rounds):
            p_wins.append([0, 0])
            draws.append(0)

            # Para cada partida
            for j in range(matches_per_round):

                # Limpio el tablero
                board.clear_board()
                
                if fixed_boards and j<5: # Los primeros 5 tableros son predeterminados
                    generator.generate_fixed_board(j+1)
                else:
                    generator.generate_board()
                # Juego
                game_performance = perf.play(generalizer.v, generalizer.v_individual, j, player_1_random)
                count_matches += 1

                result_movements = game_performance['movements_count']
                result_winner = 0
                # Si es un empate
                if game_performance['was_draw']:
                    results.append((result_winner,result_movements))
                    draws[i] += 1
                    logging.debug("------------ It's a draw! ------------")
                else:
                    winner = game_performance['winner']
                    results.append((winner,result_movements))
                    if winner != 0:
                        p_wins[i][winner - 1] += 1
                        logging.debug("------------ The winner is player " + str(winner) + " ------------")

                # Genero el conjunto de entrenamiento
                critic = Critic(board, gamma)

                # Si quiero que los pesos varíen, aplico critic y lms con generalizer
                if not play_with_fixed_weights:
                    v = None
                    if use_v:
                        v = generalizer.v

                    # Genero el conjunto de entrenamiento según si quiero usar v o 1, -1
                    training_set = critic.generate_training_set(game_performance['game_history'], use_gamma, v)

                    # Aplico lms
                    logging.debug("weights_player1 pre-lms:")
                    logging.debug(generalizer.weights)
                    generalizer.lms(training_set)
                    logging.debug("weights_player1 post-lms:")
                    logging.debug(generalizer.weights)

            if enfriamiento_por_ronda:
                mu += mu_factor

        printGameStatistics(rounds, p_wins, draws, False)
        
    return results

def printRoundResults(round, playerOneResults, playerTwoResults, draws):
    print("Round Number: ", round + 1)
    logging.info("--- Player Aprendizaje Automatico won " + str(playerOneResults) + " times ------------")
    logging.info("--- Player Algoritmos Evolutivos won " + str(playerTwoResults) + " times ------------")
    logging.info("--- There where " + str(draws) + " draws ------------")

def printGameStatistics(rounds, results, draws, percentages):
    p1_wins = [sum(x) for x in zip(*results)][0]
    p2_wins = [sum(x) for x in zip(*results)][1]
    total_draws = sum(draws)
    p1_wins_percentage = ((p1_wins / (p1_wins + p2_wins)) * 100) if (p1_wins + p2_wins) != 0 else 0
    p1_wins_percentage_w_draws = (p1_wins / (p1_wins + p2_wins + total_draws)) * 100
    p2_wins_percentage_w_draws = (p2_wins / (p1_wins + p2_wins + total_draws)) * 100
    draws_percentage = (total_draws / (p1_wins + p2_wins + total_draws)) * 100
        
    for i in range(rounds):
        logging.info("============================================================================")
        logging.info("Round: " + str(i+1))
        logging.info("AA won: " + str(results[i][0]) + " /  AE won: " + str(results[i][1]) + " / Draws: " + str(draws[i]))
        logging.info("")
    if percentages:
        logging.info("")
        logging.info("------------ Player Aprendizaje Automatico won " + str(p1_wins) + " times in total ------------")
        logging.info("------------ Player Algoritmos Evolutivos won " + str(p2_wins) + " times in total ------------")
        logging.info("------------ There where " + str(total_draws) + " draws in total ------------")
        logging.info("------------ Player Aprendizaje Automatico won " + str(p1_wins_percentage) + "% of the non-drawn games ------------")
        logging.info("------------ Player Aprendizaje Automatico won " + str(p1_wins_percentage_w_draws) + "% of the games ------------")
        logging.info("------------ Player Algoritmos Evolutivos won " + str(p2_wins_percentage_w_draws) + "% of the games ------------")
        logging.info("------------ There were " + str(draws_percentage) + "% of draws ------------")
