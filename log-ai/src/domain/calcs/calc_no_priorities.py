import json
from typing import List

from domain.distribute_points_kmeans import distribute_points_kmeans
from domain.genetic_algorithm import genetic_algorithm
from domain.matrix.gmaps import gmaps_matrix
from domain.matrix.haversine import haversine_distance_matrix
from infra.env import MATRIX_LIB
from models.delivery_point import DeliveryPoint
from models.route import Route

def no_priority(
        points: List[DeliveryPoint],
        min_clusters = 2,
        max_clusters = 10,
):
    if min_clusters is None:
        min_clusters = 2
    if max_clusters is None:
        max_clusters = 10


    clusters, best_k = distribute_points_kmeans(
        points,
        min_clusters,
        max_clusters,
    )

    routes: List[Route] = []

    for i, cluster in enumerate(clusters.items()):
        points: List[DeliveryPoint] = cluster[1]

        if MATRIX_LIB == 'gmaps':
            matrix = gmaps_matrix(points)
        else:
            matrix = haversine_distance_matrix(points)

        population_size= (len(points) * len(points))

        if population_size > 1000:
            population_size = 1000

        if population_size < 100:
            population_size = 100

        """
        Durante a execução do algoritmo genético, alguns clusters pequenos (com menos de dois genes úteis para o crossover) 
        causavam exceções no processo de recombinação.
        Para evitar isso, adicionou-se uma verificação de tamanho mínimo no operador de crossover, garantindo 
        que apenas indivíduos com número suficiente de genes passem por recombinação, enquanto os demais são 
        preservados por cópia direta.
        """
        if len(points) < 3:
            # não dá pra fazer crossover — usa caminho direto
            best_route = list(range(len(points)))
            # best_distance = calc_total_distance(points)
        else:
            best_route, best_distance = genetic_algorithm(
                matrix,
                population_size,
                generations=100,
                lock_start=False,
                lock_end=False,
            )

        route = Route()
        for best_route_idx in best_route:
            route.add_point(points[best_route_idx])

        routes.append(route)

    json_output = json.dumps([r.to_dict() for r in routes], indent=2)

    return json_output

def calc_total_distance(points: List):
    """
    Calcula a distância total percorrida em uma rota (ordem dos pontos).
    Retorna a distância total em quilômetros.
    """
    if len(points) < 2:
        return 0.0

    total = 0.0
    for i in range(len(points) - 1):
        total += haversine(points[i], points[i + 1])

    return total