import { useEffect } from "react";
import { Link } from "react-router-dom";

import { Loader } from "../../components/Loader/Loader";

import { getModes } from "../../api/getModes";
import { useModesContext } from "../../context/ModesContext/ModesProvider";

import { BsChevronLeft } from "react-icons/bs";

import "./MenuPage.css";

export const MenuPage = (): JSX.Element => {
  const { modes, handleSetModes, handleClearModes } = useModesContext()!;

  const handleGetModes = async (): Promise<void> => {
    const request = await getModes();
    const data = await request.json();

    handleSetModes(data.data);
  };

  useEffect(() => {
    handleGetModes();

    return () => {
      handleClearModes();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!modes)
    return (
      <main>
        <Loader></Loader>
      </main>
    );

  return (
    <main>
      <Link to="/"></Link>
      <BsChevronLeft id="go-back"></BsChevronLeft>
      <section className="menu_container">
        <h1>Choose a MODE</h1>
        <article className="menu_container_option">
          {modes.map((mode) => {
            return (
              <Link key={mode._id} to={`/menu/${mode.name}`}>
                {mode.name} MODE
              </Link>
            );
          })}
        </article>
      </section>
    </main>
  );
};
