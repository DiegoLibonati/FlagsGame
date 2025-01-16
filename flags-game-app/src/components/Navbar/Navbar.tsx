import { Link, NavLink } from "react-router-dom";

import { Hamburger } from "../Hamburger/Hamburger";

import { useUiContext } from "../../context/UiContext/UiProvider";

import "./Navbar.css";

export const Navbar = (): JSX.Element => {
  const { navbar, handleManageNavbar } = useUiContext();

  return (
    <header className="header">
      <div className="header__logo">
        <Link to="/" aria-label="title FlagsGame">
          FlagsGame
        </Link>

        <Hamburger
          navbar={navbar}
          manageNavbar={handleManageNavbar}
        ></Hamburger>
      </div>

      <nav
        className={
          navbar ? "header__nav open__nav" : "header__nav"
        }
      >
        <ul className="header__nav__list">
          <li>
            <NavLink
              to="/"
              aria-label="home"
              className={({ isActive }) =>
                isActive ? "nav__link active" : "nav__link"
              }
            >
              Home
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/menu"
              aria-label="menu"
              className={({ isActive }) =>
                isActive ? "nav__link active" : "nav__link"
              }
            >
              Menu
            </NavLink>
          </li>
        </ul>
      </nav>
    </header>
  );
};
