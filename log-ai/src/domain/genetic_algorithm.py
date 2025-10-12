import random
from typing import List
import numpy as np

# Calcula o "fitness" (aptidão) de uma rota.
# Nesse caso, é a distância total percorrida somando as distâncias entre
# todos os pontos e retornando ao ponto inicial.
# Quanto MENOR o valor retornado, MELHOR é a rota.
def calculate_fitness(route, dist_matrix):
    total_dist = 0
    for i in range(len(route) - 1):
        total_dist += dist_matrix[route[i]][route[i+1]]
    total_dist += dist_matrix[route[-1]][route[0]]  # volta ao início
    return total_dist

# Gera a população inicial do algoritmo genético.
# Cada indivíduo (rota) é uma permutação aleatória dos pontos.
# Se lock_start=True ou lock_end=True, o primeiro e/ou último ponto são fixos
# (útil para manter uma origem e destino fixos, como início/fim de uma entrega).
def generate_population(
        size,
        num_points,
        lock_start=True,
        lock_end=True,
):
    population = []
    all_points = list(range(num_points))

    fixed_start = None
    middle = all_points[:]
    if lock_start:
        fixed_start = all_points[0]
        middle = all_points[1:]

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

# Seleciona um indivíduo para reprodução usando "torneio".
# Escolhe k indivíduos aleatórios e retorna o que tem melhor fitness (menor distância).
# Essa técnica mantém diversidade, mas ainda favorece os melhores.
def tournament_selection(population, fitnesses, k=7):
    # garante que k não ultrapasse o tamanho da população
    k = min(k, len(population))
    if k <= 0:
        raise ValueError("População vazia — impossível selecionar indivíduos.")

    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]

# Executa o cruzamento (crossover) entre dois pais para gerar um novo filho.
# Usa o método "Order Crossover" (OX):
# 1. Copia um trecho contínuo do primeiro pai.
# 2. Completa o restante com a ordem dos pontos do segundo pai,
#    sem repetir elementos.
# Mantém start/end fixos se indicado.
def order_crossover(parent1, parent2, lock_start=True, lock_end=True):
    size = len(parent1)

    # ajusta índices de corte para não pegar start/end
    start_idx = 1 if lock_start else 0
    end_idx = size - 2 if lock_end else size - 1

    # garante que há ao menos 2 posições para amostragem
    if end_idx - start_idx < 1:
        # fallback: sem cruzamento, apenas copia o parent1
        return parent1.copy()

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

# Executa mutação em uma rota com certa probabilidade (mutation_rate).
# A mutação inverte a ordem de um trecho aleatório da rota (2-opt simples).
# Mantém o primeiro e/ou último ponto fixo se lock_start/end forem True.
# Serve para evitar que a população convirja prematuramente.
def mutate(
        route,
        mutation_rate=0.1,
        lock_start=False,
        lock_end=False,
):
    route2 = route[:]
    if random.random() < mutation_rate:
        start_idx = 1 if lock_start else 0
        end_idx = len(route) - 2 if lock_end else len(route) - 1
        # end_idx = len(route) - 1 if lock_end else len(route) - 2

        # garante que há pelo menos 2 posições possíveis
        if end_idx - start_idx < 1:
            # não há espaço suficiente para mutação
            return route2

        i, j = sorted(random.sample(range(start_idx, end_idx+1), 2))
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
    num_points = len(dist_matrix)
    population = generate_population(
        population_size,
        num_points,
        lock_start,
        lock_end,
    )

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

        # if gen % 5 == 0:
        #     print(best_route)
        #     print(f"Geração {gen}: melhor distância = {best_distance}")

    return best_route, best_distance
