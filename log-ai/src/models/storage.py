from .delivery_point import DeliveryPoint

class Storage:
    def __init__(
            self,
            length: float,
            width: float,
            height: float,
            # deliveryPoint: DeliveryPoint
    ):
        self.length = length
        self.width = width
        self.height = height
        self.volume = self.calculate_volume()

    def calculate_volume(self):
        return self.length * self.width * self.height