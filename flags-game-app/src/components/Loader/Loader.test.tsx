import { render } from "@testing-library/react";

import { Loader } from "@src/components/Loader/Loader";

type RenderComponent = {
  container: HTMLElement;
};

const renderComponent = (): RenderComponent => {
  const { container } = render(<Loader></Loader>);

  return {
    container: container,
  };
};

describe("Loader.tsx", () => {
  describe("General Tests.", () => {
    test("You must render the Loader component.", () => {
      const { container } = renderComponent();

      // eslint-disable-next-line
      const loader = container.querySelector(".loader");

      expect(loader).toBeInTheDocument();
    });
  });
});
