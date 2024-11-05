import { useContext, useState } from "react";

import {
  ModesContext as ModesContextT,
  ModesProviderProps,
  Mode,
} from "../../entities/entities";

import { ModesContext } from "./ModesContext";

export const ModesProvider = ({ children }: ModesProviderProps) => {
  // Modes
  const [modes, setModes] = useState<Mode[] | null>(null);

  const handleSetModes = (modes: Mode[]) => {
    setModes(modes);
  };

  const handleClearModes = () => {
    setModes(null);
  };

  // ActualMode
  const [actualMode, setActualMode] = useState<Mode | null>(null);

  const handleSetActualMode = (mode: Mode) => {
    setActualMode(mode);
  };

  const handleClearActualMode = () => {
    setActualMode(null);
  };

  return (
    <ModesContext.Provider
      value={{
        actualMode: actualMode!,
        modes: modes!,
        handleSetActualMode: handleSetActualMode,
        handleSetModes: handleSetModes,
        handleClearModes: handleClearModes,
        handleClearActualMode: handleClearActualMode,
      }}
    >
      {children}
    </ModesContext.Provider>
  );
};

export const useModesContext = (): ModesContextT => {
  return useContext(ModesContext)!;
};
