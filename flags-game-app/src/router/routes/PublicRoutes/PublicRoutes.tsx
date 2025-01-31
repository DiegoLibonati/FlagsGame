import { Route, Routes } from "react-router-dom";

import { HomePage } from "../../../pages/HomePage/HomePage";
import { MenuPage } from "../../../pages/MenuPage/MenuPage";
import { MenuModePage } from "../../../pages/MenuModePage/MenuModePage";
import { GamePage } from "../../../pages/GamePage/GamePage";
import { StartGamePage } from "../../../pages/StartGamePage/StartGamePage";
import { FinishGamePage } from "../../../pages/FinishGamePage/FinishGamePage";

import { UsersProvider } from "../../../context/UsersContext/UsersProvider";
import { ModesProvider } from "../../../context/ModesContext/ModesProvider";
import { ModeProvider } from "../../../context/ModeContext/ModeProvider";
import { FlagsProvider } from "../../../context/FlagsContext/FlagsProvider";
import { GameProvider } from "../../../context/GameContext/GameProvider";

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
        path="/menu/:mode"
        element={
          <ModeProvider>
            <UsersProvider>
              <MenuModePage></MenuModePage>
            </UsersProvider>
          </ModeProvider>
        }
      ></Route>

      <Route
        path="/menu/:mode/*"
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
        path="/menu/:mode/start"
        element={<StartGamePage></StartGamePage>}
      ></Route>
    </Routes>
  );
};
