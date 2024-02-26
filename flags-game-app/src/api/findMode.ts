import { apiRouteModes } from "./apiRoute";

export const findMode = (mode: string): Promise<Response> => {
  return fetch(`${apiRouteModes}/findmode/${mode}`,{
    method: "get",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
