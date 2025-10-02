import { BsChevronLeft } from "react-icons/bs";
import { Link } from "react-router-dom";

import { ListStats } from "@src/components/ListStats/ListStats";
import { Loader } from "@src/components/Loader/Loader";

import { useUsersContext } from "@src/context/UsersContext/UsersProvider";
import { useModeContext } from "@src/context/ModeContext/ModeProvider";

import "@src/pages/MenuModePage/MenuModePage.css";

export const MenuModePage = (): JSX.Element => {
  const { topUsers } = useUsersContext();
  const { mode } = useModeContext();

  if (mode.loading) {
    return (
      <main className="menu-mode-main">
        <Loader></Loader>
      </main>
    );
  }

  return (
    <main className="menu-mode-main">
      <Link to="/menu" aria-label="go home">
        <BsChevronLeft id="go-back" className="icon-go-back"></BsChevronLeft>
      </Link>

      <section className="menu-mode-page">
        <h1 className="menu-mode-page__title">{mode.mode?.name} MODE</h1>

        <article className="menu-mode-page__explication">
          <p className="menu-mode-page__description">
            {mode.mode?.description}
          </p>

          <Link
            to={`/menu/${mode.mode?._id}/start`}
            aria-label="play"
            className="menu-mode-page__play"
          >
            ¡PLAY!
          </Link>
        </article>

        {topUsers.loading ? (
          <Loader></Loader>
        ) : (
          <ListStats
            nameTop={`${mode.mode?.name!.toUpperCase()} TOP USERS`}
            arrayTop={topUsers.users!}
          ></ListStats>
        )}
      </section>
    </main>
  );
};
