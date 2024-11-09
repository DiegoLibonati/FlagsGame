import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { Loader } from "../../components/Loader/Loader";
import { Flag as FlagComponent } from "../../components/Flag/Flag";
import { FormGuessFlag } from "../../components/Forms/FormGuessFlag/FormGuessFlag";

import { useCountdown } from "../../hooks/useCountdown";
import { useFlagsContext } from "../../context/FlagsContext/FlagsProvider";
import { useModeContext } from "../../context/ModeContext/ModeProvider";
import { useGameContext } from "../../context/GameContext/GameProvider";

import "./GamePage.css";

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
      navigate(`/menu/${mode.mode?.name}/finishgame`);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [endTime, completeGuess]);

  if (flags.loading || !currentFlagToGuess) {
    return (
      <main>
        <Loader></Loader>
      </main>
    );
  }

  return (
    <main>
      <section className="guess_container">
        <article className="guess_container_header">
          <h1>GUESS THE FLAG</h1>
          <FlagComponent
            key={currentFlagToGuess!._id}
            image={currentFlagToGuess?.image!}
            name={currentFlagToGuess?.name!}
          ></FlagComponent>
        </article>

        <FormGuessFlag secondsLeft={secondsLeft}></FormGuessFlag>

        <article className="guess_container_score">
          <h3>Score: {score} PTS</h3>

          <h3>Time left: {timerText}</h3>
        </article>
      </section>
    </main>
  );
};
