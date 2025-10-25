import { Mode } from "@src/entities/app";
import { AddModeResponse } from "@src/entities/responses";

import { modesApi } from "@src/api/modes";

export const addMode = async (body: Mode): Promise<AddModeResponse> => {
  try {
    const response = await fetch(`${modesApi}/`, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error adding Mode.");
    }

    const data: AddModeResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error adding Mode: ${e}.`);
  }
};
