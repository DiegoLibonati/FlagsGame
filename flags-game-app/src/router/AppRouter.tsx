import { Navigate, Route, Routes } from "react-router-dom";

import { FlagsGameRoute } from "@src/router/FlagsGameRoute";

import { HomePage } from "@src/pages/HomePage/HomePage";
import { GamePage } from "@src/pages/GamePage/GamePage";
import { MenuPage } from "@src/pages/MenuPage/MenuPage";
import { FinishGamePage } from "@src/pages/FinishGamePage/FinishGamePage";
import { StartGamePage } from "@src/pages/StartGamePage/StartGamePage";
import { MenuModePage } from "@src/pages/MenuModePage/MenuModePage";

import { ModesProvider } from "@src/contexts/ModesContext/ModesContext";
import { UsersProvider } from "@src/contexts/UsersContext/UsersContext";
import { ModeProvider } from "@src/contexts/ModeContext/ModeContext";
import { FlagsProvider } from "@src/contexts/FlagsContext/FlagsContext";
import { GameProvider } from "@src/contexts/GameContext/GameContext";

export const AppRouter = (): JSX.Element => {
  return (
    <Routes>
      <Route element={<FlagsGameRoute />}>
        <Route
          path="/"
          element={
            <UsersProvider>
              <HomePage></HomePage>
            </UsersProvider>
          }
        ></Route>

        <Route
          path="/menu"
          element={
            <ModesProvider>
              <MenuPage></MenuPage>
            </ModesProvider>
          }
        ></Route>

        <Route
          path="/menu/:idMode"
          element={
            <ModeProvider>
              <UsersProvider>
                <MenuModePage></MenuModePage>
              </UsersProvider>
            </ModeProvider>
          }
        ></Route>

        <Route
          path="/menu/:idMode/start"
          element={<StartGamePage></StartGamePage>}
        ></Route>

        <Route
          path="/menu/:idMode/*"
          element={
            <FlagsProvider>
              <ModeProvider>
                <GameProvider>
                  <Routes>
                    <Route path="game" element={<GamePage />} />
                    <Route path="finishgame" element={<FinishGamePage />} />
                  </Routes>
                </GameProvider>
              </ModeProvider>
            </FlagsProvider>
          }
        ></Route>
      </Route>

      <Route path="/*" element={<Navigate to="/"></Navigate>}></Route>
    </Routes>
  );
};
