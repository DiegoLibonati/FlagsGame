import { createContext } from "react";
import { FlagsContextT } from "../entities/entities";

export const FlagsContext = createContext<FlagsContextT | null>(null);
