import { useEffect, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { addOrModifyUser } from "../../../api/addOrModifyUser";
import { useAlertContext } from "../../../context/AlertContext/AlertProvider";
import { useGameContext } from "../../../context/GameContext/GameProvider";
import { useForm } from "../../../hooks/useForm";

import "./FormUpdateUser.css";

export const FormUpdateUser = (): JSX.Element => {
  const redirectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const { mode } = useParams();
  const navigate = useNavigate();

  const { score } = useGameContext();
  const { alert, handleSetAlert } = useAlertContext();

  const { formState, onInputChange, onResetForm } = useForm<{
    username: string;
    password: string;
  }>({
    username: "",
    password: "",
  });

  const onSendRequest = async (
    e: React.FormEvent<HTMLFormElement>
  ): Promise<void> => {
    e.preventDefault();

    const body = {
      username: formState.username,
      password: formState.password,
      score: score,
      mode_name: mode!,
    };

    const result = await addOrModifyUser(body, "PUT");

    const messageBody = await result.json();

    const { message } = messageBody;

    if (!result.ok) {
      handleSetAlert({ type: "alert-auth-error", message: message });
      onResetForm();
      return;
    }

    handleSetAlert({ type: "alert-auth-success", message: message });
    onResetForm();

    redirectTimeoutRef.current = setTimeout(() => {
      navigate("/");
    }, 2000);
  };

  useEffect(() => {
    return () => {
      if (redirectTimeoutRef.current) clearTimeout(redirectTimeoutRef.current);
    };
  }, []);

  return (
    <form
      className="form__send__points form__update"
      onSubmit={(e) => onSendRequest(e)}
    >
      <h3>Your score was: {score} PTS</h3>
      <input
        type="text"
        placeholder="Your username goes here"
        value={formState.username}
        name="username"
        onChange={(e) => onInputChange(e)}
      ></input>
      <input
        type="password"
        placeholder="Your password goes here"
        value={formState.password}
        name="password"
        onChange={(e) => onInputChange(e)}
      ></input>
      <button
        type="submit"
        aria-label="send and replace"
        disabled={
          alert.type === "alert-auth-error" ||
          alert.type === "alert-auth-success"
        }
      >
        Send and replace
      </button>
    </form>
  );
};
