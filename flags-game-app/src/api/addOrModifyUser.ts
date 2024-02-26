import { User } from "../entities/entities";
import { apiRouteUsers } from "./apiRoute";

export const addOrModifyUser = (
  body: {
    username: string;
    password: string;
    score: number;
    mode_name: string;
  },
  method: string
): Promise<Response> => {
  return fetch(`${apiRouteUsers}/addormodify`, {
    method: method,
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
    },
  });
};
