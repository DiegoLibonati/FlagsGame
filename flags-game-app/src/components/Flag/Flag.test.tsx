import { screen, render } from "@testing-library/react";

import { FlagProps } from "@src/entities/props";

import { Flag } from "@src/components/Flag/Flag";

type RenderComponent = {
  props: FlagProps;
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

describe("Flag.tsx", () => {
  describe("General Tests.", () => {
    test("You must render the Flag component with its respective props.", () => {
      const { props } = renderComponent();

      const flag = screen.getByRole("img");

      expect(flag).toBeInTheDocument();
      expect(flag).toHaveAttribute("src", props.image);
      expect(flag).toHaveAttribute("alt", props.name);
    });
  });
});
