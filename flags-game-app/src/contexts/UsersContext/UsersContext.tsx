import { createContext, useState } from "react";

import { TopUsersState } from "@src/entities/states";
import { UsersContext as UsersContextT } from "@src/entities/contexts";
import { UserTop } from "@src/entities/app";
import { UsersProviderProps } from "@src/entities/props";

export const UsersContext = createContext<UsersContextT | null>(null);

export const UsersProvider = ({ children }: UsersProviderProps) => {
  // Top
  const [topUsers, setTopUsers] = useState<TopUsersState>({
    users: [],
    error: null,
    loading: false,
  });

  const handleSetTopUsers = (users: UserTop[]) => {
    setTopUsers((state) => ({
      ...state,
      users: users,
    }));
  };

  const handleClearTopUsers = () => {
    setTopUsers({ users: [], error: null, loading: false });
  };

  const handleStartFetchUsers = () => {
    setTopUsers((state) => ({
      ...state,
      loading: true,
      error: null,
    }));
  };

  const handleEndFetchUsers = () => {
    setTopUsers((state) => ({
      ...state,
      loading: false,
    }));
  };

  const handleSetErrorUsers = (error: string) => {
    setTopUsers((state) => ({
      ...state,
      error: error,
    }));
  };

  return (
    <UsersContext.Provider
      value={{
        topUsers: topUsers!,
        handleSetTopUsers: handleSetTopUsers,
        handleClearTopUsers: handleClearTopUsers,
        handleStartFetchUsers: handleStartFetchUsers,
        handleEndFetchUsers: handleEndFetchUsers,
        handleSetErrorUsers: handleSetErrorUsers,
      }}
    >
      {children}
    </UsersContext.Provider>
  );
};
