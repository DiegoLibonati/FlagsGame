import { useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { addUser } from "@src/api/addUser";
import { useForm } from "@src/hooks/useForm";
import { useGameContext } from "@src/context/GameContext/GameProvider";
import { useAlertContext } from "@src/context/AlertContext/AlertProvider";

import "@src/components/Forms/FormRegisterUser/FormRegisterUser.css";

export const FormRegisterUser = (): JSX.Element => {
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

    const result = await addUser(body);

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

  return (
    <form className="form-register-user" onSubmit={(e) => onSendRequest(e)}>
      <h3 className="form-register-user__score">Your score was: {score} PTS</h3>
      <input
        type="text"
        placeholder="Your username goes here"
        value={formState.username}
        className="form-register-user__input"
        name="username"
        onChange={(e) => onInputChange(e)}
      ></input>
      <input
        type="password"
        placeholder="Your password goes here"
        value={formState.password}
        className="form-register-user__input"
        name="password"
        onChange={(e) => onInputChange(e)}
      ></input>
      <button
        type="submit"
        aria-label="send and register"
        className="form-register-user__submit"
        disabled={
          alert.type === "alert-auth-error" ||
          alert.type === "alert-auth-success"
        }
      >
        Send and register
      </button>
    </form>
  );
};
