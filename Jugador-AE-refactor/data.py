def initIndividualData(n_individual):
    data = {}
    for index in range(0, n_individual):
        data[index] = {
            "boards": []
        }
    return data
