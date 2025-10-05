import random
import numpy as np

# todo
# escolher o algoritimo correto conforme a quantidade de dados e o resultado de combinações,
# se for apenas 7 pontos o numero de população é baixo (7−1)!/2=360
# para poucos pontos ( < 10 ) não adianta usar AG, é melhor usar força bruta
# para medio ( 20 - 40 pontos ) é melhor começar usar AG, pois o numero de combinações de populaçao aumenta muito

# # --- Função de fitness ---
def calculate_fitness(route, dist_matrix):
    total_dist = 0
    for i in range(len(route) - 1):
        total_dist += dist_matrix[route[i]][route[i+1]]
    total_dist += dist_matrix[route[-1]][route[0]]  # volta ao início
    return total_dist

# # --- Inicialização da população ---
def generate_population(size, num_points):
    population = []
    for _ in range(size):
        route = list(range(num_points))
        random.shuffle(route)
        population.append(route)
    return population

# # --- Seleção por torneio ---
def tournament_selection(population, fitnesses, k=7):
    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]

# # --- Crossover (Order Crossover - OX) ---
def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size
    child[start:end] = parent1[start:end]

    ptr = end
    for i in range(size):
        city = parent2[(end + i) % size]
        if city not in child:
            child[ptr % size] = city
            ptr += 1
    return child

# # --- Mutação (swap) ---
def mutate(route, mutation_rate):
    route = route[:]
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

# ---------- Mutação (2-opt style: inverte segmento) ----------
# def mutate(route, mutation_rate=0.1):
#     route = route[:]
#     if random.random() < mutation_rate:
#         i, j = sorted(random.sample(range(len(route)), 2))
#         route[i:j] = reversed(route[i:j])
#     return route


# ---------- Algoritmo Genético ----------
def genetic_algorithm(
        dist_matrix,
        population_size=300,
        generations=3500,
        mutation_rate=0.01
):
    num_points = len(dist_matrix)
    population = generate_population(population_size, num_points)

    best_route = None
    best_distance = float("inf")

    for gen in range(generations):
        fitnesses = [calculate_fitness(ind, dist_matrix) for ind in population]

        # Melhor da geração
        gen_best_idx = np.argmin(fitnesses)
        gen_best_route = population[gen_best_idx]
        gen_best_distance = fitnesses[gen_best_idx]

        if gen_best_distance < best_distance:
            best_distance = gen_best_distance
            best_route = gen_best_route

        # Nova população com elitismo
        new_population = [best_route]

        print('\n')

        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child = order_crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        print(new_population)

        population = new_population

        # if gen % 25 == 0:
        # print(best_route)
        # print(f"Geração {gen}: melhor distância = {best_distance}")

    return best_route, best_distance
