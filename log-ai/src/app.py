from typing import List, Tuple

from models.delivery_point import DeliveryPoint
from models.package import Package
from build_distance_matrix import build_route_matrix
from domain.genetic_algorithm import genetic_algorithm
from data.points import points_oriente, points_satelite, points_oriente_priority
from haversine import haversine_distance_matrix, points_in_area, points_in_radius, pair_points, \
    assign_points_to_pairs_with_radius
from models.route import Route

# todo - necessário considerar que um DeliveryPoint pode receber multiplos pactoes? Para o MVP podemos considerar um pacote fechado, ex: 3 remedios  em um unico pacote para um unico endereço

pdt1 = Package(
    length=30,
    width=20,
    height=5,
)

def main(
        # self,
        priorities: List[DeliveryPoint],
        commons: List[DeliveryPoint],
):
    pairs = pair_points(priorities)

    pairs_aggregated, remaining = assign_points_to_pairs_with_radius(pairs, commons)

    # o último ponto de entrega de cada rota será usado para calcular a distribuição de rotas restantes (remaining)
    last_points: List[DeliveryPoint] = []

    print('\n')
    for pair_ag in pairs_aggregated:
        matrix = haversine_distance_matrix(pair_ag)
        # aqui nao precisamos travar o start e endpoint, eles serão os priorities e teremos poucas entregas entre eles
        best_route, best_distance = genetic_algorithm(
            matrix,
            population_size=len(pair_ag) * len(pair_ag), # poderiamos usar força bruta, pois aqui temos poucas rotas entre priority A e Z
            generations=100,
            lock_start=False,
            lock_end=False,
        )

        last_points.append(pair_ag[best_route[-1]])
        # last_point = pair_ag[best_route[-1]]

    pairs_final = distribute_remaining_with_ga(
        pairs_aggregated,
        remaining,
        last_points,
    )

    for pair_final in pairs_final:
        print('\npair final matrix....')
        print(pair_final)
        for point in pair_final:
            print(f"{point.title} - {point.is_priority}")

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

    if len(remaining):
        raise Exception('Remaining is not cleared')

    return new_routes


main(
    priorities=points_oriente_priority,
    commons=points_oriente
)
    # for route in pair:
    #     # print(len(route))
    #     print(f"- {route.title}")

# jd satelite
# -23.222092, -45.885470- rua pedro tursi, 301
# -23.220456, -45.893967 - Rua Polar, 100
# -23.225819, -45.888817 - Rua aldebaram, 2
# -23.232030, -45.889525 - rua nazaré, 829
# -23.225839, -45.894160 - rua scorpius, 800
# -23.230275, -45.895791 - rua joao de paula, 189
# -23.228829, -45.881087 - rua tijuca, 442

# print(pdt1.width)