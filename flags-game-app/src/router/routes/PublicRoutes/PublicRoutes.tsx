import { Route, Routes } from "react-router-dom";

import { HomePage } from "@src/pages/HomePage/HomePage";
import { MenuPage } from "@src/pages/MenuPage/MenuPage";
import { MenuModePage } from "@src/pages/MenuModePage/MenuModePage";
import { GamePage } from "@src/pages/GamePage/GamePage";
import { StartGamePage } from "@src/pages/StartGamePage/StartGamePage";
import { FinishGamePage } from "@src/pages/FinishGamePage/FinishGamePage";

import { UsersProvider } from "@src/context/UsersContext/UsersProvider";
import { ModesProvider } from "@src/context/ModesContext/ModesProvider";
import { ModeProvider } from "@src/context/ModeContext/ModeProvider";
import { FlagsProvider } from "@src/context/FlagsContext/FlagsProvider";
import { GameProvider } from "@src/context/GameContext/GameProvider";

export const PublicRoutes = (): JSX.Element => {
  return (
    <Routes>
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

      <Route
        path="/menu/:idMode/start"
        element={<StartGamePage></StartGamePage>}
      ></Route>
    </Routes>
  );
};
