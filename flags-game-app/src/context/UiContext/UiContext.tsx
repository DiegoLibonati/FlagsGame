import { createContext } from "react";

import { UiContext as UiContextT } from "../../entities/entities";

export const UiContext = createContext<UiContextT | null>(null);
