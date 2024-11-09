import { Link, useParams } from "react-router-dom";

import { BsChevronLeft } from "react-icons/bs";

import "./StartGamePage.css";

export const StartGamePage = (): JSX.Element => {
  const { mode } = useParams();

  return (
    <main>
      <Link to={`/menu/${mode}`} aria-label="go home">
        <BsChevronLeft id="go-back"></BsChevronLeft>
      </Link>

      <section className="section_btn_start">
        <Link
          to={`/menu/${mode}/game`}
          className="btn-start-game"
          aria-label="start game"
        >
          START GAME
        </Link>
      </section>
    </main>
  );
};
