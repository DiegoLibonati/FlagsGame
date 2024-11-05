import { useContext, useState } from "react";

import {
  UsersContext as UsersContextT,
  UsersProviderProps,
  User,
} from "../../entities/entities";

import { UsersContext } from "./UsersContext";

export const UsersProvider = ({ children }: UsersProviderProps) => {
  // Top
  const [topUsers, setTopUsers] = useState<User[] | null>(null);

  const handleSetTopUsers = (users: User[]) => {
    setTopUsers(users);
  };

  const handleClearTopUsers = () => {
    setTopUsers(null);
  };

  return (
    <UsersContext.Provider
      value={{
        topUsers: topUsers!,
        handleSetTopUsers: handleSetTopUsers,
        handleClearTopUsers: handleClearTopUsers,
      }}
    >
      {children}
    </UsersContext.Provider>
  );
};

export const useUsersContext = (): UsersContextT => {
  return useContext(UsersContext)!;
};
