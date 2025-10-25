import { GetTopModeResponse } from "@src/entities/responses";

import { modesApi } from "@src/api/modes";

export const getTopMode = async (
  mode_id: string
): Promise<GetTopModeResponse> => {
  try {
    const response = await fetch(`${modesApi}/${mode_id}/top`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error fetching Top Mode.");
    }

    const data: GetTopModeResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error fetching Top Mode: ${e}.`);
  }
};
