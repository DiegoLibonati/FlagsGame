import { createContext } from "react";

import { GameContext as GameContextT } from "../../entities/entities";

export const GameContext = createContext<GameContextT | null>(null);
