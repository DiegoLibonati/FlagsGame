import { useContext } from "react";

import { UseModeContext } from "@src/entities/hooks";

import { ModeContext } from "@src/contexts/ModeContext/ModeContext";

export const useModeContext = (): UseModeContext => {
  const context = useContext(ModeContext);
  if (!context)
    throw new Error("useModeContext must be used within ModeProvider");
  return context;
};
