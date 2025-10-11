import { DeliveryPointInput } from "./delivery-point.input";

export type CalculateInput = {
  vehicles: {
    min: number;
    max: number;
  },
  deliveryPoints: DeliveryPointInput[];
}
