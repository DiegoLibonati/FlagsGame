import { Flag } from "../entities/entities";
import { apiRouteFlags } from "./apiRoute";

export const addFlag = (body: Flag): Promise<Response> => {
  return fetch(`${apiRouteFlags}/newflag`, {
    method: "post",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
    },
  });
};
