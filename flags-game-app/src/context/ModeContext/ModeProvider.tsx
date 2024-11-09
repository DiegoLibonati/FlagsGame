import { useCallback, useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  ModeContext as ModeContextT,
  Mode,
  ModeState,
} from "../../entities/entities";

import { ModeContext } from "./ModeContext";
import { findMode } from "../../api/findMode";

interface ModeProviderProps {
  children: React.ReactNode;
}

export const ModeProvider = ({ children }: ModeProviderProps) => {
  // 3RD
  const { mode: modeName } = useParams();

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

  // Función para obtener un mode especifico
  const fetchMode = useCallback(async () => {
    try {
      handleStartFetchMode();
      const response = await findMode(modeName!);
      const data = await response.json();
      handleSetMode(data.data);
    } catch (error) {
      handleSetErrorMode(String(error));
    } finally {
      handleEndFetchMode();
    }
  }, []);

  useEffect(() => {
    fetchMode();

    return () => {
      handleClearMode();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <ModeContext.Provider
      value={{
        mode: mode,
        handleClearMode: handleClearMode,
        handleSetMode: handleSetMode,
        refreshMode: fetchMode,
      }}
    >
      {children}
    </ModeContext.Provider>
  );
};

export const useModeContext = (): ModeContextT => {
  return useContext(ModeContext)!;
};
