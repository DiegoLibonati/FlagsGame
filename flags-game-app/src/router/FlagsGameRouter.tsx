import { BrowserRouter } from "react-router-dom";

import { Navbar } from "../components/Navbar/Navbar";

import { PublicRoutes } from "./routes/PublicRoutes/PublicRoutes";

export const FlagsGameRouter = (): JSX.Element => {
  return (
    <BrowserRouter>
      <Navbar></Navbar>

      <PublicRoutes></PublicRoutes>
    </BrowserRouter>
  );
};
