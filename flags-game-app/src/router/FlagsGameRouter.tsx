import { BrowserRouter } from "react-router-dom";

import { Navbar } from "@src/components/Navbar/Navbar";

import { PublicRoutes } from "@src/router/routes/PublicRoutes/PublicRoutes";

export const FlagsGameRouter = (): JSX.Element => {
  return (
    <BrowserRouter
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <Navbar></Navbar>

      <PublicRoutes></PublicRoutes>
    </BrowserRouter>
  );
};
