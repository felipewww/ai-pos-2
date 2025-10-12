# Distância em linha reta entre dois pontos
# utilizado por haversine_distance_matrix
from math import radians, sin, atan2, sqrt, cos
from typing import List

from models.delivery_point import DeliveryPoint


def haversine(p1: DeliveryPoint, p2: DeliveryPoint) -> float:
    # Raio médio da Terra em km
    R = 6371.0

    lat1, lon1 = radians(p1.lat), radians(p1.lng)
    lat2, lon2 = radians(p2.lat), radians(p2.lng)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance # retorna em km

# Distância Matrix em linha reta entre todos os pontos
# Existe uma implementação com google maps distance matrix, mas é muito caro para testes (build_distance_matrix.py)
def haversine_distance_matrix(points: List[DeliveryPoint]) -> List[float]:
    dist_matrix = [
        [haversine(p1, p2) for p2 in points]
        for p1 in points
    ]

    return dist_matrix