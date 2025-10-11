import { Body, Controller, Get, Post, Req } from "@nestjs/common";
import { AppService } from './app.service';
import { Responser } from "./infra/responser";
import { DeliveryPointInput } from "./domain/types/calculate/delivery-point.input";
import { CalculateInput } from "./domain/types/calculate/calculate.input";

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get('gkey')
  googleMapsKey() {
    return Responser.send(process.env.GOOGLE_MAPS_API_KEY as string);
  }

  @Post('calculate')
  async calculate(
    @Body() body: CalculateInput
  ) {
    // console.log(body);
    return Responser.send(
      await this.appService.calcRoutes(
        body.deliveryPoints,
        body.vehicles,
      )
    )
  }
}
