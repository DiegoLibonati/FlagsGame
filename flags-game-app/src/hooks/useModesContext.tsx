import { useContext } from "react";

import { UseModesContext } from "@src/entities/hooks";

import { ModesContext } from "@src/contexts/ModesContext/ModesContext";

export const useModesContext = (): UseModesContext => {
  const context = useContext(ModesContext);
  if (!context)
    throw new Error("useModesContext must be used within ModesProvider");
  return context;
};
