from models.storage import Storage
from build_distance_matrix import build_route_matrix
from domain.genetic_algorithm import genetic_algorithm
from data.points import points_oriente, points_satelite, points_oriente_priority
from haversine import haversine_distance_matrix, points_in_area, points_in_radius, pair_points, \
    assign_points_to_pairs_with_radius

# todo - necessário considerar que um DeliveryPoint pode receber multiplos pactoes? Para o MVP podemos considerar um pacote fechado, ex: 3 remedios  em um unico pacote para um unico endereço

pdt1 = Storage(
    length=30,
    width=20,
    height=5,
)

# def distribute_packages():


# todo - limitar em 25 points, se ultrapassar, fazer multiplas reqs e depois mergear os resultados
# matrix = build_distance_matrix(points)
# matrix = build_route_matrix(points_oriente)
# matrix = haversine_distance_matrix(points_satelite)
# print(matrix)

# todo - Pegar um array somente com as rotas prioritarias, calcular o havesine

# genetic_algorithm(
#     matrix,
#     lock_start=True,
#     lock_end=True,
# )

# todo - primeiro, calcular a menor distancia entre 3 prioridade, se forem só 2, não precisa calcular.
# todo - pegar as 2 mais curtas, iserir num array com todas as outras (inclusive a  ignorada)

# inside, outside = points_in_radius(points_oriente)
#
# print("Dentro do retângulo:")
# for p in inside:
#     print(f"- {p.title}")
#
# print("\nFora do retângulo:")
# for p in outside:
#     print(f"- {p.title}")

pairs = pair_points(points_oriente_priority)

# print(pairs)
# for pair in pairs:
#     print('pair....')
#     for point in pair:
#         print(f"- {point.title}")

routes, remaining = assign_points_to_pairs_with_radius(pairs, points_oriente)

print(routes)
print('\nremaining')
print(remaining)
# jd satelite
# -23.222092, -45.885470- rua pedro tursi, 301
# -23.220456, -45.893967 - Rua Polar, 100
# -23.225819, -45.888817 - Rua aldebaram, 2
# -23.232030, -45.889525 - rua nazaré, 829
# -23.225839, -45.894160 - rua scorpius, 800
# -23.230275, -45.895791 - rua joao de paula, 189
# -23.228829, -45.881087 - rua tijuca, 442

# print(pdt1.width)