import { Link, useParams } from "react-router-dom";

import { BsChevronLeft } from "react-icons/bs";

import "@src/pages/StartGamePage/StartGamePage.css";

export const StartGamePage = (): JSX.Element => {
  const { idMode } = useParams();

  return (
    <main className="start-game-main">
      <Link to={`/menu/${idMode}`} aria-label="go home">
        <BsChevronLeft id="go-back" className="icon-go-back"></BsChevronLeft>
      </Link>

      <section className="start-game-page">
        <Link
          to={`/menu/${idMode}/game`}
          className="start-game-page__btn-start"
          aria-label="start game"
        >
          START GAME
        </Link>
      </section>
    </main>
  );
};
