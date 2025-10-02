import { User } from "@src/entities/entities";

import { apiRouteUsers } from "@src/api/apiRoute";

export const patchUser = (
  body: Pick<User, "username" | "password"> & {
    score: number;
    mode_id: string;
  }
): Promise<Response> => {
  return fetch(`${apiRouteUsers}/`, {
    method: "PATCH",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
    },
  });
};
