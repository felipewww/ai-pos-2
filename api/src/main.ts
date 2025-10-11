import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const originsEnv = process.env.CORS_ORIGINS as string
  const allowedOrigins = originsEnv
    .split(',')
    .map(o => o.trim());

  app.enableCors({
    allowedOrigins,
    origin: (origin, callback) => {
      // Se a origem estiver na lista ou for undefined (ex: ferramentas locais tipo curl/postman)
      if (!origin || allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error(`Origin ${origin} not allowed by CORS`), false);
      }
    },
    credentials: true,
  });

  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
