from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
from typing import List, Dict, Tuple
from math import ceil

from models.delivery_point import DeliveryPoint


def distribute_points_with_kmeans(
        delivery_points: List[DeliveryPoint],
        k_min: int = 2,
        k_max: int = 10,
        random_state: int = 42,
) -> Dict[int, List[DeliveryPoint]]:
    """
    Distribui pontos de entrega (DeliveryPoints) em clusters (veículos) usando K-Means.
    Descobre automaticamente o número ótimo de clusters via silhouette score.
    """

    if len(delivery_points) < k_min:
        raise ValueError("Número de pontos insuficiente para clusterização.")

    # Monta a matriz de coordenadas
    X = np.array([[p.lat, p.lng] for p in delivery_points])

    # 🔹 Determinar o melhor número de clusters (K)
    best_k = k_min
    best_score = -1
    for k in range(k_min, min(k_max, len(delivery_points)) + 1):
        kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10).fit(X)
        # silhouette só faz sentido se houver mais de 1 cluster distinto
        if len(set(kmeans.labels_)) > 1:
            score = silhouette_score(X, kmeans.labels_)
            if score > best_score:
                best_k, best_score = k, score

    print(f"➡️ Melhor número de veículos: {best_k} (silhouette={best_score:.3f})")

    # 🔹 Clusterização final
    kmeans = KMeans(n_clusters=best_k, random_state=random_state, n_init=10).fit(X)
    clusters = {i: [] for i in range(best_k)}

    for i, label in enumerate(kmeans.labels_):
        clusters[label].append(delivery_points[i])

    return clusters

# def distribute_points_with_kmeans(
#         delivery_points: List[DeliveryPoint],
#         k_min: int = 2,
#         k_max: int = 10,
#         random_state: int = 42,
#         balance: bool = True,
# ) -> Dict[int, List[DeliveryPoint]]:
#     print(f'total points: {len(delivery_points)}')
#     """
#     Distribui DeliveryPoints em clusters (veículos) via K-Means, determinando o melhor número de clusters automaticamente
#     e balanceando o tamanho dos grupos para que fiquem próximos em quantidade.
#
#     Retorna: {cluster_id: [DeliveryPoint, ...]}
#     """
#
#     if len(delivery_points) < k_min:
#         raise ValueError("Número de pontos insuficiente para clusterização.")
#
#     X = np.array([[p.lat, p.lng] for p in delivery_points])
#
#     # Determinar o melhor número de clusters (K)
#     best_k = k_min
#     best_score = -1
#     for k in range(k_min, min(k_max, len(delivery_points)) + 1):
#         kmeans = KMeans(n_clusters=k, random_state=random_state, n_init="auto").fit(X)
#         if len(set(kmeans.labels_)) > 1:
#             score = silhouette_score(X, kmeans.labels_)
#             if score > best_score:
#                 best_k, best_score = k, score
#
#     print(f"➡️ Melhor número de veículos (clusters): {best_k} (silhouette={best_score:.3f})")
#
#     # Rodar o KMeans final
#     kmeans = KMeans(n_clusters=best_k, random_state=random_state, n_init="auto").fit(X)
#     labels = kmeans.labels_
#     centroids = kmeans.cluster_centers_
#
#     # Montar clusters iniciais
#     clusters = {i: [] for i in range(best_k)}
#     for idx, label in enumerate(labels):
#         clusters[label].append(delivery_points[idx])
#
#     # Balancear se necessário
#     if balance:
#         clusters = balance_clusters(clusters, centroids)
#
#     return clusters


def balance_clusters(
        clusters: Dict[int, List[DeliveryPoint]],
        centroids: np.ndarray,
) -> Dict[int, List[DeliveryPoint]]:
    """
    Redistribui pontos para que os clusters tenham tamanhos mais equilibrados,
    mantendo a proximidade com o centroide.
    """

    all_points = [p for c in clusters.values() for p in c]
    n_clusters = len(clusters)
    target_size = ceil(len(all_points) / n_clusters)

    # Ordena clusters por tamanho
    sorted_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)
    balanced = {cid: pts[:] for cid, pts in clusters.items()}

    for cid, pts in sorted_clusters:
        while len(balanced[cid]) > target_size:
            # Remove o ponto mais distante do centroide
            distances = [
                np.linalg.norm(
                    np.array([p.lat, p.lng]) - centroids[cid]
                )
                for p in balanced[cid]
            ]
            farthest_idx = int(np.argmax(distances))
            point_to_move = balanced[cid].pop(farthest_idx)

            # Encontra o cluster mais próximo com espaço disponível
            candidate_clusters = {
                i: np.linalg.norm(
                    np.array([point_to_move.lat, point_to_move.lng]) - centroids[i]
                )
                for i in range(n_clusters)
                if len(balanced[i]) < target_size
            }
            if candidate_clusters:
                new_cid = min(candidate_clusters, key=candidate_clusters.get)
                balanced[new_cid].append(point_to_move)

    return balanced

def clusterize_kmeans(
        points: List[DeliveryPoint],
        n_clusters: int = 8
):
    """
    Clusteriza DeliveryPoints por latitude/longitude usando KMeans do scikit-learn.

    :param points: lista de objetos DeliveryPoint
    :param n_clusters: número de clusters (mínimo 2)
    :return: dicionário {cluster_id: [DeliveryPoint, ...]}
    """
    if n_clusters < 2:
        raise ValueError("O número mínimo de clusters é 2")

    # Converter coordenadas para array numpy
    coords = np.array([[p.lat, p.lng] for p in points])

    # Executar o KMeans
    kmeans = KMeans(n_clusters=n_clusters, n_init="auto", random_state=42)
    labels = kmeans.fit_predict(coords)

    # Agrupar resultados
    clusters = {}
    for label, point in zip(labels, points):
        clusters.setdefault(label, []).append(point)

    return clusters

# def auto_kmeans(points: List[DeliveryPoint], max_clusters: int = 10):
#     """
#     Clusteriza automaticamente DeliveryPoints sem duplicações.
#     Cada ponto pertence a um único cluster.
#     """
#     if len(points) < 2:
#         raise ValueError("É necessário pelo menos 2 pontos para clusterizar")
#
#     coords = np.array([[p.lat, p.lng] for p in points])
#
#     best_k = 2
#     best_score = -1
#     best_labels = None
#
#     # Testa k de 2 até max_clusters
#     for k in range(2, min(max_clusters, len(points)) + 1):
#         kmeans = KMeans(n_clusters=k, n_init="auto", random_state=42)
#         labels = kmeans.fit_predict(coords)
#         score = silhouette_score(coords, labels)
#
#         if score > best_score:
#             best_k = k
#             best_score = score
#             best_labels = labels
#
#     # Garante que cada ponto está em apenas 1 cluster
#     clusters = {i: [] for i in range(best_k)}
#     for idx, label in enumerate(best_labels):
#         clusters[label].append(points[idx])
#
#     return clusters, best_k

def auto_kmeans(
        points: List[DeliveryPoint],
        min_clusters: int = 2,
        max_clusters: int = 10
):
    """
    Clusteriza automaticamente DeliveryPoints, escolhendo o melhor número de clusters (K)
    entre min_clusters e max_clusters com base no melhor silhouette score.

    :param points: lista de DeliveryPoint
    :param min_clusters: número mínimo de clusters (>= 2)
    :param max_clusters: número máximo de clusters a testar
    :return: (clusters: dict, best_k: int)
    """
    n_points = len(points)
    if n_points < 2:
        raise ValueError("É necessário pelo menos 2 pontos para clusterizar")
    if min_clusters < 2:
        raise ValueError("min_clusters deve ser >= 2")
    if max_clusters < min_clusters:
        raise ValueError("max_clusters deve ser >= min_clusters")

    coords = np.array([[p.lat, p.lng] for p in points])

    best_k = min_clusters
    best_score = -1
    best_labels = None

    for k in range(min_clusters, min(max_clusters, n_points) + 1):
        if k >= n_points:  # não faz sentido mais clusters que pontos
            break
        kmeans = KMeans(n_clusters=k, n_init="auto", random_state=42)
        labels = kmeans.fit_predict(coords)
        # silhouette só é válido se houver pelo menos 2 clusters distintos
        if len(set(labels)) > 1:
            score = silhouette_score(coords, labels)
            if score > best_score:
                best_k = k
                best_score = score
                best_labels = labels

    if best_labels is None:
        # fallback: todos em um cluster (raro, só se os pontos forem idênticos)
        best_labels = np.zeros(n_points, dtype=int)

    clusters = {i: [] for i in range(best_k)}
    for idx, label in enumerate(best_labels):
        clusters[label].append(points[idx])

    return clusters, best_k