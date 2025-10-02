import { apiRouteModes } from "@src/api/apiRoute";

export const getModes = (): Promise<Response> => {
  return fetch(`${apiRouteModes}/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
