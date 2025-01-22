import { useEffect, useRef } from "react";

import { useForm } from "../../../hooks/useForm";
import { useModeContext } from "../../../context/ModeContext/ModeProvider";
import { useGameContext } from "../../../context/GameContext/GameProvider";
import { rootCss } from "../../../constants/configCss";

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
      inputElement.style.borderColor = rootCss.colors.green;
      onResetForm();
      handleSetScore(score + secondsLeft * mode.mode?.multiplier!);
      handleNextFlagToGuess();
      return;
    }

    inputElement.style.borderColor = rootCss.colors.red;
    onResetForm();
  };

  useEffect(() => {
    const inputElement = inputRef.current!;

    if (!inputElement) return;

    const timeout = setTimeout(() => {
      inputRef.current!.style.borderColor = rootCss.colors.white;
    }, 500);

    return () => {
      clearTimeout(timeout);
    };
  }, [inputRef.current?.style?.borderColor]);

  return (
    <form className="form-guess-flag" onSubmit={(e) => onSubmit(e)}>
      <input
        ref={inputRef}
        type="text"
        value={formState.name}
        placeholder="Enter a Country Name..."
        onChange={(e) => onInputChange(e)}
        className="form-guess-flag__name"
        name="name"
      ></input>
      <button
        type="submit"
        aria-label="submit guess"
        className="form-guess-flag__submit"
      >
        SUBMIT
      </button>
    </form>
  );
};
