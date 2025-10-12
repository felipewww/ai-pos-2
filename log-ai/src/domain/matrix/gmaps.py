from google.maps.routing_v2 import ComputeRouteMatrixRequest
from numpy.f2py.auxfuncs import throw_error

from infra.env import MAPS_API_KEY

import googlemaps
from typing import List
from models.delivery_point import DeliveryPoint

from google.maps import routing
from google.maps.routing import RouteMatrixOrigin, RouteMatrixDestination, Waypoint
from google.protobuf import field_mask_pb2

def gmaps_matrix(points: List[DeliveryPoint]):
    """
    Calcula a matriz de distâncias e duração entre todos os pares de pontos
    usando o método Compute Route Matrix da Google Maps Routes API.
    """

    # O limite de 625 elementos (25x25) geralmente é o máximo seguro para este endpoint.
    MAX_ELEMENTS = 625
    n_points = len(points)

    if n_points * n_points > MAX_ELEMENTS:
        raise Exception(f"Número de pontos ({n_points}) excede o limite de {MAX_ELEMENTS} elementos (n*n). Considere dividir a matriz.")

    # 2. Preparação dos Waypoints (Origens e Destinos)
    # A nova API espera objetos com o formato de Waypoint.

    origins = [
        RouteMatrixOrigin(
            waypoint=Waypoint(location={"lat_lng": {"latitude": pt.lat, "longitude": pt.lng}})
        )
        for pt in points
    ]

    destinations = [
        RouteMatrixDestination(
            waypoint=Waypoint(location={"lat_lng": {"latitude": pt.lat, "longitude": pt.lng}})
        )
        for pt in points
    ]

    # 3. Inicializa o novo cliente da Routes API (não usa a chave no construtor)
    routes_client = routing.RoutesClient(
        client_options={"api_key": MAPS_API_KEY}
    )

    # 4. Define o Field Mask (Mascára de Campo) - OBRIGATÓRIO!
    # Especifica quais informações você quer de volta na resposta para evitar cobranças desnecessárias.
    FIELD_MASK = field_mask_pb2.FieldMask(
        paths=["distance_meters", "duration", "status", "origin_index", "destination_index"]
    )

    field_mask_string = ",".join(FIELD_MASK.paths)

    # Inicializa a matriz de distância
    dist_matrix = [[0.0] * n_points for _ in range(n_points)]

    # print(f"Calculando matriz de {n_points}x{n_points} = {n_points*n_points} elementos...")

    # return [[0, 1235, 741, 1567, 1504, 2059, 1891, 2094, 1862, 2658, 1366, 2399, 1525, 527, 1084, 928, 3401], [1898, 0, 1068, 1713, 785, 1995, 2417, 2240, 1798, 3764, 451, 2636, 1748, 1167, 1410, 634, 3622], [1412, 1154, 0, 1009, 946, 1501, 1410, 1536, 1304, 1946, 1084, 1629, 736, 681, 526, 646, 2615], [2238, 1849, 1009, 0, 950, 1409, 1522, 797, 1212, 2058, 1758, 1741, 262, 1507, 684, 1472, 2102], [2244, 923, 1171, 943, 0, 1372, 2023, 1470, 1175, 2558, 832, 2241, 978, 1514, 421, 981, 3041], [4059, 2922, 2296, 1947, 2115, 0, 3148, 2411, 195, 5974, 2487, 3366, 1981, 2794, 1970, 2758, 3982], [1434, 2110, 1134, 1244, 1753, 2077, 0, 2112, 1880, 974, 2157, 657, 983, 1401, 1333, 1719, 1643], [2765, 2377, 1537, 798, 1478, 1595, 2389, 0, 1398, 2859, 2286, 2001, 1091, 2035, 1212, 2000, 2089], [5011, 3057, 2303, 1954, 2123, 195, 3156, 2419, 0, 5924, 2622, 3374, 1989, 2801, 1978, 2766, 3990], [1030, 2265, 1771, 2256, 2534, 3089, 1934, 2431, 2892, 0, 2396, 844, 2555, 1556, 2114, 1958, 1830], [2380, 617, 1108, 1753, 825, 2035, 3284, 2280, 1838, 3474, 0, 2675, 1788, 1207, 1450, 674, 5391], [2078, 3127, 2611, 1623, 2552, 2670, 1409, 1798, 2472, 1617, 3360, 0, 1618, 2418, 2286, 3074, 1197], [2248, 1884, 736, 262, 984, 1332, 1252, 1090, 1134, 1787, 1792, 1471, 0, 1541, 718, 1506, 2088], [935, 1318, 391, 1478, 1416, 1971, 1525, 2005, 1774, 1799, 1278, 1482, 1159, 0, 995, 840, 2468], [1754, 1497, 526, 684, 421, 1176, 1609, 1210, 979, 2144, 1427, 1827, 718, 1024, 0, 989, 2781], [1371, 632, 646, 1472, 1409, 1964, 2254, 1998, 1767, 2531, 1148, 2214, 1506, 668, 989, 0, 3200], [2918, 3300, 2542, 1978, 2894, 3012, 2296, 1672, 2814, 2713, 3429, 1855, 1850, 2591, 3147, 2991, 0]]

    try:
        request = ComputeRouteMatrixRequest(
            origins=origins,
            destinations=destinations,
            travel_mode=routing.RouteTravelMode.DRIVE,
        )

        # 5. Faz a chamada à API Compute Route Matrix
        # O método retorna um 'stream' (fluxo) de resultados
        route_stream = routes_client.compute_route_matrix(
            # origin=origins,
            # destination=destinations,
            # travel_mode=routing.RouteTravelMode.DRIVE,
            # A máscara de campo é passada em 'request_options'
            # request_options={"x_goog_field_mask": FIELD_MASK}
            request,
            metadata=(("x-goog-fieldmask", field_mask_string),)
        )

        # print('route_stream?????')
        # print(route_stream)
        # print('\n\n')

        # 6. Processa o Stream de Resultados
        for element in route_stream:
            # print(element)
            i = element.origin_index
            j = element.destination_index

            dist_matrix[i][j] = element.distance_meters
            # O status de erro é retornado no objeto element (via código gRPC)
            # if element.status.code == 0:  # Code 0 significa OK
            #     # A distância está em metros, conforme a sua função original
            #     dist_matrix[i][j] = element.distance_meters
            # else:
            #     print(f"Erro ao calcular Origem {i} -> Destino {j}: Status {element.status.message}")
            #     dist_matrix[i][j] = float("inf")

        return dist_matrix

    except Exception as e:
        print(f"Erro na comunicação com a Routes API: {e}")
        raise e