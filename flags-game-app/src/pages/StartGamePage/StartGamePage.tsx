import { Link, useParams } from "react-router-dom";

import { BsChevronLeft } from "react-icons/bs";

import "./StartGamePage.css";

export const StartGamePage = (): JSX.Element => {
  const { mode } = useParams();

  return (
    <main className="start-game-main">
      <Link to={`/menu/${mode}`} aria-label="go home">
        <BsChevronLeft id="go-back" className="icon__go-back"></BsChevronLeft>
      </Link>

      <section className="start-game-page">
        <Link
          to={`/menu/${mode}/game`}
          className="start-game-page__btn-start"
          aria-label="start game"
        >
          START GAME
        </Link>
      </section>
    </main>
  );
};
