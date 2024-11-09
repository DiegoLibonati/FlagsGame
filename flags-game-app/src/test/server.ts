import { RequestHandler } from "msw/lib/core/handlers/RequestHandler";
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";

type HandleConfig = {
  path: string;
  method: "get" | "post" | "delete" | "patch" | "put";
  status?: number;
  res: () => Record<string, unknown> | Record<string, unknown>[];
};

export const createServer = (handlerConfig: HandleConfig[]): void => {
  const handlers: RequestHandler[] = handlerConfig.map((handleConfig) => {
    return http[handleConfig.method](handleConfig.path, () => {
      return HttpResponse.json(handleConfig.res(), {
        status: handleConfig.status ?? 200,
      });
    });
  });

  const server = setupServer(...handlers);

  beforeAll(() => {
    server.listen();
  });
  afterEach(() => {
    server.resetHandlers();
  });
  afterAll(() => {
    server.close();
  });
};
