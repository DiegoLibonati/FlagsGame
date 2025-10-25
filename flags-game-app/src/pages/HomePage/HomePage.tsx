import { useEffect } from "react";
import { Link } from "react-router-dom";

import { ListStats } from "@src/components/ListStats/ListStats";
import { Loader } from "@src/components/Loader/Loader";

import { useUsersContext } from "@src/hooks/useUsersContext";

import { getTopGeneral } from "@src/api/get/getTopGeneral";

import "@src/pages/HomePage/HomePage.css";

export const HomePage = (): JSX.Element => {
  const {
    topUsers,
    handleStartFetchUsers,
    handleSetTopUsers,
    handleEndFetchUsers,
    handleSetErrorUsers,
    handleClearTopUsers,
  } = useUsersContext();

  const handleGetGeneralTopUsers = async () => {
    try {
      handleStartFetchUsers();
      const response = await getTopGeneral();
      handleSetTopUsers(response.data);
    } catch (error) {
      handleSetErrorUsers(String(error));
    } finally {
      handleEndFetchUsers();
    }
  };

  useEffect(() => {
    handleGetGeneralTopUsers();

    return () => {
      handleClearTopUsers();
    };
  }, []);

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
