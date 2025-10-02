import { createContext } from "react";

import { UsersContext as UsersContextT } from "@src/entities/contexts";

export const UsersContext = createContext<UsersContextT | null>(null);
