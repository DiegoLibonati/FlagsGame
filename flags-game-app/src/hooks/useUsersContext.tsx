import { useContext } from "react";

import { UseUsersContext } from "@src/entities/hooks";

import { UsersContext } from "@src/contexts/UsersContext/UsersContext";

export const useUsersContext = (): UseUsersContext => {
  const context = useContext(UsersContext);
  if (!context)
    throw new Error("useUsersContext must be used within UsersProvider");
  return context;
};
