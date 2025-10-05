from models.storage import Storage
from models.delivery_point import DeliveryPoint
from build_distance_matrix import build_distance_matrix

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
    )
]

build_distance_matrix(points)

# jd satelite
# -23.222092, -45.885470- rua pedro tursi, 301
# -23.220456, -45.893967 - Rua Polar, 100
# -23.225819, -45.888817 - Rua aldebaram, 2
# -23.232030, -45.889525 - rua nazaré, 829
# -23.225839, -45.894160 - rua scorpius, 800
# -23.230275, -45.895791 - rua joao de paula, 189
# -23.228829, -45.881087 - rua tijuca, 442

# print(pdt1.width)