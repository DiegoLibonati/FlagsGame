import { screen, render, within } from "@testing-library/react";

import { MemoryRouter } from "react-router-dom";

import { HomePage } from "@src/pages/HomePage/HomePage";

import { UsersProvider } from "@src/contexts/UsersContext/UsersContext";

import { usersApi } from "@src/api/users";

import { createServer } from "@tests/msw/server";
import { USERS_TOP_STATIC_TEST } from "@tests/jest.constants";

type RenderComponent = {
  container: HTMLElement;
};

const renderComponent = (): RenderComponent => {
  const { container } = render(
    <MemoryRouter
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <UsersProvider>
        <HomePage></HomePage>
      </UsersProvider>
    </MemoryRouter>
  );

  return {
    container: container,
  };
};

const renderComponentAsync = async (): Promise<RenderComponent> => {
  const { container } = render(
    <MemoryRouter
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <UsersProvider>
        <HomePage></HomePage>
      </UsersProvider>
    </MemoryRouter>
  );

  await screen.findByRole("list");

  return {
    container: container,
  };
};

describe("HomePage.tsx", () => {
  describe("General Tests.", () => {
    createServer([
      {
        path: `${usersApi}/top_global`,
        method: "get",
        res: () => {
          return {
            data: USERS_TOP_STATIC_TEST,
          };
        },
      },
    ]);

    test("It must render the main of home page.", async () => {
      await renderComponentAsync();

      const main = screen.getByRole("main");

      expect(main).toBeInTheDocument();
    });

    test("It must render a loader before the top load is completed and must not display the list of users.", () => {
      const { container } = renderComponent();

      const loader = container.querySelector<HTMLSpanElement>(".loader");
      const list = screen.queryByRole("list");

      expect(loader).toBeInTheDocument();
      expect(list).not.toBeInTheDocument();
    });

    test("It should render the link to play and the top list of general users.", async () => {
      await renderComponentAsync();

      const letsPlay = screen.getByRole("link", {
        name: /lets play/i,
      });
      const userTopTitle = screen.getByRole("heading", {
        name: /global top users/i,
      });
      const usersTopList = screen.getByRole("list");

      expect(letsPlay).toBeInTheDocument();
      expect(userTopTitle).toBeInTheDocument();

      expect(usersTopList).toBeInTheDocument();
      expect(usersTopList).toHaveClass("list-stats__users");

      const usersInList = within(usersTopList).getAllByRole("listitem");

      expect(usersInList).toHaveLength(USERS_TOP_STATIC_TEST.length);
    });
  });
});
