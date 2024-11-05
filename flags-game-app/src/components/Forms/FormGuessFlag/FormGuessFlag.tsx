import { useRef } from "react";

import { useForm } from "../../../hooks/useForm";
import { useFlagsContext } from "../../../context/FlagsContext/FlagsProvider";
import { useModesContext } from "../../../context/ModesContext/ModesProvider";

import "./FormGuessFlag.css";

interface FormGuessFlagProps {
  secondsLeft: number;
}

export const FormGuessFlag = ({
  secondsLeft,
}: FormGuessFlagProps): JSX.Element => {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const { currentFlagToGuess, score, handleSetScore, handleNextFlagToGuess } =
    useFlagsContext();
  const { actualMode } = useModesContext();

  const { formState, onInputChange, onResetForm } = useForm<{ name: string }>({
    name: "",
  });

  const onSubmit: React.FormEventHandler<HTMLFormElement> = (e) => {
    e.preventDefault();

    const currentFlagName = currentFlagToGuess!.name.toLowerCase();
    const inputElement = inputRef.current!;
    const inputValue = formState.name.toLowerCase();

    if (currentFlagName === inputValue) {
      inputElement.style.borderColor = "white";
      onResetForm();
      handleSetScore(score + secondsLeft * actualMode.multiplier);
      handleNextFlagToGuess();
      return;
    }

    inputElement.style.borderColor = "red";
    onResetForm();
  };

  return (
    <form className="guess_container_form" onSubmit={(e) => onSubmit(e)}>
      <input
        ref={inputRef}
        type="text"
        value={formState.name}
        onChange={(e) => onInputChange(e)}
        name="name"
      ></input>
      <button>SUBMIT</button>
    </form>
  );
};
