import { Link } from "react-router-dom";

import { ListStats } from "@src/components/ListStats/ListStats";
import { Loader } from "@src/components/Loader/Loader";

import { useUsersContext } from "@src/context/UsersContext/UsersProvider";

import "@src/pages/HomePage/HomePage.css";

export const HomePage = (): JSX.Element => {
  const { topUsers } = useUsersContext();

  return (
    <main className="home-main">
      <section className="home-page">
        <article className="home-page__actions">
          <Link to="/menu" aria-label="lets play" className="home-page__play">
            ¡Lets PLAY!
          </Link>
        </article>

        {topUsers.loading ? (
          <Loader></Loader>
        ) : (
          <ListStats
            nameTop={"GLOBAL TOP USERS"}
            arrayTop={topUsers.users!}
          ></ListStats>
        )}
      </section>
    </main>
  );
};
