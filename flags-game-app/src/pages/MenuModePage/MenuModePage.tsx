import { Link } from "react-router-dom";

import { ListStats } from "../../components/ListStats/ListStats";
import { Loader } from "../../components/Loader/Loader";

import { useUsersContext } from "../../context/UsersContext/UsersProvider";
import { useModeContext } from "../../context/ModeContext/ModeProvider";

import { BsChevronLeft } from "react-icons/bs";

import "./MenuModePage.css";

export const MenuModePage = (): JSX.Element => {
  const { topUsers } = useUsersContext();
  const { mode } = useModeContext();

  if (mode.loading) {
    return (
      <main>
        <Loader></Loader>
      </main>
    );
  }

  return (
    <main>
      <Link to="/menu" aria-label="go home">
        <BsChevronLeft id="go-back"></BsChevronLeft>
      </Link>

      <section className="mode_container">
        <h1>{mode.mode?.name} MODE</h1>

        <article className="mode_container_explain">
          <p>{mode.mode?.description}</p>

          <Link to={`/menu/${mode.mode?.name}/start`} aria-label="play">
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
