import React from "react";
import { useContext } from "react";
import { useEffect } from "react";
import { Link } from "react-router-dom";
import { ListStats } from "../components/ListStats";
import { FlagsContext } from "../context/FlagsContext";
import "./HomePage.css";

export const HomePage = () => {
  const { arrayTop, isLoadingTop, setTopUrl } = useContext(FlagsContext);

  useEffect(() => {
    setTopUrl(`http://127.0.0.1:5000/users/top/general`);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <main>
        <section className="home_container">
          <article className="home_container_play">
            <Link to="/menu">¡Lets PLAY!</Link>
          </article>

          <ListStats
            nametop={"GLOBAL TOP USERS"}
            arrayTop={arrayTop}
            isLoadingTop={isLoadingTop}
            actualMode={"general_score"}
          ></ListStats>
        </section>
      </main>
    </>
  );
};
