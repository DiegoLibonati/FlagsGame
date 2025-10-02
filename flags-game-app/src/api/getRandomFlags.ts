import { apiRouteFlags } from "@src/api/apiRoute";

export const getRandomFlags = (quantity: number): Promise<Response> => {
  return fetch(`${apiRouteFlags}/random/${quantity}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
