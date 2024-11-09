import { Mode } from "../entities/entities";

import { apiRouteModes } from "./apiRoute";

export const addMode = (body: Mode): Promise<Response> => {
  return fetch(`${apiRouteModes}/newmode`, {
    method: "post",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
    },
  });
};
