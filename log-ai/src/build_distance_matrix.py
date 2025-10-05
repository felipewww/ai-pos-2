from infra.env import MAPS_API_KEY

import googlemaps
from typing import List
from models.delivery_point import DeliveryPoint

def build_distance_matrix(points: List[DeliveryPoint]):
    gmaps = googlemaps.Client(key=MAPS_API_KEY)

    coords = [f"{pt.lat},{pt.lng}" for pt in points]
    n = len(points)
    dist_matrix = [[0.0] * n for _ in range(n)]

    max_batch_size = 25  # Limite da API

    print(dist_matrix)

    # for i in range(0, n, max_batch_size):
        # origins = coords[i:i + max_batch_size]
    #
    #     for j in range(0, n, max_batch_size):
    #         destinations = coords[j:j + max_batch_size]
    #
    #         response = gmaps.distance_matrix(
    #             origins=origins,
    #             destinations=destinations,
    #             mode="driving"
    #         )
    #
    #         for oi, row in enumerate(response["rows"]):
    #             origin_index = i + oi
    #             for di, element in enumerate(row["elements"]):
    #                 dest_index = j + di
    #                 if element["status"] == "OK":
    #                     dist_matrix[origin_index][dest_index] = element["distance"]["value"]
    #                 else:
    #                     dist_matrix[origin_index][dest_index] = float("inf")

    return dist_matrix