from typing import List, Tuple
from math import radians, sin, cos, sqrt, atan2

from models.delivery_point import DeliveryPoint

# Distância em linha reta entre dois pontos
# utilizado por haversine_distance_matrix
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

# Cria um retângulo entre 2 lat/long e busca pontos dentro deste retângulo
# deprecated, mas seria uma opção de busca de pontos menor que radius
def points_in_area(points: List[DeliveryPoint]) -> tuple[List[DeliveryPoint], List[DeliveryPoint]]:
    if len(points) < 2:
        return [], []

    start = points[0]
    end = points[-1]

    # limites do retângulo (bounding box)
    min_lat = min(start.lat, end.lat)
    max_lat = max(start.lat, end.lat)
    min_lng = min(start.lng, end.lng)
    max_lng = max(start.lng, end.lng)

    inside, outside = [], []
    for p in points:
        if min_lat <= p.lat <= max_lat and min_lng <= p.lng <= max_lng:
            inside.append(p)
        else:
            outside.append(p)

    return inside, outside

def points_in_radius(points: List[DeliveryPoint], radius_km=0.3) -> tuple[List[DeliveryPoint], List[DeliveryPoint]]:
    if len(points) < 2:
        return [], []

    start = points[0]
    end = points[-1]

    inside, outside = [], []
    for p in points:
        dist_start = haversine(start, p)
        dist_end = haversine(end, p)

        # entra se estiver dentro do raio de pelo menos um dos dois
        if dist_start <= radius_km or dist_end <= radius_km:
            inside.append(p)
        else:
            outside.append(p)

    return inside, outside

# Formar pares de rotas mais próximas para pontos prioritários
# que definirão o início e fim de uma rota inicial (2 prioridade mergeadas com comuns)
def pair_points(points) -> List[Tuple[DeliveryPoint, DeliveryPoint]]:
    # todo
    # Aqui seria uma melhoria do sistema, caso as prioridades sejam número impar, poderíamos
    # extrair uma entrega comum mais próxima do remaining (usando haversine) e considerá-la como
    # prioritária apena para fechar a dupla
    if len(points) % 2 != 0:
        raise ValueError("Número de pontos deve ser par para formar duplas exatas")

    remaining = points[:]  # copia da lista
    pairs = []

    while len(remaining) > 1:
        best_dist = float("inf")
        best_pair = (None, None)

        # procurar a dupla mais próxima
        for i in range(len(remaining)):
            for j in range(i+1, len(remaining)):
                d = haversine(remaining[i], remaining[j])
                if d < best_dist:
                    best_dist = d
                    best_pair = (i, j)

        i, j = best_pair
        p1, p2 = remaining[i], remaining[j]
        # pairs.append((p1, p2, best_dist))
        pairs.append((p1, p2))

        # remover os dois pontos da lista
        for idx in sorted([i, j], reverse=True):
            remaining.pop(idx)

    return pairs


def assign_points_to_pairs_with_radius(
        pairs: List[Tuple[DeliveryPoint, DeliveryPoint]],
        candidates: List[DeliveryPoint],
        radius_km=0.3
) -> Tuple[List[List[DeliveryPoint]], List[DeliveryPoint]]:
    """
    pairs: lista de tuplas (p1, p2)
    candidates: pontos extras
    radius_km: raio em km
    """

    routes = []
    used = set()
    # used = []

    for (p1, p2) in pairs:
        # rota inicial = a dupla
        # route = [p1, p2]
        route = []

        # candidatos que ainda não foram usados
        unused_candidates = [c for idx, c in enumerate(candidates) if idx not in used]

        inside, outside = points_in_radius([p1, p2] + unused_candidates, radius_km)

        # removemos p1 e p2 da lista "inside" (eles sempre estão dentro)
        inside = [p for p in inside if p not in (p1, p2)]

        # adiciona os pontos dentro do raio
        for c in inside:
            route.append(c)
            used.add(candidates.index(c))
            # used.append(c)

        route = [p1] + route + [p2]

        routes.append(route)

    # remaining = candidatos que nunca foram usados
    remaining = [c for idx, c in enumerate(candidates) if idx not in used]

    return routes, remaining