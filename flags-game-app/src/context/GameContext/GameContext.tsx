import { createContext } from "react";

import { GameContext as GameContextT } from "@src/entities/contexts";

export const GameContext = createContext<GameContextT | null>(null);
