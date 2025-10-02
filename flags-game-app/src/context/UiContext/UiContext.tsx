import { createContext } from "react";

import { UiContext as UiContextT } from "@src/entities/contexts";

export const UiContext = createContext<UiContextT | null>(null);
