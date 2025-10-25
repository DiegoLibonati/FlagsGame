import { GetModeResponse } from "@src/entities/responses";

import { modesApi } from "@src/api/modes";

export const getMode = async (mode_id: string): Promise<GetModeResponse> => {
  try {
    const response = await fetch(`${modesApi}/${mode_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error fetching mode.");
    }

    const data: GetModeResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error fetching mode: ${e}.`);
  }
};
