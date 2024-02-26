import { apiRouteModes } from "./apiRoute";

export const getTopMode = (mode: string): Promise<Response> => {
  return fetch(`${apiRouteModes}/mode/top/${mode}`,{
    method: "get",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
