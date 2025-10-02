import { useCallback, useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { TopUsersState } from "@src/entities/states";
import { UsersContext as UsersContextT } from "@src/entities/contexts";
import { UserTop } from "@src/entities/entities";
import { UsersProviderProps } from "@src/entities/props";

import { UsersContext } from "@src/context/UsersContext/UsersContext";
import { getTopGeneral } from "@src/api/getTopGeneral";
import { getTopMode } from "@src/api/getTopMode";

export const UsersProvider = ({ children }: UsersProviderProps) => {
  // 3RD
  const { idMode } = useParams();

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
      const response = await getTopMode(idMode!);
      const data = await response.json();
      handleSetTopUsers(data.data);
    } catch (error) {
      handleSetErrorUsers(String(error));
    } finally {
      handleEndFetchUsers();
    }
  }, []);

  useEffect(() => {
    if (!topUsers.users.length && !idMode) fetchGeneralTopUsers();
    if (!topUsers.users.length && idMode) fetchModeTopUsers();

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
