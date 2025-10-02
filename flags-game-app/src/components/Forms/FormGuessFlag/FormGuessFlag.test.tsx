import { screen, render } from "@testing-library/react";
import user from "@testing-library/user-event";

import { createServer } from "@tests/msw/server";
import {
  FLAG_DATA_STATIC_TEST,
  FLAGS_DATA_STATIC_TEST,
  MODE_DATA_STATIC_TEST,
} from "@tests/jest.constants";

import { FormGuessFlagProps } from "@src/entities/props";

import { FormGuessFlag } from "@src/components/Forms/FormGuessFlag/FormGuessFlag";

import { apiRouteFlags, apiRouteModes } from "@src/api/apiRoute";
import { FlagsProvider } from "@src/context/FlagsContext/FlagsProvider";
import { ModeProvider } from "@src/context/ModeContext/ModeProvider";
import { GameProvider } from "@src/context/GameContext/GameProvider";

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
    createServer([
      {
        path: `${apiRouteFlags}/random/:quantity`,
        method: "get",
        res: () => {
          return {
            data: FLAGS_DATA_STATIC_TEST,
          };
        },
      },
      {
        path: `${apiRouteModes}/:idMode`,
        method: "get",
        res: () => {
          return {
            data: MODE_DATA_STATIC_TEST,
          };
        },
      },
    ]);

    test("It must render the form.", () => {
      const { container } = renderComponent();

      //eslint-disable-next-line
      const form = container.querySelector(".form-guess-flag");

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

  describe("Hit the flag name", () => {
    createServer([
      {
        path: `${apiRouteFlags}/random/:quantity`,
        method: "get",
        res: () => {
          return {
            data: FLAGS_DATA_STATIC_TEST,
          };
        },
      },
      {
        path: `${apiRouteModes}/:idMode`,
        method: "get",
        res: () => {
          return {
            data: MODE_DATA_STATIC_TEST,
          };
        },
      },
    ]);

    test("It should send the form when you click submit.", async () => {
      renderComponent();

      const inputName = screen.getByPlaceholderText(/enter a country name.../i);
      const submitButton = screen.getByRole("button", {
        name: /submit/i,
      });

      expect(inputName).toBeInTheDocument();
      expect(inputName).toHaveAttribute("name", "name");
      expect(submitButton).toBeInTheDocument();

      const flagToGuess = FLAG_DATA_STATIC_TEST.name;

      await user.click(inputName);
      await user.keyboard(flagToGuess);

      await user.click(submitButton);

      expect(inputName).toHaveStyle("borderColor: green;");
      expect(inputName).not.toHaveValue();
    });
  });

  describe("NOT hit the flag name", () => {
    createServer([
      {
        path: `${apiRouteFlags}/random/:quantity`,
        method: "get",
        res: () => {
          return {
            data: FLAGS_DATA_STATIC_TEST,
          };
        },
      },
      {
        path: `${apiRouteModes}/:idMode`,
        method: "get",
        res: () => {
          return {
            data: MODE_DATA_STATIC_TEST,
          };
        },
      },
    ]);

    test("It should send the form when you click submit. Not HIT the flag name", async () => {
      renderComponent();

      const inputName = screen.getByPlaceholderText(/enter a country name.../i);
      const submitButton = screen.getByRole("button", {
        name: /submit/i,
      });

      expect(inputName).toBeInTheDocument();
      expect(inputName).toHaveAttribute("name", "name");
      expect(submitButton).toBeInTheDocument();

      const flagToGuess = "Argentina";

      await user.click(inputName);
      await user.keyboard(flagToGuess);

      await user.click(submitButton);

      expect(flagToGuess === FLAG_DATA_STATIC_TEST.name).toBeFalsy();
      expect(inputName).toHaveStyle("borderColor: red;");
      expect(inputName).not.toHaveValue();
    });
  });
});
