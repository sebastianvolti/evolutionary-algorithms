from deap import creator, base, tools, algorithms
import random
import data
import numpy as np
import argparse
import metrics
from manual_play import manual_play_set
import fitness
import mutation
import constants
import copy
import math
import hof_tournament
import timeit

# py main.py -npop 2 -ngen 1 -nmat 1 -nsel 2 -iter 1 -deb 1 -sm 0
# python3 main.py -npop 10 -ngen 5 -nmat 10 -nsel 5 -iter 5 -sm 1 -minimax 0 

#python3 main.py -npop 10 -ngen 20 -nmat 20 -nsel 5 -iter 2 -sm 1 -minimax 0 -hof_eval 0
#python3 main.py -npop 20 -ngen 20 -nmat 20 -nsel 5 -iter 2 -sm 1 -minimax 0 -hof_eval 0
#python3 main.py -npop 30 -ngen 20 -nmat 20 -nsel 5 -iter 2 -sm 1 -minimax 0 -hof_eval 0
#python3 main.py -npop 40 -ngen 20 -nmat 20 -nsel 5 -iter 2 -sm 1 -minimax 0 -hof_eval 0

# Lee argumentos de entrada
ap = argparse.ArgumentParser(description='Proyecto Final Algoritmos Evolutivos')
ap.add_argument('-npop', '--n_pop', default='10', help='Cantidad de individuos de la población')
ap.add_argument('-ngen', '--n_gen', default='10', help='Indica cantidad de generaciones a realizar')
ap.add_argument('-nmat', '--n_mat', default='20', help='Indica cantidad de partidas a realizar por individuo')
ap.add_argument('-nsel', '--n_sel', default='5', help='Indica cantidad de individuos a seleccionar para nueva generacion')
ap.add_argument('-iter', '--iter', default='2', help='Indica cantidad de iteraciones del algoritmo evolutivo')
ap.add_argument('-pm', '--p_mut', default='0.25', help='Probabilidad de mutación ajuste parámetros ae')
ap.add_argument('-pp', '--p_per', default='0.50', help='Probabilidad de permutación')
ap.add_argument('-rand', '--rand_player', default='0', help='1 para que AA juegue todo aleatorio, 0 para jugar aleatorio cada 5 movs')
ap.add_argument('-deb', '--debug', default='1', help='1 para imprimir info, 0 para no imprimir')
ap.add_argument('-sm', '--show_m', default='1', help='1 para calcular métricas, 0 para no calcular')
ap.add_argument('-pr_games', '--print_games', default='0', help='1 para imprimir los juegos, 0 para no imprimir')
ap.add_argument('-pr_movs', '--print_movs', default='0', help='1 para imprimir los movimientos, 0 para no imprimir')
ap.add_argument('-manual', '--do_manual_play', default='0', help='1 para jugar solo una partida manual, 0 para ejecutar el AE')
ap.add_argument('-minimax', '--do_minimax', default='1', help='1 para que AE use minimax, 0 para que no lo use')
ap.add_argument('-hof_eval', '--do_hof_eval', default='1', help='1 para que se hagan juegos con peso fijo al final con los mejores, 0 para que no se hagan')

weights_for_individual = 10 # CANTIDAD DE COEFICIENTES QUE TIENE CADA INDIVIDUO DE AE
args = vars(ap.parse_args())
n_population = int(args['n_pop'])
n_generation = int(args['n_gen'])
n_matches = int(args['n_mat'])
n_selected = int(args['n_sel'])
n_iter = int(args['iter'])
p_mutation = float(args['p_mut']) 
p_permutation = float(args['p_per'])
full_random = int(args['rand_player'])
debug_mode = int(args['debug']) 
show_metrics = int(args['show_m']) 
print_games = int(args['print_games'])
print_movements = int(args['print_movs'])
manual_play = int(args['do_manual_play']) 
do_minimax = int(args['do_minimax'])
hof_evaluation = int(args['do_hof_eval'])
individual_boards_data = data.initIndividualData(n_population)


def main():
    if manual_play == 0: 
        # Main del Algoritmo Evolutivo 
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        toolbox = base.Toolbox()
        toolbox.register("attr_float", random.random)
        toolbox.register("generateInd", generateIndividual)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.generateInd, 1)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", evaluateIndividual)
        toolbox.register("mate", permutateIndividual)
        toolbox.register("mutate", mutateIndividual)
        toolbox.register("select", tools.selTournament, tournsize=n_selected)

        timeAvg = 0
        hof = tools.HallOfFame(5) # Select 5 best individuals over generations
        stats = tools.Statistics(lambda ind: ind.fitness.values) 
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)
        metrics_over_generations = []
        best_fitness_list = []
        for i in range(n_iter):
            print('\n+++++++++++++++++++++++++++++++++++++++++++ Iteración número: %d +++++++++++++++++++++++++++++++++++++++++++\n' % i)
            population = toolbox.population(n_population)
            generateIndividualsId(population)
            start = timeit.default_timer()
            selected_population, logbook = algorithms.eaSimple(population, toolbox, cxpb=p_permutation, mutpb=p_mutation, ngen=n_generation, stats=stats, halloffame=hof)
            #Your statements here
            stop = timeit.default_timer()
            print('Time: ', stop - start)  
            timeAvg += stop - start
            metrics_over_generations.append((logbook,hof))
            best_fitnnes = getBestFitnessValue(selected_population, i)
            best_fitness_list.append(best_fitnnes)
        if (show_metrics == 1): 
            calculateMetrics(best_fitness_list, metrics_over_generations, timeAvg/2)
        if (hof_evaluation == 1):
            hallOfFameEvaluation(hof, n_matches)
    else: # Se hace un juego manual (usado para estudiar la inteligencia manualmente)
        manual_play_set([0.16505840048581627, 0.3044750422596512, 0.16198595040529404, 0.10777541220873908, 0.638745211045903, 0.27540793477905057, 0.36338448340721374, 0.411896308091403, 0.28257475396970594, 0.2117943026378791],True)
    

def generateIndividual():
    individual = []
    for index in range (0, weights_for_individual):
        individual.append(random.random())
    return (individual,0)

def generateIndividualsId(population):
    new_index = 0
    for elem in population:
        ind, index = elem[0]
        elem[0] = (ind, new_index)
        new_index+=1 

def evaluateIndividual(individual):
    individual_coef, individual_id = individual[0]
    value, individual_boards = fitness.init_game(individual_coef, n_matches, p_mutation, print_games, print_movements, full_random, do_minimax)
    individual_boards_data[individual_id]['boards'] = individual_boards
    return (value,)

def getBestFitnessValue(selected_population, i):
    best_fitnnes = metrics.evaluateSelectedIndividuals(selected_population, n_matches, p_mutation, print_games, print_movements, full_random, do_minimax)
    return best_fitnnes

def calculateMetrics(best_fitness_list, metrics_over_generations, time_avg):
    #metrics.calculateMetrics(best_fitness_list)
    #metrics.metricsOverGenerations(metrics_over_generations)
    metrics.metricsAvgOverGenerations(metrics_over_generations, round(time_avg,2))

#Mutación customizada coeficientes de Jugador AE
def mutateIndividual(individual):
    individual_coef, individual_id = individual[0]
    new_individual = individual_coef
    for ae_board in individual_boards_data[individual_id]['boards']:
        if ae_board != []:
            new_individual = mutation.update_individual(new_individual, ae_board)
    individual[0] = new_individual, individual_id
    return (individual,)

# 'miti-miti': Intercambia la segunda mitad de los pesos del ind_1 por los del ind_2 y la primer mitad de los pesos de ind_2 por los de ind_1
# permutateIndividual([1,2,3,4,5,6,7],[-1,-2,-3,-4,-5,-6,-7]) = [1,2,3,-4,-5,-6,-7] [-1,-2,-3,4,5,6,7]
def permutateIndividual(individual_1, individual_2):
    individual_coef1, individual_id1 = individual_1[0]
    individual_coef2, individual_id2 = individual_2[0]
    half_element = math.floor(len(individual_coef1)/2)
    
    individual_1[0] = (individual_coef1[:half_element] + individual_coef2[half_element:], individual_id1)
    individual_2[0] = (individual_coef2[:half_element] + individual_coef1[half_element:], individual_id2)
    return individual_1, individual_2

# Crea un hijo promediando los pesos de los dos padres
def permutateAverageIndividual(individual_1, individual_2):
    individual_coef1, individual_id1 = individual_1[0]
    individual_coef2, individual_id2 = individual_2[0]
    promedio = []
    medioPromedio = []
    for index in range(len(individual_coef1)):
        promedio.append((individual_coef1[index] + individual_coef2[index]) / 2)
        medioPromedio.append((individual_coef1[index] + individual_coef2[index]) / 4)
    
    individual_1[0] = (promedio, individual_id1)
    individual_2[0] = (medioPromedio, individual_id2)
    return individual_1, individual_2

# Para todos los individuos en el hof, hace N juegos contra oponentes sin inteligencia y contra AA (Todo con pesos fijos) y muestra resultados        
def hallOfFameEvaluation(hof, n_matches):
    hof_tournament.hof_tournament(hof, n_matches, print_games, do_minimax)
        
if __name__ == "__main__":
    main()