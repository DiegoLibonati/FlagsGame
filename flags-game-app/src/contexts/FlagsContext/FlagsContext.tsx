import { createContext, useState } from "react";

import { Flag } from "@src/entities/app";
import { FlagsContext as FlagsContextT } from "@src/entities/contexts";
import { FlagsState } from "@src/entities/states";
import { FlagsProviderProps } from "@src/entities/props";

export const FlagsContext = createContext<FlagsContextT | null>(null);

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

  return (
    <FlagsContext.Provider
      value={{
        flags: flags!,
        handleSetFlags: handleSetFlags,
        handleClearFlags: handleClearFlags,
        handleStartFetchFlags: handleStartFetchFlags,
        handleEndFetchFlags: handleEndFetchFlags,
        handleSetErrorFlags: handleSetErrorFlags,
      }}
    >
      {children}
    </FlagsContext.Provider>
  );
};
