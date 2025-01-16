import { screen, render } from "@testing-library/react";

import { MemoryRouter, Route, Routes } from "react-router-dom";

import { StartGamePage } from "./StartGamePage";

type RenderComponent = {
  container: HTMLElement;
};

const currentPath = `/menu/Normal/start`;

const renderComponent = (): RenderComponent => {
  const { container } = render(
    <MemoryRouter
      initialEntries={[currentPath]}
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <Routes>
        <Route
          path="/menu/:mode/start"
          element={<StartGamePage></StartGamePage>}
        ></Route>
      </Routes>
    </MemoryRouter>
  );

  return {
    container: container,
  };
};

describe("StartGamePage.tsx", () => {
  describe("General Tests.", () => {
    test("It must render the main of menu page.", () => {
      renderComponent();

      const main = screen.getByRole("main");

      expect(main).toBeInTheDocument();
    });

    test("It must render the back button to return to the home page.", () => {
      renderComponent();

      const linkGoHome = screen.getByRole("link", {
        name: /go home/i,
      });

      expect(linkGoHome).toBeInTheDocument();
    });

    test("It must render the Start Game link.", () => {
      renderComponent();

      const linkStartGame = screen.getByRole("link", {
        name: /start game/i,
      });

      expect(linkStartGame).toBeInTheDocument();
      expect(linkStartGame).toHaveClass("start__game__btn");
    });
  });
});
