import json
import sys

from domain.calcs.calc_no_priorities import no_priority
from domain.calcs.calc_priorities import calc_with_priorities
from models.delivery_point import DeliveryPoint

# todo - necessário considerar que um DeliveryPoint pode receber multiplos pactoes? Para o MVP podemos considerar um pacote fechado, ex: 3 remedios  em um unico pacote para um unico endereço

def main():
    input_json = sys.argv[1]
    data = json.loads(input_json)

    delivery_points = [
        DeliveryPoint(
            id=item['id'],
            title=item['address'],
            lat=item['lat'],
            lng=item['lng'],
            is_priority=item.get('isPriority')
        )
        for item in data["deliveryPoints"]
    ]

    dps = []
    dpsPriority = []

    for item in data["deliveryPoints"]:
        dp = DeliveryPoint(
            id=item['id'],
            title=item['address'],
            lat=item['lat'],
            lng=item['lng'],
            is_priority=item.get('isPriority')
        )

        if item['isPriority']:
            dpsPriority.append(dp)
        else:
            dps.append(dp)

    # se não houver duplas possiveis, desconsiderar priorities
    if len(dpsPriority) == 0 or len(dpsPriority) % 2 != 0:
        dps += dpsPriority
        vehicles = data["vehicles"] if data["vehicles"] else 2

        processed = no_priority(
            delivery_points,
            min_clusters=vehicles["min"],
            max_clusters=vehicles["max"],
        )
    else:
        processed = calc_with_priorities(dpsPriority, dps)

    print(processed)

if __name__ == "__main__":
    main()