from deap import creator, base, tools, algorithms
import random
import numpy as np
import fitness
from board import Board

#constants
n_population = 25
n_generation = 100
n_individuals = 10
n_matches = 10

def main():
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.random)
    toolbox.register("individual", tools.initRepeat, creator.Individual,toolbox.attr_float, n=n_individuals)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluateIndividual)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)
    population = toolbox.population(n_population)
    population, log = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=n_generation)
    #eaSimple more complete 
    #hof = tools.HallOfFame(n_population * n_generation)
    #stats = tools.Statistics(lambda ind: ind.fitness.values)
    #stats.register("avg", np.mean)
    #stats.register("min", np.min)
    #stats.register("max", np.max)
    #population, log = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=n_generation, halloffame=hof, verbose=True)

def evaluateIndividual(individual):
    value = fitness.initGame(individual, n_matches)
    return (value,)


if __name__ == "__main__":
    main()
