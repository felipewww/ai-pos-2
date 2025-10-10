from typing import List

from models.delivery_point import DeliveryPoint


class Route:
    def __init__(self, track: List[DeliveryPoint] = None):
        self.track = track if track is not None else []

    def add_point(self, point: DeliveryPoint):
        self.track.append(point)

    def to_dict(self):
        return {
            "deliveryPoints": [
                {
                    "lat":  p.lat,
                    "lng": p.lng
                 } for p in self.track
            ]
        }