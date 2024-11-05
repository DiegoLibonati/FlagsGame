import { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { Loader } from "../../components/Loader/Loader";
import { Flag as FlagComponent } from "../../components/Flag/Flag";
import { FormGuessFlag } from "../../components/Forms/FormGuessFlag/FormGuessFlag";

import { getRandomFlags } from "../../api/getRandomFlags";
import { findMode } from "../../api/findMode";
import { useCountdown } from "../../hooks/useCountdown";
import { useFlagsContext } from "../../context/FlagsContext/FlagsProvider";
import { useModesContext } from "../../context/ModesContext/ModesProvider";

import "./GamePage.css";

export const GamePage = (): JSX.Element => {
  const { mode } = useParams();
  const navigate = useNavigate();

  const {
    flags,
    score,
    completeGuess,
    currentFlagToGuess,
    handleSetFlags,
    handleClearFlags,
    handleClearCurrentFlagToGuess,
    handleSetFlagToGuess,
  } = useFlagsContext()!;
  const { actualMode, handleSetActualMode, handleClearActualMode } =
    useModesContext();

  const { timerText, secondsLeft, endTime, onCountdownReset } = useCountdown(
    actualMode && actualMode?.timeleft
  );

  const handleMode = async (): Promise<void> => {
    const request = await findMode(mode!);

    const data = await request.json();

    handleSetActualMode(data.data);
  };

  const handleFlags = async (): Promise<void> => {
    const request = await getRandomFlags(mode!);

    const data = await request.json();

    handleSetFlags(data.data);
    handleSetFlagToGuess(data.data[0]);
  };

  useEffect(() => {
    handleFlags();
    handleMode();

    return () => {
      onCountdownReset();
      handleClearFlags();
      handleClearCurrentFlagToGuess();
      handleClearActualMode();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (endTime || completeGuess)
      navigate(`/menu/${actualMode.name}/finishgame`);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [endTime, completeGuess]);

  if (!flags) {
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
