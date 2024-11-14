import { screen, render } from "@testing-library/react";

import { MemoryRouter } from "react-router-dom";

import { MenuPage } from "./MenuPage";

import { ModesProvider } from "../../context/ModesContext/ModesProvider";

import { createServer } from "../../test/msw/server";
import { MODES_DATA_STATIC_TEST } from "../../test/constants/constants";

type RenderComponent = {
  container: HTMLElement;
};

createServer([
  {
    path: `/v1/modes`,
    method: "get",
    res: () => {
      return {
        data: MODES_DATA_STATIC_TEST,
      };
    },
  },
]);

const renderComponent = (): RenderComponent => {
  const { container } = render(
    <MemoryRouter>
      <ModesProvider>
        <MenuPage></MenuPage>
      </ModesProvider>
    </MemoryRouter>
  );

  return {
    container: container,
  };
};

const renderComponentAsync = async (): Promise<RenderComponent> => {
  const { container } = render(
    <MemoryRouter>
      <ModesProvider>
        <MenuPage></MenuPage>
      </ModesProvider>
    </MemoryRouter>
  );

  await screen.findByRole("link", {
    name: /go home/i,
  });

  return {
    container: container,
  };
};

test("It must render the main of menu page.", async () => {
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

test("It should render the menu page title and the list of links for each service mode.", async () => {
  await renderComponentAsync();

  const heading = screen.getByRole("heading", {
    name: /choose a mode/i,
  });

  expect(heading).toBeInTheDocument();

  for (let mode of MODES_DATA_STATIC_TEST) {
    const linkMode = screen.getByRole("link", {
      name: new RegExp(`select ${mode.name} to play`),
    });

    expect(linkMode).toBeInTheDocument();
  }
});
