import { useContext, useState, useEffect } from "react";
import { FlagsContext } from "../context/FlagsContext";
import { useNavigate, useParams } from "react-router-dom";
import { useForm } from "../hooks/useForm";
import { addOrModifyUser } from "../api/addOrModifyUser";
import "./FinishGamePage.css";

export const FinishGamePage = (): JSX.Element => {
  const [alert, setAlert] = useState<{ type: string; message: string }>({
    type: "",
    message: "",
  });

  const { mode } = useParams();
  const { score } = useContext(FlagsContext)!;
  const { formState, onInputChange, onResetForm } = useForm<{
    username: string;
    password: string;
  }>({
    username: "",
    password: "",
  });
  const navigate = useNavigate();

  const onSendRequest = async (
    e: React.FormEvent<HTMLFormElement>,
    method: string
  ): Promise<void> => {
    e.preventDefault();

    const body = {
      username: formState.username,
      password: formState.password,
      score: score,
      mode_name: mode!,
    };

    const result = await addOrModifyUser(body, method);

    const messageBody = await result.json();

    const { message } = messageBody;

    if (result.status === 200) {
      setAlert({ ...alert, type: "success", message: message });
      navigate("/");
    } else {
      setAlert({ ...alert, type: "error", message: message });
    }

    onResetForm();
  };

  useEffect(() => {
    const timeout = setTimeout(() => {
      setAlert({ ...alert, type: "", message: "" });
    }, 2000);

    return () => {
      clearTimeout(timeout);
    };
  }, [alert, navigate]);

  return (
    <main>
      <section className="send_points_container">
        <h4 className={`alert ${alert.type}`}>{alert.message}</h4>
        <article className="send_points_container_mini">
          <h2>If you DONT have a user register</h2>

          <form
            className="send_points_container_mini_form"
            onSubmit={(e) => onSendRequest(e, "POST")}
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
              type="text"
              placeholder="Your password goes here"
              value={formState.password}
              name="password"
              onChange={(e) => onInputChange(e)}
            ></input>
            <button type="submit">Send and register</button>
          </form>
        </article>

        <article className="send_points_container_mini">
          <h2>If you HAVE a user register</h2>

          <form
            className="send_points_container_mini_form"
            onSubmit={(e) => onSendRequest(e, "PUT")}
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
              type="text"
              placeholder="Your password goes here"
              value={formState.password}
              name="password"
              onChange={(e) => onInputChange(e)}
            ></input>
            <button type="submit">Send and replace</button>
          </form>
        </article>
      </section>
    </main>
  );
};
