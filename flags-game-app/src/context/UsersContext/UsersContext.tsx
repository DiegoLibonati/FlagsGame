import { createContext } from "react";

import { UsersContext as UsersContextT } from "../../entities/entities";

export const UsersContext = createContext<UsersContextT | null>(null);
