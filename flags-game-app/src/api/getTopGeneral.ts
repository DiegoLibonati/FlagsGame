import { apiRouteUsers } from "@src/api/apiRoute";

export const getTopGeneral = (): Promise<Response> => {
  return fetch(`${apiRouteUsers}/top_global`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
