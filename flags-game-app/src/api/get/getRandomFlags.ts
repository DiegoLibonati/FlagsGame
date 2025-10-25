import { GetRandomFlagsResponse } from "@src/entities/responses";

import { flagsApi } from "@src/api/flags";

export const getRandomFlags = async (
  quantity: number
): Promise<GetRandomFlagsResponse> => {
  try {
    const response = await fetch(`${flagsApi}/random/${quantity}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error fetching random flags.");
    }

    const data: GetRandomFlagsResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error fetching random flags: ${e}.`);
  }
};
