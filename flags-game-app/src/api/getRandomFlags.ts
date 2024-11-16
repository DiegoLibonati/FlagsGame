import { apiRouteFlags } from "./apiRoute";

export const getRandomFlags = (quantity: number): Promise<Response> => {
  return fetch(`${apiRouteFlags}/random/${quantity}`, {
    method: "get",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
