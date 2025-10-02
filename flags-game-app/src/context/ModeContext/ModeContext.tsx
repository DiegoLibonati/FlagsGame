import { createContext } from "react";

import { ModeContext as ModeContextT } from "@src/entities/contexts";

export const ModeContext = createContext<ModeContextT | null>(null);
