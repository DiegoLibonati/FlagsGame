import { Route, Routes } from "react-router-dom";

import { HomePage } from "../../../pages/HomePage/HomePage";
import { MenuPage } from "../../../pages/MenuPage/MenuPage";
import { MenuModePage } from "../../../pages/MenuModePage/MenuModePage";
import { GamePage } from "../../../pages/GamePage/GamePage";
import { StartGamePage } from "../../../pages/StartGamePage/StartGamePage";
import { FinishGamePage } from "../../../pages/FinishGamePage/FinishGamePage";

export const PublicRoutes = (): JSX.Element => {
  return (
    <Routes>
      <Route path="/" element={<HomePage></HomePage>}></Route>
      <Route path="/menu" element={<MenuPage></MenuPage>}></Route>
      <Route path="/menu/:mode" element={<MenuModePage></MenuModePage>}></Route>
      <Route path="/menu/:mode/start" element={<StartGamePage></StartGamePage>}></Route>
      <Route path="/menu/:mode/game" element={<GamePage></GamePage>}></Route>
      <Route
        path="/menu/:mode/finishgame"
        element={<FinishGamePage></FinishGamePage>}
      ></Route>
    </Routes>
  );
};
