import type {DeliveryPointInput} from "@/types/dtos/calculate/delivery-point.input.ts";

export type CalculateInput = {
  vehicles: {
    min: number;
    max: number;
  },
  deliveryPoints: DeliveryPointInput[];
}
