import { createContext } from "react";

import { ModeContext as ModeContextT } from "../../entities/entities";

export const ModeContext = createContext<ModeContextT | null>(null);
