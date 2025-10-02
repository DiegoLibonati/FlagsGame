import { createContext } from "react";

import { AlertContext as AlertContextT } from "@src/entities/contexts";

export const AlertContext = createContext<AlertContextT | null>(null);
