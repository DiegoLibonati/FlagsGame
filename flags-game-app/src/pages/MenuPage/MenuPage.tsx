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
    <main>
      <Link to="/" aria-label="go home">
        <BsChevronLeft id="go-back"></BsChevronLeft>
      </Link>

      <section className="menu__page">
        <h1>Choose a MODE</h1>
        <article className="menu__page__option">
          {modes.modes!.map((mode) => {
            return (
              <Link
                key={mode._id}
                to={`/menu/${mode.name}`}
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
