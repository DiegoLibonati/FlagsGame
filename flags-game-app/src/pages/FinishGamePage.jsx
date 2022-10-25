import React from "react";
import { useContext } from "react";
import "./FinishGamePage.css";
import { FlagsContext } from "../context/FlagsContext";
import { useParams } from "react-router-dom";
import { useForm } from "../hooks/useForm";
import { useRequest } from "../hooks/useRequest";

export const FinishGamePage = () => {
  const { score } = useContext(FlagsContext);
  const { mode } = useParams();
  const { formState, onInputChange, onResetForm } = useForm({
    username: "",
    password: "",
  });

  const { onSendRequest, alert } = useRequest(
    formState.username,
    formState.password,
    score,
    mode,
    "http://127.0.0.1:5000/users/addormodify",
    onResetForm
  );

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
