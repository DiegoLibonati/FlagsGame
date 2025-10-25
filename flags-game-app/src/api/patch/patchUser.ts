import { User } from "@src/entities/app";
import { PatchUserResponse } from "@src/entities/responses";

import { usersApi } from "@src/api/users";

export const patchUser = async (
  body: Pick<User, "username" | "password"> & {
    score: number;
    mode_id: string;
  }
): Promise<PatchUserResponse> => {
  try {
    const response = await fetch(`${usersApi}/`, {
      method: "PATCH",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorData: Pick<PatchUserResponse, "code" | "message"> =
        await response.json();
      throw errorData;
    }

    const data: PatchUserResponse = await response.json();

    return data;
  } catch (e) {
    if (typeof e === "object" && e && "message" in e) throw e.message;
    throw new Error("Network or unexpected error");
  }
};
