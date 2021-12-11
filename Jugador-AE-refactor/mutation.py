def update_individual(weights_list, aa_board_attrs_history):
    training_set = generate_training_set(aa_board_attrs_history, weights_list) # Genero el conjunto de entrenamiento con historial de tableros del jugador de AA para una partida
    updated_weights = lms(weights_list, training_set) # Aplico lms para ajustar los valores de los coeficientes, en base al conjunto de entrenamiento dado
    return updated_weights

def lms(weights, training_set):
    mu = 0.1
    for attrs, vt_board in training_set:
        vop = 0
        for i, attr in enumerate(attrs):
            vop += attr * weights[i]
        for i, weight in enumerate(weights):
            weights[i] = abs(weight + mu * (vt_board - vop) * attrs[i])
    return weights


def generate_training_set(game_attrs_history, weights):
    training_set = []
    gamma = 0.9
    value = 1
    last_board = True
    for i, board_attrs in enumerate(reversed(game_attrs_history)):
        if i != 0:
            if last_board:
                training_set.append((board_attrs,value))
                last_board = False
            else:
                value = gamma * value
                training_set.append((board_attrs,value))
    return training_set