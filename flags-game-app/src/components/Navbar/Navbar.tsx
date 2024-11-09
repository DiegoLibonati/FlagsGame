import { Link, NavLink } from "react-router-dom";

import { Hamburger } from "../Hamburger/Hamburger";

import { useUiContext } from "../../context/UiContext/UiProvider";

import "./Navbar.css";

export const Navbar = (): JSX.Element => {
  const { navbar, handleManageNavbar } = useUiContext();

  return (
    <header className="header_container">
      <div className="header_container_logo">
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
          navbar ? "header_container_nav open-nav" : "header_container_nav"
        }
      >
        <ul className="header_container_nav_list">
          <li>
            <NavLink
              to="/"
              aria-label="home"
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
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
                isActive ? "nav-link active" : "nav-link"
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
