import { screen, render } from "@testing-library/react";
import user from "@testing-library/user-event";

import { HamburgerProps } from "@src/entities/props";

import { Hamburger } from "@src/components/Hamburger/Hamburger";

type RenderComponent = {
  props: {
    manageNavbar: jest.Mock;
  } & HamburgerProps;
  container: HTMLElement;
};

interface RenderComponentProps {
  navbar: boolean;
}

const renderComponent = ({ navbar }: RenderComponentProps): RenderComponent => {
  const props = {
    navbar: navbar,
    manageNavbar: jest.fn(),
  };

  const { container } = render(
    <Hamburger
      navbar={props.navbar}
      manageNavbar={props.manageNavbar}
    ></Hamburger>
  );

  return {
    props: props,
    container: container,
  };
};

describe("Hamburger.tsx", () => {
  describe("General Tests.", () => {
    test("You must render the Hamburger.", () => {
      renderComponent({ navbar: false });

      const hamburger = screen.getByRole("button", {
        name: /main menu/i,
      });

      expect(hamburger).toBeInTheDocument();
    });

    test("Must render menu class if navbar prop is false.", () => {
      renderComponent({ navbar: false });

      const hamburger = screen.getByRole("button", {
        name: /main menu/i,
      });

      expect(hamburger).toBeInTheDocument();
      expect(hamburger).toHaveClass("hamburger");
    });

    test("Must render menu open class if navbar prop is true.", () => {
      renderComponent({ navbar: true });

      const hamburger = screen.getByRole("button", {
        name: /main menu/i,
      });

      expect(hamburger).toBeInTheDocument();
      expect(hamburger).toHaveClass("hamburger hamburger--open");
    });

    test("You must run the manageNavbar function when you click on Hamburger.", async () => {
      const { props } = renderComponent({ navbar: false });

      const hamburger = screen.getByRole("button", {
        name: /main menu/i,
      });

      await user.click(hamburger);

      expect(hamburger).toBeInTheDocument();
      expect(props.manageNavbar).toHaveBeenCalledTimes(1);
    });
  });
});
