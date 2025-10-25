import { createContext, useState } from "react";

import { Mode } from "@src/entities/app";
import { ModesContext as ModesContextT } from "@src/entities/contexts";
import { ModesState } from "@src/entities/states";
import { ModesProviderProps } from "@src/entities/props";

export const ModesContext = createContext<ModesContextT | null>(null);

export const ModesProvider = ({ children }: ModesProviderProps) => {
  // Modes
  const [modes, setModes] = useState<ModesState>({
    modes: [],
    error: null,
    loading: false,
  });

  const handleSetModes = (modes: Mode[]) => {
    setModes((state) => ({
      ...state,
      modes: modes,
    }));
  };

  const handleClearModes = () => {
    setModes({
      modes: [],
      error: null,
      loading: false,
    });
  };

  const handleStartFetchModes = () => {
    setModes((state) => ({
      ...state,
      loading: true,
      error: null,
    }));
  };

  const handleEndFetchModes = () => {
    setModes((state) => ({
      ...state,
      loading: false,
    }));
  };

  const handleSetErrorModes = (error: string) => {
    setModes((state) => ({
      ...state,
      error: error,
    }));
  };

  return (
    <ModesContext.Provider
      value={{
        modes: modes!,
        handleSetModes: handleSetModes,
        handleClearModes: handleClearModes,
        handleStartFetchModes: handleStartFetchModes,
        handleEndFetchModes: handleEndFetchModes,
        handleSetErrorModes: handleSetErrorModes,
      }}
    >
      {children}
    </ModesContext.Provider>
  );
};
