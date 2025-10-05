from infra.env import MAPS_API_KEY

import googlemaps
from typing import List
from models.delivery_point import DeliveryPoint

def build_distance_matrix(points: List[DeliveryPoint]):
    gmaps = googlemaps.Client(key=MAPS_API_KEY)

    # Lista de coordenadas em formato aceito pela API
    coords = [f"{pt.lat},{pt.lng}" for pt in points]
    n = len(points)
    dist_matrix = [[0.0] * n for _ in range(n)]

    # Uma chamada só com todas as origens e destinos
    # response = gmaps.distance_matrix(
    #     origins=coords,
    #     destinations=coords,
    #     mode="driving"
    # )
    #
    # for i, row in enumerate(response["rows"]):
    #     for j, element in enumerate(row["elements"]):
    #         if element["status"] == "OK":
    #             dist_matrix[i][j] = element["distance"]["value"]  # metros
    #         else:
    #             dist_matrix[i][j] = float("inf")
    #
    # return dist_matrix

    mock = [
        [0, 1235, 741, 1567, 1504, 2059, 1891],
        [1898, 0, 1068, 1713, 785, 1995, 2417],
        [1412, 1154, 0, 1009, 946, 1501, 1410],
        [2238, 1849, 1009, 0, 950, 1409, 1522],
        [2244, 923, 1171, 943, 0, 1372, 2023],
        [4059, 2922, 2296, 1947, 2115, 0, 3148],
        [1434, 2110, 1134, 1244, 1753, 2077, 0]
    ]

    return mock