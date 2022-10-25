import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getFinishGame } from "../helpers/getFinishGame";

export const useLogic = (
  arr,
  input,
  onResetForm,
  timer,
  setScore,
  actualScore,
  actualMode,
  refElement
) => {
  const [index, setIndex] = useState(0);
  const [currentItem, setCurrentItem] = useState("");
  const [finishGame, setFinishGame] = useState(false);
  const [guess, setGuess] = useState(false);
  const navigate = useNavigate();

  useMemo(() => {
    getFinishGame(timer, index, arr, setFinishGame);
  }, [timer, index, arr]);

  useEffect(() => {
    if (finishGame) {
      navigate(`/menu/${actualMode}/finishgame`);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [finishGame]);

  useEffect(() => {
    try {
      setCurrentItem(arr[index]);
    } catch (e) {}
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [index, arr]);

  useEffect(() => {
    const timeout = setTimeout(() => {
      try {
        refElement.current.style.borderColor = "white";
        setGuess(false);
      } catch (e) {}
    }, 1000);

    return () => clearTimeout(timeout);
  }, [guess, refElement]);

  const onSubmit = (e) => {
    e.preventDefault();

    const currentItemLower = currentItem.name.toLowerCase();
    const inputLower = input.toLowerCase();

    if (currentItemLower === inputLower) {
      setIndex(index + 1);

      const timerArray = timer.split(":");

      const secondsMultiply = timerArray[1] + timerArray[2];

      if (secondsMultiply[0] === "0") {
        const secondsMultiplyFinal = secondsMultiply.slice(1, 4);

        if (actualMode === "normal") {
          const score = 10 * parseInt(secondsMultiplyFinal);

          setScore(actualScore + score);
        } else if (actualMode === "hard") {
          const score = 100 * parseInt(secondsMultiplyFinal);

          setScore(actualScore + score);
        } else if (actualMode === "hardcore") {
          const score = 1000 * parseInt(secondsMultiplyFinal);

          setScore(actualScore + score);
        }

        setGuess(true);
        refElement.current.style.borderColor = "green";

        onResetForm();
      } else {
        const secondsMultiplyFinal = secondsMultiply.slice(1, 4);

        if (actualMode === "normal") {
          const score = 10 * parseInt(secondsMultiplyFinal);

          setScore(actualScore + score);
        } else if (actualMode === "hard") {
          const score = 100 * parseInt(secondsMultiplyFinal);

          setScore(actualScore + score);
        } else if (actualMode === "hardcore") {
          const score = 1000 * parseInt(secondsMultiplyFinal);

          setScore(actualScore + score);
        }
        setGuess(true);
        refElement.current.style.borderColor = "green";
        onResetForm();
      }
    } else {
      setGuess(true);
      refElement.current.style.borderColor = "red";
      onResetForm();
    }
  };

  return {
    currentItem,
    onSubmit,
    setFinishGame,
  };
};
