import { GetModesResponse } from "@src/entities/responses";

import { modesApi } from "@src/api/modes";

export const getModes = async (): Promise<GetModesResponse> => {
  try {
    const response = await fetch(`${modesApi}/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error fetching modes.");
    }

    const data: GetModesResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error fetching modes: ${e}.`);
  }
};
