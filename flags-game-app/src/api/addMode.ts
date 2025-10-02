import { Mode } from "@src/entities/entities";

import { apiRouteModes } from "@src/api/apiRoute";

export const addMode = (body: Mode): Promise<Response> => {
  return fetch(`${apiRouteModes}/`, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
    },
  });
};
