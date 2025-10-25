import { Fragment } from "react/jsx-runtime";
import { Outlet } from "react-router-dom";

import { Navbar } from "@src/components/Navbar/Navbar";

export const FlagsGameRoute = () => {
  return (
    <Fragment>
      <Navbar></Navbar>
      <Outlet />
    </Fragment>
  );
};
