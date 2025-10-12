import type {DeliveryPoint} from "@/types/delivery-point.ts";

export class RouteCalc {
    public showing = false;
    public readonly points: DeliveryPoint[] = [];

    constructor(
        public readonly id: number,
        public readonly color: string,
        // public readonly points: DeliveryPoint[],
    ) {
    }

    addDeliveryPoint(deliveryPoint: DeliveryPoint) {
        this.points.push(deliveryPoint);
        deliveryPoint.assignRoute(this);
    }
}
