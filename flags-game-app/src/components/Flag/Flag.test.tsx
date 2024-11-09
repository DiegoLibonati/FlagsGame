import { screen, render } from "@testing-library/react";

import { Flag } from "./Flag";

type RenderComponent = {
  props: {
    image: string;
    name: string;
  };
  container: HTMLElement;
};

const renderComponent = (): RenderComponent => {
  const props = {
    image: "image.png",
    name: "image",
  };

  const { container } = render(
    <Flag image={props.image} name={props.name}></Flag>
  );

  return {
    props: props,
    container: container,
  };
};

test("You must render the Flag component with its respective props.", () => {
  const { props } = renderComponent();

  const flag = screen.getByRole("img");

  expect(flag).toBeInTheDocument();
  expect(flag).toHaveAttribute("src", props.image);
  expect(flag).toHaveAttribute("alt", props.name);
});
