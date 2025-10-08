import random
from typing import List

import numpy as np

# todo
# escolher o algoritimo correto conforme a quantidade de dados e o resultado de combinações,
# se for apenas 7 pontos o numero de população é baixo (7−1)!/2=360
# para poucos pontos ( < 10 ) não adianta usar AG, é melhor usar força bruta
# para medio ( 20 - 40 pontos ) é melhor começar usar AG, pois o numero de combinações de populaçao aumenta muito

# --- Função de fitness ---
def calculate_fitness(route, dist_matrix):
    total_dist = 0
    for i in range(len(route) - 1):
        total_dist += dist_matrix[route[i]][route[i+1]]
    total_dist += dist_matrix[route[-1]][route[0]]  # volta ao início
    return total_dist

# --- Inicialização da população ---
# def generate_population(size, num_points, start_point=0):
#     population = []
#     other_points = [i for i in range(num_points) if i != start_point]
#
#     for _ in range(size):
#         route = [start_point] + random.sample(other_points, len(other_points))
#         population.append(route)
#     return population

# def generate_population(
#         size,
#         num_points,
#         start_point=True,
#         end_point=True,
# ):
#     population = []
#     all_points = list(range(num_points))
#
#     # etapa 1: separa start fixo
#     fixed_start = []
#     middle = all_points[:]
#     if start_point:
#         fixed_start = all_points[0]
#         middle = all_points[1:]
#
#     # etapa 2: separa end fixo
#     fixed_end = []
#     if end_point:
#         fixed_end = middle[-1]
#         middle = middle[:-1]
#
#     print("middle", middle)
#
#     # etapa 3: monta rotas
#     for _ in range(size):
#         route = random.sample(middle, len(middle))
#
#         if start_point:
#             route.insert(fixed_start, 0)
#
#         if end_point:
#             route.append(fixed_end)
#         # route = fixed_start + random.sample(middle, len(middle)) + fixed_end
#         population.append(route)
#
#     return population

def generate_population(
        size,
        num_points,
        lock_start=True,
        lock_end=True,
):
    population = []
    all_points = list(range(num_points))

    # fixa start
    fixed_start = None
    middle = all_points[:]
    if lock_start:
        fixed_start = all_points[0]
        middle = all_points[1:]

    # fixa end
    fixed_end = None
    if lock_end:
        fixed_end = middle[-1]
        middle = middle[:-1]

    for _ in range(size):
        route = random.sample(middle, len(middle))

        if lock_start:
            route = [fixed_start] + route
        if lock_end:
            route = route + [fixed_end]

        population.append(route)

    return population

# --- Seleção por torneio ---
def tournament_selection(population, fitnesses, k=7):
    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]

def order_crossover(parent1, parent2, lock_start=True, lock_end=True):
    size = len(parent1)

    # ajusta índices de corte para não pegar start/end
    start_idx = 1 if lock_start else 0
    end_idx = size - 2 if lock_end else size - 1

    start, end = sorted(random.sample(range(start_idx, end_idx+1), 2))

    child = [None] * size

    # preserva start e end fixos
    if lock_start:
        child[0] = parent1[0]
    if lock_end:
        child[-1] = parent1[-1]

    # copia fatia intermediária
    child[start:end] = parent1[start:end]

    # preenche com genes do segundo pai, respeitando start/end
    ptr = end
    for i in range(size):
        point = parent2[(end + i) % size]
        if point not in child:
            while child[ptr % size] is not None:
                ptr += 1
            child[ptr % size] = point

    return child

# --- Mutação (swap) ---
# def mutate(route, mutation_rate):
#     route = route[:]
#     if random.random() < mutation_rate:
#         i, j = random.sample(range(len(route)), 2)
#         route[i], route[j] = route[j], route[i]
#     return route

# ---------- Mutação (2-opt style: inverte segmento) ----------
# def mutate(route, mutation_rate=0.5):
#     route = route[:]
#     if random.random() < mutation_rate:
#         i, j = sorted(random.sample(range(len(route)), 2))
#         route[i:j] = reversed(route[i:j])
#     return route

def mutate(
        route,
        mutation_rate=0.1,
        lock_start=False,
        lock_end=False,
):
    route2 = route[:]
    if random.random() < mutation_rate:
        start_idx = 1 if lock_start else 0
        # end_idx = len(route) - 2 if lock_end else len(route) - 1
        end_idx = len(route) - 1 if lock_end else len(route) - 2
        i, j = sorted(random.sample(range(start_idx, end_idx+1), 2))
        # route[i:j] = reversed(route[i:j])
        route2[i:j] = reversed(route2[i:j])
    return route2

# ---------- Algoritmo Genético ----------
def genetic_algorithm(
        dist_matrix: List[float],
        population_size=700, # população em 70 o reusltado é muito melhor, porque? o mesmo para generations e mutation_rate
        generations=200,
        mutation_rate=0.9,
        lock_start=False,
        lock_end=False,
):
    # print("Start point?", start_point)
    num_points = len(dist_matrix)
    population = generate_population(
        population_size,
        num_points,
        lock_start,
        lock_end,
    )

    # print('all population')
    # for inner_array in population:
    #     print(inner_array)

    # return
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

        # elitismo com 5%
        # elite_size = max(1, population_size // 20)  # 5%
        # elite_indices = np.argsort(fitnesses)[:elite_size]
        # new_population = [population[i] for i in elite_indices]

        # print('\n')

        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child = order_crossover(parent1, parent2, lock_start, lock_end)
            child = mutate(
                child,
                mutation_rate,
                lock_start,
                lock_end,
            )
            new_population.append(child)

        population = new_population

        if gen % 5 == 0:
            print(best_route)
            print(f"Geração {gen}: melhor distância = {best_distance}")


    return best_route, best_distance
