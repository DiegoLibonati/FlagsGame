import { Link } from "react-router-dom";

import { ListStats } from "../../components/ListStats/ListStats";
import { Loader } from "../../components/Loader/Loader";

import { useUsersContext } from "../../context/UsersContext/UsersProvider";

import "./HomePage.css";

export const HomePage = (): JSX.Element => {
  const { topUsers } = useUsersContext();

  return (
    <main>
      <section className="home">
        <article className="home__play">
          <Link to="/menu" aria-label="lets play">
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
