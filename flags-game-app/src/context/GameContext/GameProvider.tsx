import { useContext, useEffect, useState } from "react";

import { Flag, GameContext as GameContextT } from "../../entities/entities";

import { GameContext } from "./GameContext";
import { useFlagsContext } from "../FlagsContext/FlagsProvider";

interface GameProviderProps {
  children: React.ReactNode;
}

export const GameProvider = ({ children }: GameProviderProps) => {
  // 3RD
  const { flags } = useFlagsContext();

  // Current Flag To Guess
  const [currentFlagToGuess, setCurrentFlagToGuess] = useState<Flag | null>(
    null
  );
  const [completeGuess, setCompleteGuess] = useState<boolean>(false);

  const handleNextFlagToGuess = () => {
    const arrFlags = flags.flags;

    const indexOfFlag = arrFlags?.indexOf(currentFlagToGuess!)!;
    const newIndexFlag = indexOfFlag + 1;

    if (newIndexFlag === arrFlags!.length) return setCompleteGuess(true);

    setCurrentFlagToGuess(arrFlags![newIndexFlag]);
  };

  const handleSetFlagToGuess = (flag: Flag) => {
    setCurrentFlagToGuess(flag);
  };

  const handleClearCurrentFlagToGuess = () => {
    setCurrentFlagToGuess(null);
    setCompleteGuess(false);
  };

  useEffect(() => {
    const arrFlags = flags.flags;

    if (!arrFlags.length || currentFlagToGuess) return;

    handleSetFlagToGuess(arrFlags[0]);
  }, [flags.flags.length]);

  // Score
  const [score, setScore] = useState<number>(0);

  const handleSetScore = (score: number) => {
    setScore(score);
  };

  useEffect(() => {
    return () => {
      handleClearCurrentFlagToGuess();
    };
  }, []);

  return (
    <GameContext.Provider
      value={{
        currentFlagToGuess: currentFlagToGuess,
        completeGuess: completeGuess,
        score: score,
        handleNextFlagToGuess: handleNextFlagToGuess,
        handleSetScore: handleSetScore,
      }}
    >
      {children}
    </GameContext.Provider>
  );
};

export const useGameContext = (): GameContextT => {
  return useContext(GameContext)!;
};
