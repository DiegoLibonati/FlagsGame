import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { Loader } from "@src/components/Loader/Loader";
import { Flag as FlagComponent } from "@src/components/Flag/Flag";
import { FormGuessFlag } from "@src/components/Forms/FormGuessFlag/FormGuessFlag";

import { useCountdown } from "@src/hooks/useCountdown";
import { useFlagsContext } from "@src/context/FlagsContext/FlagsProvider";
import { useModeContext } from "@src/context/ModeContext/ModeProvider";
import { useGameContext } from "@src/context/GameContext/GameProvider";

import "@src/pages/GamePage/GamePage.css";

export const GamePage = (): JSX.Element => {
  const navigate = useNavigate();

  const { flags } = useFlagsContext()!;
  const { mode } = useModeContext();
  const { completeGuess, currentFlagToGuess, score } = useGameContext();

  const { timerText, secondsLeft, endTime, onCountdownReset } = useCountdown(
    mode.mode! && mode.mode?.timeleft
  );

  useEffect(() => {
    return () => {
      onCountdownReset();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (endTime || completeGuess)
      navigate(`/menu/${mode.mode?._id}/finishgame`);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [endTime, completeGuess]);

  if (flags.loading || !currentFlagToGuess) {
    return (
      <main className="game-main">
        <Loader></Loader>
      </main>
    );
  }

  return (
    <main className="game-main">
      <section className="game-page">
        <article className="game-page__header">
          <h1 className="game-page__title">GUESS THE FLAG</h1>
          <FlagComponent
            key={currentFlagToGuess!._id}
            image={currentFlagToGuess?.image!}
            name={currentFlagToGuess?.name!}
          ></FlagComponent>
        </article>

        <FormGuessFlag secondsLeft={secondsLeft}></FormGuessFlag>

        <article className="game-page__stats">
          <h3 className="game-page__score">Score: {score} PTS</h3>

          <h3 className="game-page__timeleft">Time left: {timerText}</h3>
        </article>
      </section>
    </main>
  );
};
