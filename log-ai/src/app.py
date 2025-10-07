from models.storage import Storage
from models.delivery_point import DeliveryPoint
from build_distance_matrix import build_route_matrix
from domain.genetic_algorithm import genetic_algorithm

# todo - necessário considerar que um DeliveryPoint pode receber multiplos pactoes? Para o MVP podemos considerar um pacote fechado, ex: 3 remedios  em um unico pacote para um unico endereço

pdt1 = Storage(
    length=30,
    width=20,
    height=5,
)

points = [
    # Jd. Satélite
    DeliveryPoint(
        title="rua pedro tursi, 301",
        lat=-23.222092,
        lng=-45.885470
    ),
    DeliveryPoint(
        title="rua Polar, 100",
        lat=-23.220456,
        lng=-45.893967,
    ),
    DeliveryPoint(
        title="rua aldebaram, 2",
        lat=-23.225819,
        lng=-45.888817,
    ),
    DeliveryPoint(
        title="rua nazaré, 829",
        lat=-23.232030,
        lng=-45.889525,
    ),
    DeliveryPoint(
        title="rua scorpius, 800",
        lat=-23.225839,
        lng=-45.894160,
    ),
    DeliveryPoint(
        title="rua joao de paula, 189",
        lat=-23.230275,
        lng=-45.895791,
    ),
    DeliveryPoint(
        title="rua tijuca, 442",
        lat=-23.228829,
        lng=-45.881087,
    ),
    DeliveryPoint(
        title="R. Divinópolis, 2-196 - Bosque dos Eucaliptos",
        lat=-23.237525,
        lng=-45.890879,
    ),
    DeliveryPoint(
        title="R. San Marino, 81-169 - Jardim America",
        lat=-23.231288,
        lng=-45.895774,
    ),
    DeliveryPoint(
        title="R. Osvaldo Faria, 365-191 - Jardim Satélite",
        lat=-23.226893,
        lng=-45.879383,
    ),
    DeliveryPoint(
        title="R. Pleiades, 111-1 - Jardim Satélite",
        lat=-23.221031,
        lng=-45.895959,
    ),
    DeliveryPoint(
        title="R. Maranduba, 2-156 - Jardim Satélite",
        lat=-23.232992,
        lng=-45.881497,
    ),
    DeliveryPoint(
        title="R. Ipiau, 162-408 - Jardim Satélite",
        lat=-23.230846,
        lng=-45.888061,
    ),
    DeliveryPoint(
        title="R. Vírgem, 377-175 - Jardim Satélite",
        lat=-23.225325,
        lng=-45.886689,
    ),
    DeliveryPoint(
        title="R. Crater, 437-231 - Jardim Satélite",
        lat=-23.227301,
        lng=-45.891361,
    ),
    DeliveryPoint(
        title="R. Cisne, 179-1 - Jardim Satélite",
        lat=-23.221202,
        lng=-45.891324,
    ),
    DeliveryPoint(
        title="R. Newton Viêira Novaes, 2-170 - Bosque dos Eucaliptos",
        lat=-23.241682,
        lng=-45.882831,
    ),
]

# todo - limitar em 25 points, se ultrapassar, fazer multiplas reqs e depois mergear os resultados
# matrix = build_distance_matrix(points)
matrix = build_route_matrix(points)

print(matrix)

genetic_algorithm(
    matrix,
    lock_start=True,
    lock_end=True,
)

# jd satelite
# -23.222092, -45.885470- rua pedro tursi, 301
# -23.220456, -45.893967 - Rua Polar, 100
# -23.225819, -45.888817 - Rua aldebaram, 2
# -23.232030, -45.889525 - rua nazaré, 829
# -23.225839, -45.894160 - rua scorpius, 800
# -23.230275, -45.895791 - rua joao de paula, 189
# -23.228829, -45.881087 - rua tijuca, 442

# print(pdt1.width)