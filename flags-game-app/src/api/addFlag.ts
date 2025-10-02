import { Flag } from "@src/entities/entities";

import { apiRouteFlags } from "@src/api/apiRoute";

export const addFlag = (body: Flag): Promise<Response> => {
  return fetch(`${apiRouteFlags}/`, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
    },
  });
};
