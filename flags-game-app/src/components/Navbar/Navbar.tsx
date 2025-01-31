import { Link, NavLink } from "react-router-dom";

import { Hamburger } from "../Hamburger/Hamburger";

import { useUiContext } from "../../context/UiContext/UiProvider";

import "./Navbar.css";

export const Navbar = (): JSX.Element => {
  const { navbar, handleManageNavbar } = useUiContext();

  return (
    <header className="header-wrapper">
      <div className="header__logo">
        <Link
          to="/"
          aria-label="title FlagsGame"
          className="header__title"
        >
          FlagsGame
        </Link>

        <Hamburger
          navbar={navbar}
          manageNavbar={handleManageNavbar}
        ></Hamburger>
      </div>

      <nav className={navbar ? "header__nav header__nav--open" : "header__nav"}>
        <ul className="header__nav-list">
          <li className="header__nav-list-item">
            <NavLink
              to="/"
              aria-label="home"
              className={({ isActive }) =>
                isActive ? "header__nav-link header__nav-link--active" : "header__nav-link"
              }
            >
              Home
            </NavLink>
          </li>
          <li className="header__nav-list-item">
            <NavLink
              to="/menu"
              aria-label="menu"
              className={({ isActive }) =>
                isActive ? "header__nav-link header__nav-link--active" : "header__nav-link"
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
