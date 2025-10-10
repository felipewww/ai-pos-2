import json
from typing import List, Tuple

from domain.distribute_points_kmeans import distribute_points_with_kmeans, clusterize_kmeans, auto_kmeans
from models.delivery_point import DeliveryPoint
from models.package import Package
from domain.genetic_algorithm import genetic_algorithm
from data.points import points_oriente, points_oriente_priority
from haversine import haversine_distance_matrix, pair_points, \
    assign_points_to_pairs_with_radius
from models.route import Route

# todo - necessário considerar que um DeliveryPoint pode receber multiplos pactoes? Para o MVP podemos considerar um pacote fechado, ex: 3 remedios  em um unico pacote para um unico endereço

pdt1 = Package(
    length=30,
    width=20,
    height=5,
)

def main(
        priorities: List[DeliveryPoint],
        commons: List[DeliveryPoint],
):
    pairs = pair_points(priorities)
    pairs_aggregated, remaining = assign_points_to_pairs_with_radius(pairs, commons)

    # o último ponto de entrega de cada rota prioritária será usado
    # para calcular a distribuição de rotas restantes (remaining)
    last_points: List[DeliveryPoint] = []

    for pair_ag in pairs_aggregated:
        matrix = haversine_distance_matrix(pair_ag)
        # aqui não precisamos travar o start e endpoint, eles serão os priorities e teremos poucas entregas entre eles
        best_route, best_distance = genetic_algorithm(
            matrix,
            population_size=len(pair_ag) * len(pair_ag), # poderiamos usar força bruta, pois aqui temos poucas rotas entre priority 1 e 2
            generations=100,
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
            print(f"{point.title} - {point.is_priority}")

        routes.append(route)

    json_output = json.dumps([r.to_dict() for r in routes], indent=2)

    print(json_output)

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
        print('\n')
        print('calculating remainings....')
        print(remaining)
        if not remaining:
            new_routes.append(pair)
            continue

        # quantos esse par deve pegar
        k = base_count + (1 if i < sobra else 0)

        # pontos disponíveis para otimizar
        points_to_optimize = [last_points[i]] + remaining

        # matriz de distâncias
        matrix = haversine_distance_matrix(points_to_optimize)

        best_route, _ = genetic_algorithm(
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


# main(
#     priorities=points_oriente_priority,
#     commons=points_oriente
# )

# clusters = clusterize_kmeans(
#     points_oriente_priority + points_oriente
# )

# clusters = distribute_points_with_kmeans(
#     points_oriente_priority + points_oriente
# )

def no_priority():
    clusters, best_k = auto_kmeans(
        points=points_oriente_priority + points_oriente,
        min_clusters=4,
        # points_oriente
    )

    routes: List[Route] = []
    #
    # for cluster in enumerate(clusters.items()):
    #     route = Route()
    #     for point in pair_final:
    #         route.add_point(point)
    #         print(f"{point.title} - {point.is_priority}")
    #
    #     routes.append(route)
    #
    # json_output = json.dumps([r.to_dict() for r in routes], indent=2)
    #
    # print(json_output)

    for i, cluster in enumerate(clusters.items()):
        print('\n')
        points: List[DeliveryPoint] = cluster[1]
        print(f'cluster {i} len {len(points)}')

        matrix = haversine_distance_matrix(points)

        population_size= (len(points) * len(points))

        if population_size > 1000:
            population_size = 1000

        best_route, best_distance = genetic_algorithm(
            matrix,
            population_size,
            generations=100,
            lock_start=False,
            lock_end=False,
        )

        print(best_route)

        route = Route()
        for best_route_idx in best_route:
            print(f'{points[best_route_idx].title}')
            route.add_point(points[best_route_idx])

        routes.append(route)

        # print(f'best route: {best_route} - best distance: {best_distance}')
    json_output = json.dumps([r.to_dict() for r in routes], indent=2)

    print(json_output)

no_priority()