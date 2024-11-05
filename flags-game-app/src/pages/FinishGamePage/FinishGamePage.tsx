import { useEffect } from "react";

import { FormRegisterUser } from "../../components/Forms/FormRegisterUser/FormRegisterUser";
import { FormUpdateUser } from "../../components/Forms/FormUpdateUser/FormUpdateUser";

import { useFlagsContext } from "../../context/FlagsContext/FlagsProvider";
import { useAlertContext } from "../../context/AlertContext/AlertProvider";

import "./FinishGamePage.css";

export const FinishGamePage = (): JSX.Element => {
  const { alert } = useAlertContext();
  const { handleSetScore } = useFlagsContext()!;

  useEffect(() => {
    return () => {
      handleSetScore(0);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main>
      <section className="send_points_container">
        <h4 className={`alert ${alert.type}`}>{alert.message}</h4>
        <article className="send_points_container_mini">
          <h2>If you DONT have a user register</h2>

          <FormRegisterUser></FormRegisterUser>
        </article>

        <article className="send_points_container_mini">
          <h2>If you HAVE a user register</h2>

          <FormUpdateUser></FormUpdateUser>
        </article>
      </section>
    </main>
  );
};
