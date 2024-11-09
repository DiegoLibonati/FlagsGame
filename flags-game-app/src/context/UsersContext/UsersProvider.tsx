import { useCallback, useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  TopUsersState,
  UsersContext as UsersContextT,
  UserWithOutPassword,
} from "../../entities/entities";

import { UsersContext } from "./UsersContext";
import { getTopGeneral } from "../../api/getTopGeneral";
import { getTopMode } from "../../api/getTopMode";

interface UsersProviderProps {
  children: React.ReactNode;
}

export const UsersProvider = ({ children }: UsersProviderProps) => {
  // 3RD
  const { mode: modeName } = useParams();

  // Top
  const [topUsers, setTopUsers] = useState<TopUsersState>({
    users: [],
    error: null,
    loading: false,
  });

  const handleSetTopUsers = (users: UserWithOutPassword[]) => {
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

  // Función para obtener el top de usuarios
  const fetchGeneralTopUsers = useCallback(async () => {
    try {
      handleStartFetchUsers();
      const response = await getTopGeneral();
      const data = await response.json();
      handleSetTopUsers(data.data);
    } catch (error) {
      handleSetErrorUsers(String(error));
    } finally {
      handleEndFetchUsers();
    }
  }, []);

  const fetchModeTopUsers = useCallback(async () => {
    try {
      handleStartFetchUsers();
      const response = await getTopMode(modeName!);
      const data = await response.json();
      handleSetTopUsers(data.data);
    } catch (error) {
      handleSetErrorUsers(String(error));
    } finally {
      handleEndFetchUsers();
    }
  }, []);

  useEffect(() => {
    if (!topUsers.users.length && !modeName) fetchGeneralTopUsers();
    if (!topUsers.users.length && modeName) fetchModeTopUsers();

    return () => {
      handleClearTopUsers();
    };
  }, []);

  return (
    <UsersContext.Provider
      value={{
        topUsers: topUsers!,
        handleSetTopUsers: handleSetTopUsers,
        handleClearTopUsers: handleClearTopUsers,
        refreshGeneralTopUsers: fetchGeneralTopUsers,
        refreshModeTopUsers: fetchModeTopUsers,
      }}
    >
      {children}
    </UsersContext.Provider>
  );
};

export const useUsersContext = (): UsersContextT => {
  return useContext(UsersContext)!;
};
