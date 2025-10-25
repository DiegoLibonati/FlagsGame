import { User } from "@src/entities/app";
import { AddUserResponse } from "@src/entities/responses";

import { usersApi } from "@src/api/users";

export const addUser = async (
  body: Pick<User, "username" | "password"> & {
    score: number;
    mode_id: string;
  }
): Promise<AddUserResponse> => {
  try {
    const response = await fetch(`${usersApi}/`, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorData: Pick<AddUserResponse, "code" | "message"> =
        await response.json();
      throw errorData;
    }

    const data = await response.json();

    return data;
  } catch (e) {
    if (typeof e === "object" && e && "message" in e) throw e.message;
    throw new Error("Network or unexpected error");
  }
};
