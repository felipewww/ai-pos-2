class DeliveryPoint:
    def __init__(
            self,
            title: str,
            lat: float,
            lng: float,
            is_priority=False,
    ):
        self.title = title
        self.lat = lat
        self.lng = lng