import { createContext, useState } from "react";

import { Flag } from "@src/entities/app";
import { GameContext as GameContextT } from "@src/entities/contexts";
import { GameProviderProps } from "@src/entities/props";

export const GameContext = createContext<GameContextT | null>(null);

export const GameProvider = ({ children }: GameProviderProps) => {
  const [currentFlagToGuess, setCurrentFlagToGuess] = useState<Flag | null>(
    null
  );
  const [completeGuess, setCompleteGuess] = useState<boolean>(false);
  const [score, setScore] = useState<number>(0);

  const handleNextFlagToGuess = (flags: Flag[]) => {
    const indexOfFlag = flags?.indexOf(currentFlagToGuess!)!;
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

  const handleSetScore = (score: number) => {
    setScore(score);
  };

  return (
    <GameContext.Provider
      value={{
        currentFlagToGuess: currentFlagToGuess,
        completeGuess: completeGuess,
        score: score,
        handleNextFlagToGuess: handleNextFlagToGuess,
        handleSetScore: handleSetScore,
        handleSetFlagToGuess: handleSetFlagToGuess,
        handleClearCurrentFlagToGuess: handleClearCurrentFlagToGuess,
      }}
    >
      {children}
    </GameContext.Provider>
  );
};
