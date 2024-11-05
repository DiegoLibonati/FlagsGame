import { useEffect } from "react";
import { Link, useParams } from "react-router-dom";

import { ListStats } from "../../components/ListStats/ListStats";
import { Loader } from "../../components/Loader/Loader";

import { getTopMode } from "../../api/getTopMode";
import { findMode } from "../../api/findMode";
import { useModesContext } from "../../context/ModesContext/ModesProvider";
import { useUsersContext } from "../../context/UsersContext/UsersProvider";

import { BsChevronLeft } from "react-icons/bs";

import "./MenuModePage.css";

export const MenuModePage = (): JSX.Element => {
  const { actualMode, handleSetActualMode, handleClearActualMode } =
    useModesContext()!;
  const { topUsers, handleSetTopUsers, handleClearTopUsers } =
    useUsersContext();

  const { mode } = useParams();

  const handleMode = async (): Promise<void> => {
    const request = await findMode(mode!);

    const data = await request.json();

    handleSetActualMode(data.data);
  };

  const handleTopMode = async (): Promise<void> => {
    const request = await getTopMode(mode!);

    const data = await request.json();

    handleSetTopUsers(data.data);
  };

  useEffect(() => {
    handleTopMode();
    handleMode();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode]);

  useEffect(() => {
    return () => {
      handleClearTopUsers();
      handleClearActualMode();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!actualMode) {
    return <Loader></Loader>;
  }

  return (
    <main>
      <Link to="/menu">
        <BsChevronLeft id="go-back"></BsChevronLeft>
      </Link>
      <section className="mode_container">
        <h1>{actualMode?.name} MODE</h1>

        <article className="mode_container_explain">
          <p>{actualMode?.description}</p>

          <Link to={`/menu/${mode}/start`}>¡PLAY!</Link>
        </article>

        <ListStats
          nametop={`${mode!.toUpperCase()} TOP USERS`}
          arrayTop={topUsers}
        ></ListStats>
      </section>
    </main>
  );
};
