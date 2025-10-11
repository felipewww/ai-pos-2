import { Injectable } from '@nestjs/common';
import { DeliveryPointInput } from "./domain/types/delivery-point.input";
import { spawn } from "node:child_process";
import { PyResponse } from "./domain/types/py-response";

@Injectable()
export class AppService {
  async calcRoutes(deliveryPoints: DeliveryPointInput[]): Promise<PyResponse> {

    return new Promise(async (resolve, reject) => {
      const pyFolder = `${__dirname}/../../log-ai`
      const python = spawn(`${pyFolder}/venv/bin/python`, [
        `${pyFolder}/src/app.py`,
        JSON.stringify(deliveryPoints)
      ]);

      let data = "";

      python.stdout.on("data", (chunk) => {
        data += chunk.toString();
      });

      python.stderr.on("data", (err) => {
        console.error("Python error:", err.toString());
      });

      // let result;

      python.on("close", () => {
        try {
          const result = JSON.parse(data) as PyResponse;
          console.log("Resposta do Python:", result);
          resolve(result);
        } catch (e) {
          console.error("Erro ao parsear resposta JSON:", data);
          resolve([])
        }
      });

      // return result;
    })
  }
}
