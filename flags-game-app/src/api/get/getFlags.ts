import { GetFlagsResponse } from "@src/entities/responses";

import { flagsApi } from "@src/api/flags";

export const getFlags = async (): Promise<GetFlagsResponse> => {
  try {
    const response = await fetch(`${flagsApi}/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error fetching flags.");
    }

    const data: GetFlagsResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error fetching flags: ${e}.`);
  }
};
