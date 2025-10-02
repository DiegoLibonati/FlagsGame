import { useEffect, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { patchUser } from "@src/api/patchUser";
import { useAlertContext } from "@src/context/AlertContext/AlertProvider";
import { useGameContext } from "@src/context/GameContext/GameProvider";
import { useForm } from "@src/hooks/useForm";

import "@src/components/Forms/FormUpdateUser/FormUpdateUser.css";

export const FormUpdateUser = (): JSX.Element => {
  const redirectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const { idMode } = useParams();
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
      mode_id: idMode!,
    };

    const result = await patchUser(body);

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
    <form className="form-update-user" onSubmit={(e) => onSendRequest(e)}>
      <h3 className="form-update-user__score">Your score was: {score} PTS</h3>
      <input
        type="text"
        placeholder="Your username goes here"
        value={formState.username}
        name="username"
        className="form-update-user__input"
        onChange={(e) => onInputChange(e)}
      ></input>
      <input
        type="password"
        placeholder="Your password goes here"
        value={formState.password}
        name="password"
        className="form-update-user__input"
        onChange={(e) => onInputChange(e)}
      ></input>
      <button
        type="submit"
        aria-label="send and replace"
        className="form-update-user__submit"
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
