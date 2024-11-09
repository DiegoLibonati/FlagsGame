import { screen, render } from "@testing-library/react";
import user from "@testing-library/user-event";

import { Hamburger } from "./Hamburger";

type RenderComponent = {
  props: {
    navbar: boolean;
    mockManageNavbar: jest.Mock;
  };
  container: HTMLElement;
};

interface RenderComponentProps {
  navbar: boolean;
}

const renderComponent = ({ navbar }: RenderComponentProps): RenderComponent => {
  const props = {
    navbar: navbar,
    mockManageNavbar: jest.fn(),
  };

  const { container } = render(
    <Hamburger
      navbar={props.navbar}
      manageNavbar={props.mockManageNavbar}
    ></Hamburger>
  );

  return {
    props: props,
    container: container,
  };
};

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
  expect(hamburger).toHaveClass("menu");
});

test("Must render menu opened class if navbar prop is true.", () => {
  renderComponent({ navbar: true });

  const hamburger = screen.getByRole("button", {
    name: /main menu/i,
  });

  expect(hamburger).toBeInTheDocument();
  expect(hamburger).toHaveClass("menu opened");
});

test("You must run the manageNavbar function when you click on Hamburger.", async () => {
  const { props } = renderComponent({ navbar: false });

  const hamburger = screen.getByRole("button", {
    name: /main menu/i,
  });

  await user.click(hamburger);

  expect(hamburger).toBeInTheDocument();
  expect(props.mockManageNavbar).toHaveBeenCalledTimes(1);
});
