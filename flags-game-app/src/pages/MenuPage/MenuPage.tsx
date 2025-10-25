import { useEffect } from "react";
import { Link } from "react-router-dom";
import { BsChevronLeft } from "react-icons/bs";

import { Loader } from "@src/components/Loader/Loader";

import { useModesContext } from "@src/hooks/useModesContext";

import { getModes } from "@src/api/get/getModes";

import "@src/pages/MenuPage/MenuPage.css";

export const MenuPage = (): JSX.Element => {
  const {
    modes,
    handleStartFetchModes,
    handleSetModes,
    handleSetErrorModes,
    handleEndFetchModes,
    handleClearModes,
  } = useModesContext()!;

  const handleGetModes = async () => {
    try {
      handleStartFetchModes();
      const response = await getModes();
      handleSetModes(response.data);
    } catch (error) {
      handleSetErrorModes(String(error));
    } finally {
      handleEndFetchModes();
    }
  };

  useEffect(() => {
    handleGetModes();

    return () => {
      handleClearModes();
    };
  }, []);

  if (modes.loading)
    return (
      <main>
        <Loader></Loader>
      </main>
    );

  return (
    <main className="menu-main">
      <Link to="/" aria-label="go home">
        <BsChevronLeft id="go-back" className="icon-go-back"></BsChevronLeft>
      </Link>

      <section className="menu-page">
        <h1 className="menu-page__title">Choose a MODE</h1>
        <article className="menu-page__modes">
          {modes.modes!.map((mode) => {
            return (
              <Link
                key={mode._id}
                to={`/menu/${mode._id}`}
                className="menu-page__mode"
                aria-label={`select ${mode.name} to play`}
              >
                {mode.name} MODE
              </Link>
            );
          })}
        </article>
      </section>
    </main>
  );
};
