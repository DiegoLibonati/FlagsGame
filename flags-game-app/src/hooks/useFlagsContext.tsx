import { useContext } from "react";

import { UseFlagsContext } from "@src/entities/hooks";

import { FlagsContext } from "@src/contexts/FlagsContext/FlagsContext";

export const useFlagsContext = (): UseFlagsContext => {
  const context = useContext(FlagsContext);
  if (!context)
    throw new Error("useFlagsContext must be used within FlagsProvider");
  return context;
};
