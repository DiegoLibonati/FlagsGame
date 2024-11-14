import { screen, render, within } from "@testing-library/react";

import { MemoryRouter, Route, Routes } from "react-router-dom";

import { MenuModePage } from "./MenuModePage";

import { UsersProvider } from "../../context/UsersContext/UsersProvider";
import { ModeProvider } from "../../context/ModeContext/ModeProvider";

import { createServer } from "../../test/msw/server";
import {
  MODE_DATA_STATIC_TEST,
  USERS_TOP_STATIC_TEST,
} from "../../test/constants/constants";

type RenderComponent = {
  container: HTMLElement;
};

const currentPath = `/menu/${MODE_DATA_STATIC_TEST.name}`;

createServer([
  {
    path: `/v1/modes/mode/top/:mode`,
    method: "get",
    res: () => {
      return {
        data: USERS_TOP_STATIC_TEST,
      };
    },
  },
  {
    path: `/v1/modes/findmode/:mode`,
    method: "get",
    res: () => {
      return {
        data: MODE_DATA_STATIC_TEST,
      };
    },
  },
]);

const renderComponent = (): RenderComponent => {
  const { container } = render(
    <MemoryRouter initialEntries={[currentPath]}>
      <Routes>
        <Route
          path="/menu/:mode"
          element={
            <UsersProvider>
              <ModeProvider>
                <MenuModePage></MenuModePage>
              </ModeProvider>
            </UsersProvider>
          }
        ></Route>
      </Routes>
    </MemoryRouter>
  );

  return {
    container: container,
  };
};

const renderComponentAsync = async (): Promise<RenderComponent> => {
  const { container } = render(
    <MemoryRouter initialEntries={[currentPath]}>
      <Routes>
        <Route
          path="/menu/:mode"
          element={
            <UsersProvider>
              <ModeProvider>
                <MenuModePage></MenuModePage>
              </ModeProvider>
            </UsersProvider>
          }
        ></Route>
      </Routes>
    </MemoryRouter>
  );

  await screen.findByRole("link", {
    name: /go home/i,
  });

  return {
    container: container,
  };
};

test("It must render the main of menu mode page.", async () => {
  await renderComponentAsync();

  const main = screen.getByRole("main");

  expect(main).toBeInTheDocument();
});

test("It must render a loader before render modes in menu page.", () => {
  const { container } = renderComponent();

  //eslint-disable-next-line
  const loader = container.querySelector(".loader");
  const linkGoHome = screen.queryByRole("link", {
    name: /go home/i,
  });

  expect(loader).toBeInTheDocument();
  expect(linkGoHome).not.toBeInTheDocument();
});

test("It must render the back button to return to the home page.", async () => {
  await renderComponentAsync();

  const linkGoHome = screen.getByRole("link", {
    name: /go home/i,
  });

  expect(linkGoHome).toBeInTheDocument();
});

test("It must render the title, description and play button of the selected mode to play.", async () => {
  await renderComponentAsync();

  const heading = screen.getByRole("heading", {
    name: new RegExp(`${MODE_DATA_STATIC_TEST.name} MODE`),
  });
  const description = screen.getByText(MODE_DATA_STATIC_TEST.description);
  const playLink = screen.getByRole("link", {
    name: `play`,
  });

  expect(heading).toBeInTheDocument();
  expect(description).toBeInTheDocument();
  expect(playLink).toBeInTheDocument();
});

test("It must render the list of top users of the selected mode.", async () => {
  await renderComponentAsync();

  const list = screen.getByRole("list");
  const titleTop = screen.getByRole("heading", {
    name: `${MODE_DATA_STATIC_TEST.name.toUpperCase()} TOP USERS`,
  });

  expect(list).toBeInTheDocument();
  expect(list).toHaveClass("list_stats_container_top_list menu_mode_top_list");
  expect(titleTop).toBeInTheDocument();

  const usersInTop = within(list).getAllByRole("listitem");

  expect(usersInTop).toHaveLength(USERS_TOP_STATIC_TEST.length);
});
