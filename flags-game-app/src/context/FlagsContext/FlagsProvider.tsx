import { useContext, useState } from "react";

import {
  Flag,
  FlagsContext as FlagsContextT,
  FlagsProviderProps,
} from "../../entities/entities";

import { FlagsContext } from "./FlagsContext";

export const FlagsProvider = ({ children }: FlagsProviderProps) => {
  // Flags
  const [flags, setFlags] = useState<Flag[] | null>(null);

  const handleSetFlags = (flags: Flag[]) => {
    setFlags(flags);
  };

  const handleClearFlags = () => {
    setFlags(null);
  };

  // Current Flag To Guess
  const [currentFlagToGuess, setCurrentFlagToGuess] = useState<Flag | null>(
    null
  );
  const [completeGuess, setCompleteGuess] = useState<boolean>(false);

  const handleNextFlagToGuess = () => {
    if (!currentFlagToGuess) return setCurrentFlagToGuess(flags![0]);

    const indexOfFlag = flags?.indexOf(currentFlagToGuess)!;
    const newIndexFlag = indexOfFlag + 1;

    if (newIndexFlag === flags!.length) return setCompleteGuess(true);

    setCurrentFlagToGuess(flags![newIndexFlag]);
  };

  const handleSetFlagToGuess = (flag: Flag) => {
    setCurrentFlagToGuess(flag);
  };

  const handleClearCurrentFlagToGuess = () => {
    setCurrentFlagToGuess(null);
    setCompleteGuess(false);
  };

  // Score
  const [score, setScore] = useState<number>(0);

  const handleSetScore = (score: number) => {
    setScore(score);
  };

  return (
    <FlagsContext.Provider
      value={{
        flags: flags!,
        score: score,
        currentFlagToGuess: currentFlagToGuess!,
        completeGuess: completeGuess,
        handleSetFlags: handleSetFlags,
        handleSetScore: handleSetScore,
        handleClearFlags: handleClearFlags,
        handleNextFlagToGuess: handleNextFlagToGuess,
        handleClearCurrentFlagToGuess: handleClearCurrentFlagToGuess,
        handleSetFlagToGuess: handleSetFlagToGuess,
      }}
    >
      {children}
    </FlagsContext.Provider>
  );
};

export const useFlagsContext = (): FlagsContextT => {
  return useContext(FlagsContext)!;
};
