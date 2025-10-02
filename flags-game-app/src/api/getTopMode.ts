import { apiRouteModes } from "@src/api/apiRoute";

export const getTopMode = (mode_id: string): Promise<Response> => {
  return fetch(`${apiRouteModes}/${mode_id}/top`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
