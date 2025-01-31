import { Link } from "react-router-dom";

import { Loader } from "../../components/Loader/Loader";

import { useModesContext } from "../../context/ModesContext/ModesProvider";

import { BsChevronLeft } from "react-icons/bs";

import "./MenuPage.css";

export const MenuPage = (): JSX.Element => {
  const { modes } = useModesContext()!;

  if (modes.loading)
    return (
      <main>
        <Loader></Loader>
      </main>
    );

  return (
    <main className="menu-main">
      <Link to="/" aria-label="go home">
        <BsChevronLeft id="go-back" className="icon-go-back"></BsChevronLeft>
      </Link>

      <section className="menu-page">
        <h1 className="menu-page__title">Choose a MODE</h1>
        <article className="menu-page__modes">
          {modes.modes!.map((mode) => {
            return (
              <Link
                key={mode._id}
                to={`/menu/${mode.name}`}
                className="menu-page__mode"
                aria-label={`select ${mode.name} to play`}
              >
                {mode.name} MODE
              </Link>
            );
          })}
        </article>
      </section>
    </main>
  );
};
