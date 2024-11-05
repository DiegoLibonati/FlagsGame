import { createContext } from "react";

import { FlagsContext as FlagsContextT } from "../../entities/entities";

export const FlagsContext = createContext<FlagsContextT | null>(null);
