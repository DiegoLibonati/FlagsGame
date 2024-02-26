import { apiRouteUsers } from "./apiRoute";

export const getTopGeneral = (): Promise<Response> => {
  return fetch(`${apiRouteUsers}/top/general`, {
    method: "get",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
