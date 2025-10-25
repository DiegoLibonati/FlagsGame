import { useContext } from "react";

import { UseGameContext } from "@src/entities/hooks";

import { GameContext } from "@src/contexts/GameContext/GameContext";

export const useGameContext = (): UseGameContext => {
  const context = useContext(GameContext);
  if (!context)
    throw new Error("useGameContext must be used within GameProvider");
  return context;
};
