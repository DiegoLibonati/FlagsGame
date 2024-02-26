import { apiRouteFlags } from "./apiRoute";

export const getFlags = (): Promise<Response> => {
  return fetch(`${apiRouteFlags}/`,{
    method: "get",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
