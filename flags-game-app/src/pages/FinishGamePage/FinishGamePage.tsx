import { useCallback, useEffect } from "react";

import { FormRegisterUser } from "../../components/Forms/FormRegisterUser/FormRegisterUser";
import { FormUpdateUser } from "../../components/Forms/FormUpdateUser/FormUpdateUser";

import { useAlertContext } from "../../context/AlertContext/AlertProvider";
import { useGameContext } from "../../context/GameContext/GameProvider";

import "./FinishGamePage.css";
import { parseAlertType } from "../../helpers/parseAlertType";

// TODO: Separar estilos de alert // Componente Alert

export const FinishGamePage = (): JSX.Element => {
  const { alert } = useAlertContext();
  const { handleSetScore } = useGameContext()!;

  const parseAlertTypeFn = useCallback(
    () => parseAlertType(alert.type),
    [alert.type]
  );

  useEffect(() => {
    return () => {
      handleSetScore(0);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main>
      <section className="send__points">
        <h4 className={`alert ${parseAlertTypeFn()}`}>{alert.message}</h4>
        <article className="send__points__mini register__article">
          <h2>If you DONT have a user register</h2>

          <FormRegisterUser></FormRegisterUser>
        </article>

        <article className="send__points__mini update__article">
          <h2>If you HAVE a user register</h2>

          <FormUpdateUser></FormUpdateUser>
        </article>
      </section>
    </main>
  );
};
