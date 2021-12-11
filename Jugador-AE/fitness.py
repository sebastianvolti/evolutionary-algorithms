import game

limit_movements = 50

def initGame(individual, n_matches):
    results = game.play(individual, n_matches, True)
    return calculateFitness(results, n_matches)

def calculateFitness(results, n_matches):
    fitness = 0
    for (winner, movements) in results:
        if (winner == 2):
            fitness+=5
            if (movements <= limit_movements):
                fitness+=5
    return fitness/(n_matches*n_matches)