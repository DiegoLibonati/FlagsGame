import { apiRouteFlags } from "@src/api/apiRoute";

export const getFlags = (): Promise<Response> => {
  return fetch(`${apiRouteFlags}/`,{
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
