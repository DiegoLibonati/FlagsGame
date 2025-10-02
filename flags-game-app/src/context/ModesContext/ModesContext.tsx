import { createContext } from "react";

import { ModesContext as ModesContextT } from "@src/entities/contexts";

export const ModesContext = createContext<ModesContextT | null>(null);
