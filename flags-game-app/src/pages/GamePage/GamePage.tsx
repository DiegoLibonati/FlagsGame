import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { Loader } from "@src/components/Loader/Loader";
import { Flag as FlagComponent } from "@src/components/Flag/Flag";
import { FormGuessFlag } from "@src/components/Forms/FormGuessFlag/FormGuessFlag";

import { useCountdown } from "@src/hooks/useCountdown";
import { useFlagsContext } from "@src/hooks/useFlagsContext";
import { useModeContext } from "@src/hooks/useModeContext";
import { useGameContext } from "@src/hooks/useGameContext";

import { getRandomFlags } from "@src/api/get/getRandomFlags";
import { getMode } from "@src/api/get/getMode";

import "@src/pages/GamePage/GamePage.css";

export const GamePage = (): JSX.Element => {
  const { idMode } = useParams();
  const navigate = useNavigate();

  const {
    flags,
    handleClearFlags,
    handleEndFetchFlags,
    handleSetErrorFlags,
    handleSetFlags,
    handleStartFetchFlags,
  } = useFlagsContext();
  const {
    mode,
    handleClearMode,
    handleEndFetchMode,
    handleSetErrorMode,
    handleSetMode,
    handleStartFetchMode,
  } = useModeContext();
  const { completeGuess, currentFlagToGuess, score, handleSetFlagToGuess } =
    useGameContext();

  const { timerText, secondsLeft, endTime, onCountdownReset } = useCountdown(
    mode.mode! && mode.mode?.timeleft
  );

  const handleGetRandomFlags = async () => {
    try {
      handleStartFetchFlags();
      const response = await getRandomFlags(5);
      handleSetFlags(response.data);
    } catch (error) {
      handleSetErrorFlags(String(error));
    } finally {
      handleEndFetchFlags();
    }
  };

  const handleGetMode = async () => {
    try {
      handleStartFetchMode();
      const response = await getMode(idMode!);
      handleSetMode(response.data);
    } catch (error) {
      handleSetErrorMode(String(error));
    } finally {
      handleEndFetchMode();
    }
  };

  useEffect(() => {
    handleGetRandomFlags();
    handleGetMode();

    return () => {
      onCountdownReset();
      handleClearFlags();
      handleClearMode();
    };
  }, []);

  useEffect(() => {
    if (endTime || completeGuess)
      navigate(`/menu/${mode.mode?._id}/finishgame`);
  }, [endTime, completeGuess]);

  useEffect(() => {
    if (!flags.flags || flags.flags.length === 0 || currentFlagToGuess) return;

    handleSetFlagToGuess(flags.flags[0]);
  }, [flags.flags]);

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
