# Retorna el hijo como el promedio parametro a parametro de los padres
def averageReproduction(individual1, individual2):
    newIndividual = []
    for i in range(len(individual1)):
        newIndividual[i] = (individual1[i] + individual2[i]) / 2
    return newIndividual 

# Retorna el primer individuo luego de intercambiar uno de sus parametros con el otro
def changeOneParameterReproduction(individual1, individual2, changeIndex):
    individual1[changeIndex] = individual2[changeIndex]
    return individual1