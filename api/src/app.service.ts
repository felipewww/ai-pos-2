import { Injectable } from '@nestjs/common';
import { DeliveryPointInput } from "./domain/types/calculate/delivery-point.input";
import { spawn } from "node:child_process";
import { PyResponse } from "./domain/types/py-response";
import { lambda, LambdaReq } from "./infra/lambda";
import { ChatGpt } from './infra/openai/chat-gpt';

type CalcResponse = {
  conversation: string,
} & PyResponse

@Injectable()
export class AppService {
  async calcRoutes(
    deliveryPoints: DeliveryPointInput[],
    vehicles: { min: number, max: number }
  ): Promise<CalcResponse> {

    if (!vehicles.min) {
      vehicles.min = null;
    }
    if (!vehicles.max) {
      vehicles.max = null;
    }

    const pyReq: LambdaReq = {
      deliveryPoints,
      vehicles,
    };

    const result = await lambda(pyReq);

    const pointsCountByRoute = []
    const history = result.routes.map((route) => {
      pointsCountByRoute.push(route.deliveryPoints.length)
      return route.info.fit_history
    })

    const prompt = `
    Meu algoritimo genetico calculou rotas para ${deliveryPoints.length} pontos de entrega e 
    gerou ${result.routes.length} rotas dividindo os pontos de entrega em ${pointsCountByRoute.join(',')} respectivamente.
    
    analisando o histórico do cálculo de fitness de cada rota, como considera que foi a qualidade do resultado?
    
    historico:
    ${JSON.stringify(history)}
    `

    console.log('\n\nprompt???')
    console.log(prompt)
    console.log('\n\nprompt???')

    const chatGPT = new ChatGpt()
    const gptAnswer = await chatGPT.chat(prompt)

    console.log(gptAnswer)

    return {
      routes: result.routes,
      conversation: gptAnswer.output_parsed.conversation
    };
  }
}
