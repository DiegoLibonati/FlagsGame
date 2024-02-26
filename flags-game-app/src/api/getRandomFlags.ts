import { apiRouteFlags } from "./apiRoute";

export const getRandomFlags = (mode: string): Promise<Response> => {
  return fetch(`${apiRouteFlags}/${mode}`, {
    method: "get",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
