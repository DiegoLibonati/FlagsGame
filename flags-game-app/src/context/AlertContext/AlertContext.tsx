import { createContext } from "react";

import { AlertContext as AlertContextT } from "../../entities/entities";

export const AlertContext = createContext<AlertContextT | null>(null);
