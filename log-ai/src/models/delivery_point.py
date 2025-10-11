from typing import List
from models.package import Package

class DeliveryPoint:
    def __init__(
            self,
            title: str,
            lat: float,
            lng: float,
            is_priority=False,
            packages: List[Package] = [],
            id: str = 'AAAZZZ',
    ):
        self.title = title
        self.lat = lat
        self.lng = lng
        self.is_priority = is_priority
        self.id = id