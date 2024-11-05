import { useNavigate, useParams } from "react-router-dom";

import { addOrModifyUser } from "../../../api/addOrModifyUser";
import { useForm } from "../../../hooks/useForm";
import { useFlagsContext } from "../../../context/FlagsContext/FlagsProvider";
import { useAlertContext } from "../../../context/AlertContext/AlertProvider";

import "./FormRegisterUser.css";

export const FormRegisterUser = (): JSX.Element => {
  const { mode } = useParams();
  const navigate = useNavigate();

  const { score } = useFlagsContext();
  const { handleSetAlert } = useAlertContext();

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
    try {
      e.preventDefault();

      const body = {
        username: formState.username,
        password: formState.password,
        score: score,
        mode_name: mode!,
      };
  
      const result = await addOrModifyUser(body, "POST");
  
      const messageBody = await result.json();
  
      const { message } = messageBody;
  
      handleSetAlert({ type: "success", message: message });
      onResetForm();
      navigate("/");
    } catch(e){
      handleSetAlert({ type: "error", message: String(e) });
    }
  };

  return (
    <form
      className="send_points_container_mini_form"
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
      <button type="submit">Send and register</button>
    </form>
  );
};
