import { apiRouteModes } from "@src/api/apiRoute";

export const getMode = (mode_id: string): Promise<Response> => {
  return fetch(`${apiRouteModes}/${mode_id}`,{
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
