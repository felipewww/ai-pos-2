from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
from typing import List
from sklearn.preprocessing import StandardScaler
from models.delivery_point import DeliveryPoint

def distribute_points_kmeans(
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

    # """
    # A aplicação do StandardScaler foi essencial para normalizar as coordenadas geográficas (latitude e longitude), garantindo que ambas tivessem a mesma escala.
    # Sem esse pré-processamento, o algoritmo K-Means tendia a agrupar todos os pontos em poucos clusters (geralmente 2), pois a diferença entre os eixos distorcia as distâncias euclidianas.
    # Após a padronização, o silhouette score passou a refletir de forma mais fiel a separação espacial dos dados, permitindo a determinação adequada do número de clusters.
    # """
    coords = np.array([[p.lat, p.lng] for p in points])
    coords = StandardScaler().fit_transform(coords)

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