import { createContext } from "react";

import { ModesContext as ModesContextT } from "../../entities/entities";

export const ModesContext = createContext<ModesContextT | null>(null);
