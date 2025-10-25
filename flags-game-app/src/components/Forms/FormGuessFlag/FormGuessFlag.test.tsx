import { screen, render } from "@testing-library/react";

import { FormGuessFlagProps } from "@src/entities/props";

import { FormGuessFlag } from "@src/components/Forms/FormGuessFlag/FormGuessFlag";

import { FlagsProvider } from "@src/contexts/FlagsContext/FlagsContext";
import { ModeProvider } from "@src/contexts/ModeContext/ModeContext";
import { GameProvider } from "@src/contexts/GameContext/GameContext";

type RenderComponent = {
  props: FormGuessFlagProps;
  container: HTMLElement;
};

const renderComponent = (): RenderComponent => {
  const props = {
    secondsLeft: 20,
  };

  const { container } = render(
    <FlagsProvider>
      <ModeProvider>
        <GameProvider>
          <FormGuessFlag secondsLeft={props.secondsLeft}></FormGuessFlag>
        </GameProvider>
      </ModeProvider>
    </FlagsProvider>
  );

  return {
    props: props,
    container: container,
  };
};

describe("FormGuessFlag.tsx", () => {
  describe("General Tests.", () => {
    test("It must render the form.", () => {
      const { container } = renderComponent();

      const form = container.querySelector<HTMLFormElement>(".form-guess-flag");

      expect(form).toBeInTheDocument();
      expect(form).toHaveClass("form-guess-flag");
    });

    test("It must render an input name to enter the name of the flag and a submit button.", () => {
      renderComponent();

      const inputName = screen.getByPlaceholderText(/enter a country name.../i);
      const submitButton = screen.getByRole("button", {
        name: /submit/i,
      });

      expect(inputName).toBeInTheDocument();
      expect(inputName).toHaveAttribute("name", "name");
      expect(submitButton).toBeInTheDocument();
    });
  });
});
