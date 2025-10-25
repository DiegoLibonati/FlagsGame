import { screen, render, within } from "@testing-library/react";
import user from "@testing-library/user-event";

import { MemoryRouter } from "react-router-dom";

import { Navbar } from "@src/components/Navbar/Navbar";

import { UiProvider } from "@src/contexts/UiContext/UiContext";

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
      <UiProvider>
        <Navbar></Navbar>
      </UiProvider>
    </MemoryRouter>
  );

  return {
    container: container,
  };
};

describe("Navbar.tsx", () => {
  describe("General Tests.", () => {
    test("It must render the Navbar component.", () => {
      renderComponent();

      const navbar = screen.getByRole("navigation");

      expect(navbar).toBeInTheDocument();
      expect(navbar).toHaveClass("header__nav");
    });

    test("It must render the title of the application.", () => {
      renderComponent();

      const titleApp = screen.getByRole("link", {
        name: /title FlagsGame/i,
      });

      expect(titleApp).toBeInTheDocument();
    });

    test("It should the hamburger component and when clicked it should open the navbar.", async () => {
      renderComponent();

      const hamburger = screen.getByRole("button", {
        name: /main menu/i,
      });

      expect(hamburger).toBeInTheDocument();

      await user.click(hamburger);

      expect(hamburger).toHaveClass("hamburger hamburger--open");

      const navbar = screen.getByRole("navigation");

      expect(navbar).toBeInTheDocument();
      expect(navbar).toHaveClass("header__nav header__nav--open");
    });

    test("It should render the navbar link list, the links are home and menu.", () => {
      renderComponent();

      const navLinks = ["home", "menu"];

      const list = screen.getByRole("list");

      expect(list).toBeInTheDocument();
      expect(list).toHaveClass("header__nav-list");

      const navLinksElements = within(list).getAllByRole("listitem");

      expect(navLinksElements).toHaveLength(navLinks.length);

      for (let navLink of navLinks) {
        const nLink = screen.getByRole("link", {
          name: new RegExp(navLink),
        });

        expect(nLink).toBeInTheDocument();
        expect(nLink).toHaveClass("header__nav-link");
      }
    });
  });
});
