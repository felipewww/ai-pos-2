from typing import List

from models.delivery_point import DeliveryPoint


class Route:
    def __init__(
        self,
        track: List[DeliveryPoint] = []
    ):
        self.track = track

    def add_point(
        self,
        point: DeliveryPoint
    ):
        self.track.append(point)