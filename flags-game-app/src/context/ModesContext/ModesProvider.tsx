import { useCallback, useContext, useEffect, useState } from "react";

import { Mode } from "@src/entities/entities";
import { ModesContext as ModesContextT } from "@src/entities/contexts";
import { ModesState } from "@src/entities/states";
import { ModesProviderProps } from "@src/entities/props";

import { ModesContext } from "@src/context/ModesContext/ModesContext";
import { getModes } from "@src/api/getModes";

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
