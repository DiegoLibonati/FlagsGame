import { User } from "@src/entities/entities";

import { apiRouteUsers } from "@src/api/apiRoute";

export const addUser = (
  body: Pick<User, "username" | "password"> & {
    score: number;
    mode_id: string;
  },
): Promise<Response> => {
  return fetch(`${apiRouteUsers}/`, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
    },
  });
};
