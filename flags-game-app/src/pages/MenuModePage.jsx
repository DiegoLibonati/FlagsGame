import React from "react";
import { useEffect } from "react";
import { useContext } from "react";
import { Link, useParams } from "react-router-dom";
import { ListStats } from "../components/ListStats";
import { FlagsContext } from "../context/FlagsContext";
import { Loader } from "../components/Loader";
import { BsChevronLeft } from "react-icons/bs";
import "./MenuModePage.css";

export const MenuModePage = () => {
  const {
    arrayMode,
    isLoadingMode,
    setModeUrl,
    arrayTop,
    isLoadingTop,
    setTopUrl,
  } = useContext(FlagsContext);

  const { mode } = useParams();

  useEffect(() => {
    setModeUrl(`http://127.0.0.1:5000/modes/findmode/${mode}`);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode]);

  useEffect(() => {
    setTopUrl(`http://127.0.0.1:5000/mode/top/${mode}`);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode]);

  const { name, description } = arrayMode;

  if (isLoadingMode) {
    <Loader></Loader>;
  } else {
    return (
      <main>
        <Link to="/menu">
          <BsChevronLeft id="go-back"></BsChevronLeft>
        </Link>
        <section className="mode_container">
          <h1>{name} MODE</h1>

          <article className="mode_container_explain">
            <p>{description}</p>

            <Link to={`/menu/${mode}/play`}>¡PLAY!</Link>
          </article>

          <ListStats
            nametop={`${mode.toUpperCase()} TOP USERS`}
            arrayTop={arrayTop}
            isLoadingTop={isLoadingTop}
            actualMode={mode}
          ></ListStats>
        </section>
      </main>
    );
  }
};
