import json
import sys
from math import isnan
from typing import List, Tuple

from domain.distribute_points_kmeans import auto_kmeans
from models.delivery_point import DeliveryPoint
from models.package import Package
from domain.genetic_algorithm import genetic_algorithm
from data.points import points_oriente, points_oriente_priority
from haversine import haversine_distance_matrix, pair_points, \
    assign_points_to_pairs_with_radius, haversine
from models.route import Route

# todo - necessário considerar que um DeliveryPoint pode receber multiplos pactoes? Para o MVP podemos considerar um pacote fechado, ex: 3 remedios  em um unico pacote para um unico endereço

pdt1 = Package(
    length=30,
    width=20,
    height=5,
)

def calc_with_priorities(
        priorities: List[DeliveryPoint],
        commons: List[DeliveryPoint],
):
    pairs = pair_points(priorities)
    pairs_aggregated, remaining = assign_points_to_pairs_with_radius(pairs, commons)

    # print('\n')
    # print(f"pairs_aggregated: {len(pairs_aggregated)}")
    # for pair in pairs_aggregated:
    #     print(f"lenpair: {len(pair)}")
    #     for p in pair:
    #         print(f"p: {p.title}")
    #
    # print('\n')
    # print(f"remaining: {len(remaining)}")
    # for p in remaining:
    #     print(f"p: {p.title}")

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
            # print(f"{point.title} - {point.is_priority}")

        routes.append(route)

    json_output = json.dumps([r.to_dict() for r in routes], indent=2)

    return json_output

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

def no_priority(
    points: List[DeliveryPoint],
    min_clusters = 2,
    max_clusters = 10,
):
    if min_clusters is None:
        min_clusters = 2
    if max_clusters is None:
        max_clusters = 10


    clusters, best_k = auto_kmeans(
        points,
        min_clusters,
        max_clusters,
    )

    routes: List[Route] = []

    for i, cluster in enumerate(clusters.items()):
        points: List[DeliveryPoint] = cluster[1]

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
            best_distance = calc_total_distance(points)
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

# no_priority()

def main():
    input_json = sys.argv[1]
    data = json.loads(input_json)

    delivery_points = [
        DeliveryPoint(
            id=item['id'],
            title=item['address'],
            lat=item['lat'],
            lng=item['lng'],
            is_priority=item.get('isPriority')
        )
        for item in data["deliveryPoints"]
    ]

    dps = []
    dpsPriority = []
    for item in data["deliveryPoints"]:
        dp = DeliveryPoint(
            id=item['id'],
            title=item['address'],
            lat=item['lat'],
            lng=item['lng'],
            is_priority=item.get('isPriority')
        )

        if item['isPriority']:
            dpsPriority.append(dp)
        else:
            dps.append(dp)

    # se não houver duplas possiveis, desconsiderar priorities
    if len(dpsPriority) == 0 or len(dpsPriority) % 2 != 0:
        dps += dpsPriority
        vehicles = data["vehicles"] if data["vehicles"] else 2

        processed = no_priority(
            delivery_points,
            min_clusters=vehicles["min"],
            max_clusters=vehicles["max"],
        )
    else:
        processed = calc_with_priorities(dpsPriority, dps)

    print(processed)

if __name__ == "__main__":
    main()