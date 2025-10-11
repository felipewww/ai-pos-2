import type {CalculateInput} from "@/types/dtos/calculate/calculate.input.ts";

export class ApiService {
    private apiUrl = import.meta.env.VITE_API_URL

    async getGmapsKey() {
        return fetch(`${this.apiUrl}/gkey`, {
            method: 'GET',
        })
    }

    async calculateRoutes(body: CalculateInput) {
        return fetch(`${this.apiUrl}/calculate`, {
            method: 'POST',
            body: JSON.stringify(body),
            headers: {
                // 'Accept': 'application/json',
                'content-type': 'application/json'
            }
        })
    }
}
