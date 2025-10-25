import { createContext, useState } from "react";

import { Mode } from "@src/entities/app";
import { ModeContext as ModeContextT } from "@src/entities/contexts";
import { ModeState } from "@src/entities/states";
import { ModeProviderProps } from "@src/entities/props";

export const ModeContext = createContext<ModeContextT | null>(null);

export const ModeProvider = ({ children }: ModeProviderProps) => {
  // mode
  const [mode, setMode] = useState<ModeState>({
    mode: null,
    error: null,
    loading: false,
  });

  const handleSetMode = (mode: Mode) => {
    setMode((state) => ({
      ...state,
      mode: mode,
    }));
  };

  const handleClearMode = () => {
    setMode({
      mode: null,
      error: null,
      loading: false,
    });
  };

  const handleStartFetchMode = () => {
    setMode((state) => ({
      ...state,
      loading: true,
      error: null,
    }));
  };

  const handleEndFetchMode = () => {
    setMode((state) => ({
      ...state,
      loading: false,
    }));
  };

  const handleSetErrorMode = (error: string) => {
    setMode((state) => ({
      ...state,
      error: error,
    }));
  };

  return (
    <ModeContext.Provider
      value={{
        mode: mode,
        handleClearMode: handleClearMode,
        handleSetMode: handleSetMode,
        handleStartFetchMode: handleStartFetchMode,
        handleEndFetchMode: handleEndFetchMode,
        handleSetErrorMode: handleSetErrorMode,
      }}
    >
      {children}
    </ModeContext.Provider>
  );
};
