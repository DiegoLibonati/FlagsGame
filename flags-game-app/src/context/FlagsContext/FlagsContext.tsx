import { createContext } from "react";

import { FlagsContext as FlagsContextT } from "@src/entities/contexts";

export const FlagsContext = createContext<FlagsContextT | null>(null);
