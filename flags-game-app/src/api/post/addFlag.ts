import { Flag } from "@src/entities/app";
import { AddFlagResponse } from "@src/entities/responses";

import { flagsApi } from "@src/api/flags";

export const addFlag = async (body: Flag): Promise<AddFlagResponse> => {
  try {
    const response = await fetch(`${flagsApi}/`, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error adding Flag.");
    }

    const data: AddFlagResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error adding Flag: ${e}.`);
  }
};
