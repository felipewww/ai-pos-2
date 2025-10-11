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
                    "id": p.id,
                    "lat":  p.lat,
                    "lng": p.lng,
                    "is_priority": p.is_priority,
                 } for p in self.track
            ]
        }