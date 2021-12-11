import fitness
import statistics
import matplotlib.pyplot as plt
import seaborn as sns

def evaluateSelectedIndividuals(selected_population, n_matches, p_mutation, print_games, print_movements, full_random, do_minimax):
    fitness_list = []
    for individual in selected_population:
        individual_coef, individual_id = individual[0]
        value, individual_boards  = fitness.init_game(individual_coef, n_matches, p_mutation, print_games, print_movements, full_random, do_minimax)
        fitness_list.append(value)
    return float(max(fitness_list))

def calculateMetrics(best_fitness_list):
    calculateAverage(best_fitness_list)
    calculateSD(best_fitness_list)

def calculateAverage(best_fitness_list):
    avg = statistics.mean(best_fitness_list)
    print("Valor de fitness más alto promedio a lo largo de las iteraciones: " + str(avg))

def calculateSD(best_fitness_list):
    #Standar Desviation required at least 2 elems, 2 iterations of eaSimple
    if len(best_fitness_list) > 1 :
        sd = statistics.stdev(best_fitness_list)
        print("Desviación estándar del fitness a lo largo de las iteraciones: " + str(sd))

def metricsOverGenerations(metrics_over_generations):
    iteration = 0
    for (logbook,hof) in metrics_over_generations:

        best = hof.items[0]
        minFitnessValues, maxFitnessValues, stdFitnessValues, meanFitnessValues = logbook.select("min","max", "std", "avg")
        print("Iteration " + str(iteration) + ":")
        print("Best Ever Individual = ", best)
        print("Best Ever Fitness = ", best.fitness.values[0])
        print("minFitnessValues-->" + str(minFitnessValues))
        print("maxFitnessValues-->" + str(maxFitnessValues))
        print("stdFitnessValues-->" + str(stdFitnessValues))
        print("meanFitnessValues-->" + str(meanFitnessValues))

        sns.set_style("whitegrid")
        plt.plot(meanFitnessValues, color='green')
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.title('Iteration ' + str(iteration) + ', Average Fitness over Generations')
        plt.show() 

        sns.set_style("whitegrid")
        plt.plot(minFitnessValues, color='red')
        plt.plot(maxFitnessValues, color='blue')
        plt.xlabel('Generation')
        plt.ylabel('Min/Max Fitness')
        plt.title('Iteration ' + str(iteration) + ',Min/Max Fitness over Generations')
        plt.show() 
        
        sns.set_style("whitegrid")
        plt.plot(stdFitnessValues, color='red')
        plt.xlabel('Generation')
        plt.ylabel('Standar Desviation')
        plt.title('Iteration ' + str(iteration) + ',Standar Desviation over Generations')
        plt.show() 
        
        iteration+=1

def metricsAvgOverGenerations(metrics_over_generations, time_avg):

    size = len(metrics_over_generations)
    minAvgFitnessValues = []
    maxAvgFitnessValues = []
    stdAvgFitnessValues = []
    meanAvgFitnessValues = []

    for (logbook,hof) in metrics_over_generations:
        minFitnessValues, maxFitnessValues, stdFitnessValues, meanFitnessValues = logbook.select("min","max", "std", "avg")
        if (minAvgFitnessValues == maxAvgFitnessValues == stdAvgFitnessValues == meanAvgFitnessValues == []):
            minAvgFitnessValues = minFitnessValues
            maxAvgFitnessValues = maxFitnessValues
            stdAvgFitnessValues = stdFitnessValues
            meanAvgFitnessValues = meanFitnessValues
        else:
            minAvgFitnessValues = [x + y for x, y in zip(minAvgFitnessValues, minFitnessValues)]
            maxAvgFitnessValues = [x + y for x, y in zip(minAvgFitnessValues, maxFitnessValues)]
            stdAvgFitnessValues = [x + y for x, y in zip(minAvgFitnessValues, stdFitnessValues)]
            meanAvgFitnessValues = [x + y for x, y in zip(minAvgFitnessValues, meanFitnessValues)]

    minAvgFitnessValues = [x/size for x in minAvgFitnessValues]
    maxAvgFitnessValues = [x/size for x in maxAvgFitnessValues]
    stdAvgFitnessValues = [x/size for x in stdAvgFitnessValues]
    meanAvgFitnessValues = [x/size for x in meanAvgFitnessValues]

    # sns.set_style("whitegrid")
    # plt.plot(meanFitnessValues, color='green')
    # plt.xlabel('Generation')
    # plt.ylabel('Average Fitness')
    # plt.title('Average Fitness over Generations, Average over Iterations')
    # plt.show() 

    # sns.set_style("whitegrid")
    # plt.plot(minFitnessValues, color='red')
    # plt.plot(maxFitnessValues, color='blue')
    # plt.xlabel('Generation')
    # plt.ylabel('Min/Max Fitness')
    # plt.title('Min/Max Fitness over Generations, Average over Iterations')
    # plt.show() 
    
    # sns.set_style("whitegrid")
    # plt.plot(stdFitnessValues, color='red')
    # plt.xlabel('Generation')
    # plt.ylabel('Standar Desviation')
    # plt.title('Standar Desviation over Generations, Average over Iterations')
    # plt.show() 

    sns.set_style("whitegrid")
    plt.plot(meanFitnessValues, color='green')
    plt.plot(minFitnessValues, color='red')
    plt.plot(maxFitnessValues, color='blue')
    plt.plot(stdFitnessValues, color='orange')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Min/Max/Avg/SD Fitness over Generations, average over 5 iterations, ' + str(time_avg) + 's')
    plt.show() 
    
        