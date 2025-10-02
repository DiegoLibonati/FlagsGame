import { useCallback, useEffect } from "react";

import { FormRegisterUser } from "@src/components/Forms/FormRegisterUser/FormRegisterUser";
import { FormUpdateUser } from "@src/components/Forms/FormUpdateUser/FormUpdateUser";

import { useAlertContext } from "@src/context/AlertContext/AlertProvider";
import { useGameContext } from "@src/context/GameContext/GameProvider";
import { parseAlertType } from "@src/helpers/parseAlertType";

import "@src/pages/FinishGamePage/FinishGamePage.css";

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
    <main className="finish-game-main">
      <section className="finish-game-page">
        <h4 className={`alert ${parseAlertTypeFn()}`}>{alert.message}</h4>
        <article className="finish-game-page__wrapper-form finish-game-page__wrapper-register">
          <h2 className="finish-game-page__form-title">
            If you DONT have a user register
          </h2>

          <FormRegisterUser></FormRegisterUser>
        </article>

        <article className="finish-game-page__wrapper-form finish-game-page__wrapper-update">
          <h2 className="finish-game-page__form-title">
            If you HAVE a user register
          </h2>

          <FormUpdateUser></FormUpdateUser>
        </article>
      </section>
    </main>
  );
};
