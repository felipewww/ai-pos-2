import json
from typing import List

from domain.genetic_algorithm import genetic_algorithm
from domain.matrix.gmaps import gmaps_matrix
from domain.matrix.haversine import haversine_distance_matrix
from domain.points_aggregators import pair_points, assign_points_to_pairs_with_radius
from infra.env import MATRIX_LIB
from models.delivery_point import DeliveryPoint
from models.route import Route


def calc_with_priorities(
        priorities: List[DeliveryPoint],
        commons: List[DeliveryPoint],
):
    pairs = pair_points(priorities)
    pairs_aggregated, remaining = assign_points_to_pairs_with_radius(pairs, commons)

    last_points: List[DeliveryPoint] = []

    for pair_ag in pairs_aggregated:
        # matrix = haversine_distance_matrix(pair_ag)
        if MATRIX_LIB == 'gmaps':
            matrix = gmaps_matrix(pair_ag)
        else:
            matrix = haversine_distance_matrix(pair_ag)

        # aqui não precisamos travar o start e endpoint, eles serão os priorities e teremos poucas entregas entre eles
        best_route, best_distance, fit_history = genetic_algorithm(
            matrix,
            population_size=len(pair_ag) * len(pair_ag), # poderiamos usar força bruta, pois aqui temos poucas rotas entre priority 1 e 2
            generations=300,
            lock_start=False,
            lock_end=False,
        )

        last_points.append(pair_ag[best_route[-1]])

    pairs_final, remaining = distribute_remaining_with_ga(
        pairs_aggregated,
        remaining,
        last_points,
    )

    routes: List[Route] = []

    for pair_final in pairs_final:
        route = Route()
        for point in pair_final:
            route.add_point(point)
            # print(f"{point.title} - {point.is_priority}")

        routes.append(route)

    route.add_info({
        # "best_route_idx": best_route_idx,
        "population_size": None,
        "fit_history": fit_history,
    })

    output = {
        "routes": [r.to_dict() for r in routes],
        # "best_route": best_route,
        # "best_distance": best_distance,
        # "fit_history": fit_history,
    }

    return json.dumps(output)

def distribute_remaining_with_ga(
        pairs_aggregated: List[List[DeliveryPoint]],
        remaining: List[DeliveryPoint],
        last_points: List[DeliveryPoint],
        generations: int = 80
) -> List[List[DeliveryPoint]]:
    """
    Distribui os remainings entre os pares usando GA como critério de seleção.
    """
    num_pairs = len(pairs_aggregated)

    total_rem = len(remaining)
    base_count = total_rem // num_pairs
    sobra = total_rem % num_pairs  # alguns pares terão +1

    new_routes = []

    for i, pair in enumerate(pairs_aggregated):
        if not remaining:
            new_routes.append(pair)
            continue

        # quantos esse par deve pegar
        k = base_count + (1 if i < sobra else 0)

        # pontos disponíveis para otimizar
        points_to_optimize = [last_points[i]] + remaining

        # matriz de distâncias
        # matrix = haversine_distance_matrix(points_to_optimize)
        if MATRIX_LIB == 'gmaps':
            matrix = gmaps_matrix(points_to_optimize)
        else:
            matrix = haversine_distance_matrix(points_to_optimize)

        best_route, best_distance, fit_history = genetic_algorithm(
            matrix,
            population_size=len(points_to_optimize) * len(points_to_optimize),
            generations=generations,
            lock_start=True,
            lock_end=False,
        )

        # reconstruir ordem de pontos reais
        ordered_points = [points_to_optimize[j] for j in best_route]

        # pegar apenas os k primeiros após o last_point
        selected = ordered_points[1 : 1 + k]

        # atualiza rota
        new_routes.append(pair + selected)

        # remove os selecionados do remaining
        remaining = [p for p in remaining if p not in selected]

    # if len(remaining):
    #     raise Exception('Remaining is not cleared')

    return new_routes, remaining