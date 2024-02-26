import { useContext } from "react";
import { useEffect } from "react";
import { Link } from "react-router-dom";
import { ListStats } from "../components/ListStats";
import { FlagsContext } from "../context/FlagsContext";
import "./HomePage.css";
import { getTopGeneral } from "../api/getTopGeneral";

export const HomePage = (): JSX.Element => {
  const { topArr, topLoading, setTopArr, setTopLoading } =
    useContext(FlagsContext)!;

  const handleTopGeneral = async (): Promise<void> => {
    setTopLoading(true);

    const request = await getTopGeneral();

    const data = await request.json();

    setTopArr(data);

    setTopLoading(false);
  };

  useEffect(() => {
    handleTopGeneral();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main>
      <section className="home_container">
        <article className="home_container_play">
          <Link to="/menu">¡Lets PLAY!</Link>
        </article>

        <ListStats
          nametop={"GLOBAL TOP USERS"}
          actualMode={"general_score"}
          arrayTop={topArr}
          isLoadingTop={topLoading}
        ></ListStats>
      </section>
    </main>
  );
};
