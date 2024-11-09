import { useEffect, useRef } from "react";

import { useForm } from "../../../hooks/useForm";
import { useModeContext } from "../../../context/ModeContext/ModeProvider";
import { useGameContext } from "../../../context/GameContext/GameProvider";

import "./FormGuessFlag.css";

interface FormGuessFlagProps {
  secondsLeft: number;
}

export const FormGuessFlag = ({
  secondsLeft,
}: FormGuessFlagProps): JSX.Element => {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const { currentFlagToGuess, score, handleSetScore, handleNextFlagToGuess } =
    useGameContext();
  const { mode } = useModeContext();

  const { formState, onInputChange, onResetForm } = useForm<{ name: string }>({
    name: "",
  });

  const onSubmit: React.FormEventHandler<HTMLFormElement> = (e) => {
    e.preventDefault();

    const currentFlagName = currentFlagToGuess!.name.toLowerCase();
    const inputElement = inputRef.current!;
    const inputValue = formState.name.toLowerCase();

    if (currentFlagName === inputValue) {
      inputElement.style.borderColor = "green";
      onResetForm();
      handleSetScore(score + secondsLeft * mode.mode?.multiplier!);
      handleNextFlagToGuess();
      return;
    }

    inputElement.style.borderColor = "red";
    onResetForm();
  };

  useEffect(() => {
    const inputElement = inputRef.current!;

    if (!inputElement) return;

    const timeout = setTimeout(() => {
      inputRef.current!.style.borderColor = "white";
    }, 500);

    return () => {
      clearTimeout(timeout);
    };
  }, [inputRef.current?.style?.borderColor]);

  return (
    <form className="guess_container_form" onSubmit={(e) => onSubmit(e)}>
      <input
        ref={inputRef}
        type="text"
        value={formState.name}
        placeholder="Enter a Country Name..."
        onChange={(e) => onInputChange(e)}
        name="name"
      ></input>
      <button type="submit">SUBMIT</button>
    </form>
  );
};
