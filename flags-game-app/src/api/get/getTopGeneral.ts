import { usersApi } from "@src/api/users";

import { GetTopGeneralResponse } from "@src/entities/responses";

export const getTopGeneral = async (): Promise<GetTopGeneralResponse> => {
  try {
    const response = await fetch(`${usersApi}/top_global`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error fetching Top General.");
    }

    const data: GetTopGeneralResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error fetching Top General: ${e}.`);
  }
};
