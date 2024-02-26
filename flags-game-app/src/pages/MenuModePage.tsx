import { useEffect } from "react";
import { useContext } from "react";
import { Link, useParams } from "react-router-dom";
import { ListStats } from "../components/ListStats";
import { FlagsContext } from "../context/FlagsContext";
import { Loader } from "../components/Loader";
import { BsChevronLeft } from "react-icons/bs";
import "./MenuModePage.css";
import { getTopMode } from "../api/getTopMode";
import { findMode } from "../api/findMode";

export const MenuModePage = (): JSX.Element => {
  const {
    actualMode,
    topArr,
    topLoading,
    modeLoading,
    setActualMode,
    setTopArr,
    setModeLoading,
    setTopLoading,
  } = useContext(FlagsContext)!;

  const { mode } = useParams();

  const handleMode = async (): Promise<void> => {
    setModeLoading(true);

    const request = await findMode(mode!);

    const data = await request.json();

    setActualMode(data);

    setModeLoading(false);
  };

  const handleTop = async (): Promise<void> => {
    setTopLoading(true);

    const request = await getTopMode(mode!);

    const data = await request.json();

    setTopArr(data);

    setTopLoading(false);
  };

  useEffect(() => {
    handleTop();
    handleMode();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode]);

  if (modeLoading) {
    return <Loader></Loader>;
  } else {
    return (
      <main>
        <Link to="/menu">
          <BsChevronLeft id="go-back"></BsChevronLeft>
        </Link>
        <section className="mode_container">
          <h1>{actualMode?.name} MODE</h1>

          <article className="mode_container_explain">
            <p>{actualMode?.description}</p>

            <Link to={`/menu/${mode}/play`}>¡PLAY!</Link>
          </article>

          <ListStats
            nametop={`${mode!.toUpperCase()} TOP USERS`}
            arrayTop={topArr}
            isLoadingTop={topLoading}
            actualMode={mode!}
          ></ListStats>
        </section>
      </main>
    );
  }
};
