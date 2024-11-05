import { apiRouteModes } from "./apiRoute";

export const getModes = (): Promise<Response> => {
  return fetch(`${apiRouteModes}/`, {
    method: "get",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
