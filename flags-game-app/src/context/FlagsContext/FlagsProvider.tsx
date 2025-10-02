import { useCallback, useContext, useEffect, useState } from "react";

import { Flag } from "@src/entities/entities";
import { FlagsContext as FlagsContextT } from "@src/entities/contexts";
import { FlagsState } from "@src/entities/states";
import { FlagsProviderProps } from "@src/entities/props";

import { FlagsContext } from "@src/context/FlagsContext/FlagsContext";
import { getRandomFlags } from "@src/api/getRandomFlags";

export const FlagsProvider = ({ children }: FlagsProviderProps) => {
  // Flags
  const [flags, setFlags] = useState<FlagsState>({
    flags: [],
    error: null,
    loading: false,
  });

  const handleSetFlags = (flags: Flag[]) => {
    setFlags((state) => ({
      ...state,
      flags: flags,
    }));
  };

  const handleClearFlags = () => {
    setFlags({
      flags: [],
      error: null,
      loading: false,
    });
  };

  const handleStartFetchFlags = () => {
    setFlags((state) => ({
      ...state,
      loading: true,
      error: null,
    }));
  };

  const handleEndFetchFlags = () => {
    setFlags((state) => ({
      ...state,
      loading: false,
    }));
  };

  const handleSetErrorFlags = (error: string) => {
    setFlags((state) => ({
      ...state,
      error: error,
    }));
  };

  // Función para obtener las flags
  const fetchFlags = useCallback(async () => {
    try {
      handleStartFetchFlags();
      const response = await getRandomFlags(5);
      const data = await response.json();
      handleSetFlags(data.data);
    } catch (error) {
      handleSetErrorFlags(String(error));
    } finally {
      handleEndFetchFlags();
    }
  }, []);

  useEffect(() => {
    fetchFlags();

    return () => {
      handleClearFlags();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <FlagsContext.Provider
      value={{
        flags: flags!,
        handleSetFlags: handleSetFlags,
        handleClearFlags: handleClearFlags,
        refreshFlags: fetchFlags,
      }}
    >
      {children}
    </FlagsContext.Provider>
  );
};

export const useFlagsContext = (): FlagsContextT => {
  return useContext(FlagsContext)!;
};
