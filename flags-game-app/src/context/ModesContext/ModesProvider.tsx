import { useCallback, useContext, useEffect, useState } from "react";

import {
  ModesContext as ModesContextT,
  Mode,
  ModesState,
} from "../../entities/entities";

import { ModesContext } from "./ModesContext";
import { getModes } from "../../api/getModes";

interface ModesProviderProps {
  children: React.ReactNode;
}

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

  // Función para obtener modes
  const fetchModes = useCallback(async () => {
    try {
      handleStartFetchModes();
      const response = await getModes();
      const data = await response.json();
      handleSetModes(data.data);
    } catch (error) {
      handleSetErrorModes(String(error));
    } finally {
      handleEndFetchModes();
    }
  }, []);

  useEffect(() => {
    if (!modes.modes.length) fetchModes();

    return () => {
      handleClearModes();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <ModesContext.Provider
      value={{
        modes: modes!,
        handleSetModes: handleSetModes,
        handleClearModes: handleClearModes,
        refreshModes: fetchModes,
      }}
    >
      {children}
    </ModesContext.Provider>
  );
};

export const useModesContext = (): ModesContextT => {
  return useContext(ModesContext)!;
};
