import type {DeliveryPoint} from "@/types/delivery-point.ts";
import type {DeliveryPointInput} from "@/types/dtos/delivery-point.input.ts";

export class ApiService {
    private apiUrl = import.meta.env.VITE_API_URL

    async getGmapsKey() {
        return fetch(`${this.apiUrl}/gkey`, {
            method: 'GET',
        })
    }

    async calculateRoutes(deliveryPoints: DeliveryPointInput[]) {
        return fetch(`${this.apiUrl}/calculate`, {
            method: 'POST',
            body: JSON.stringify({deliveryPoints}),
            headers: {
                // 'Accept': 'application/json',
                'content-type': 'application/json'
            }
        })
    }
}
