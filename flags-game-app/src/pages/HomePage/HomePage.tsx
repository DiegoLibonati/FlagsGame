import { useEffect } from "react";
import { Link } from "react-router-dom";

import { ListStats } from "../../components/ListStats/ListStats";

import { useUsersContext } from "../../context/UsersContext/UsersProvider";
import { getTopGeneral } from "../../api/getTopGeneral";

import "./HomePage.css";

export const HomePage = (): JSX.Element => {
  const { topUsers, handleSetTopUsers, handleClearTopUsers } =
    useUsersContext();

  const handleTopGeneral = async (): Promise<void> => {
    const request = await getTopGeneral();

    const data = await request.json();

    handleSetTopUsers(data.data);
  };

  useEffect(() => {
    handleTopGeneral();

    return () => {
      handleClearTopUsers();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main>
      <section className="home_container">
        <article className="home_container_play">
          <Link to="/menu">¡Lets PLAY!</Link>
        </article>

        <ListStats nametop={"GLOBAL TOP USERS"} arrayTop={topUsers}></ListStats>
      </section>
    </main>
  );
};
