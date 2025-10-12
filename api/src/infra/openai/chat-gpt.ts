import { OpenAI } from "openai";
import {z, ZodObject} from "zod";
import {zodResponseFormat, zodTextFormat} from "openai/helpers/zod";

export class ChatGpt {
  private openAI: OpenAI;

  constructor() {
    this.openAI = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });
  }

  async chat(
    // message: string,
    // chatId?: string,
    prompt: string,
  ) {
    const schema = z.object({
      conversation: z.string(),
    })

    const instructions = `
        Você é um ótimo avaliador de resultados de algoritimo genético para calculo de rotas e está me auxiliando a planejar melhor meu algoritimo
        para que ele seja o mais efetivo possivel
        `

    return this.openAI.responses.parse({
      // previous_response_id: chatId,
      instructions,
      input: [
        {
          role: "assistant",
          content: prompt,
        },
        // {
        //   role: "assistant",
        //   content: 'Start a friendly English dialogue like daily small talk asking something creative, You could ask the person opinion, talk about goals and dreams, or about the future of humankind, thinking about future, new generation and everything you think is great to start a subject be creative!',
        // },
      ],
      model: 'gpt-4.1-mini',
      text: {
        format: zodTextFormat(schema, "chat"),
      }
    })
  }
}
