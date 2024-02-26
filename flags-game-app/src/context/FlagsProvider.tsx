import { useState } from "react";
import { FlagsContext } from "./FlagsContext";
import { Flag, FlagsProviderProps, Mode, User } from "../entities/entities";

export const FlagsProvider = ({ children }: FlagsProviderProps) => {
  const [navbar, setNavbar] = useState<boolean>(false);
  const [btnStart, setBtnStart] = useState<boolean>(false);
  const [score, setScore] = useState<number>(0);

  const [flagsArr, setFlagsArr] = useState<Flag[]>([]);
  const [flagsLoading, setFlagsLoading] = useState<boolean>(false);

  const [actualMode, setActualMode] = useState<Mode | null>(null);
  const [modeLoading, setModeLoading] = useState<boolean>(false);

  const [topArr, setTopArr] = useState<User[]>([]);
  const [topLoading, setTopLoading] = useState<boolean>(false);

  const manageNavbar = (): void => {
    setNavbar(!navbar);
  };

  return (
    <FlagsContext.Provider
      value={{
        navbar,
        btnStart,
        score,
        flagsArr,
        topArr,
        actualMode,
        flagsLoading,
        modeLoading,
        topLoading,
        setBtnStart,
        setScore,
        manageNavbar,
        setFlagsArr,
        setFlagsLoading,
        setActualMode,
        setModeLoading,
        setTopArr,
        setTopLoading,
      }}
    >
      {children}
    </FlagsContext.Provider>
  );
};
