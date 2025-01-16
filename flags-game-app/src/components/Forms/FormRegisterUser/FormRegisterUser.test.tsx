import { screen, render } from "@testing-library/react";
import user from "@testing-library/user-event";

import { MemoryRouter } from "react-router-dom";

import { FormRegisterUser } from "./FormRegisterUser";

import { createServer } from "../../../tests/msw/server";
import {
  ALERT_PROVIDER_STATIC,
  FLAGS_DATA_STATIC_TEST,
} from "../../../tests/jest.constants";

import { AlertContext } from "../../../context/AlertContext/AlertContext";
import { FlagsProvider } from "../../../context/FlagsContext/FlagsProvider";
import { GameProvider } from "../../../context/GameContext/GameProvider";

type RenderComponent = {
  container: HTMLElement;
};

const renderComponent = async (): Promise<RenderComponent> => {
  const { container } = render(
    <MemoryRouter
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <AlertContext.Provider value={{ ...ALERT_PROVIDER_STATIC }}>
        <FlagsProvider>
          <GameProvider>
            <FormRegisterUser></FormRegisterUser>
          </GameProvider>
        </FlagsProvider>
      </AlertContext.Provider>
    </MemoryRouter>
  );

  await screen.findByRole("heading");

  return {
    container: container,
  };
};

describe("FormRegisterUser.tsx", () => {
  describe("General Tests", () => {
    createServer([
      {
        path: "/v1/flags/random/:quantity",
        method: "get",
        res: () => {
          return {
            data: FLAGS_DATA_STATIC_TEST,
          };
        },
      },
    ]);

    beforeEach(() => {
      jest.clearAllMocks();
    });

    test("It must render the form.", async () => {
      const { container } = await renderComponent();

      //eslint-disable-next-line
      const form = container.querySelector(".form__send__points");

      expect(form).toBeInTheDocument();
      expect(form).toHaveClass("form__send__points");
    });

    test("It must render the content of the form. A title, a username input, a password input and a submit button.", async () => {
      await renderComponent();

      const heading = screen.getByRole("heading", {
        name: `Your score was: 0 PTS`,
      });
      const inputUsername = screen.getByPlaceholderText(
        /Your username goes here/i
      );
      const inputPassword = screen.getByPlaceholderText(
        /Your password goes here/i
      );
      const submitButton = screen.getByRole("button", {
        name: /send and register/i,
      });

      expect(heading).toBeInTheDocument();
      expect(inputUsername).toBeInTheDocument();
      expect(inputUsername).toHaveAttribute("name", "username");
      expect(inputPassword).toBeInTheDocument();
      expect(inputPassword).toHaveAttribute("name", "password");
      expect(submitButton).toBeInTheDocument();
    });
  });

  describe("Result is ok. AddOrModifyUser Service", () => {
    const messageService = "Success";

    createServer([
      {
        path: "/v1/flags/random/:quantity",
        method: "get",
        res: () => {
          return {
            data: FLAGS_DATA_STATIC_TEST,
          };
        },
      },
      {
        path: `/v1/users/addormodify`,
        method: "post",
        status: 200,
        res: () => {
          return {
            message: messageService,
          };
        },
      },
    ]);

    beforeEach(() => {
      jest.clearAllMocks();
    });

    test("It should send the form when you click submit.", async () => {
      await renderComponent();

      const heading = screen.getByRole("heading", {
        name: `Your score was: 0 PTS`,
      });
      const inputUsername = screen.getByPlaceholderText(
        /Your username goes here/i
      );
      const inputPassword = screen.getByPlaceholderText(
        /Your password goes here/i
      );
      const submitButton = screen.getByRole("button", {
        name: /send and register/i,
      });

      expect(heading).toBeInTheDocument();
      expect(inputUsername).toBeInTheDocument();
      expect(inputUsername).toHaveAttribute("name", "username");
      expect(inputPassword).toBeInTheDocument();
      expect(inputPassword).toHaveAttribute("name", "password");
      expect(submitButton).toBeInTheDocument();

      await user.click(inputUsername);
      await user.keyboard("Jose");

      await user.click(inputPassword);
      await user.keyboard("1234");

      await user.click(submitButton);

      expect(ALERT_PROVIDER_STATIC.handleSetAlert).toHaveBeenCalledTimes(1);
      expect(ALERT_PROVIDER_STATIC.handleSetAlert).toHaveBeenCalledWith({
        type: "alert-auth-success",
        message: messageService,
      });
      expect(inputUsername).not.toHaveValue();
      expect(inputPassword).not.toHaveValue();
    });
  });

  describe("Result is NOT ok. AddOrModifyUser Service", () => {
    const messageService = "Error";

    createServer([
      {
        path: "/v1/flags/random/:quantity",
        method: "get",
        res: () => {
          return {
            data: FLAGS_DATA_STATIC_TEST,
          };
        },
      },
      {
        path: `/v1/users/addormodify`,
        method: "post",
        status: 400,
        res: () => {
          return {
            message: messageService,
          };
        },
      },
    ]);

    beforeEach(() => {
      jest.clearAllMocks();
    });

    test("It should send the form when you click submit.", async () => {
      await renderComponent();

      const heading = screen.getByRole("heading", {
        name: `Your score was: 0 PTS`,
      });
      const inputUsername = screen.getByPlaceholderText(
        /Your username goes here/i
      );
      const inputPassword = screen.getByPlaceholderText(
        /Your password goes here/i
      );
      const submitButton = screen.getByRole("button", {
        name: /send and register/i,
      });

      expect(heading).toBeInTheDocument();
      expect(inputUsername).toBeInTheDocument();
      expect(inputUsername).toHaveAttribute("name", "username");
      expect(inputPassword).toBeInTheDocument();
      expect(inputPassword).toHaveAttribute("name", "password");
      expect(submitButton).toBeInTheDocument();

      await user.click(inputUsername);
      await user.keyboard("Jose");

      await user.click(inputPassword);
      await user.keyboard("1234");

      await user.click(submitButton);

      expect(ALERT_PROVIDER_STATIC.handleSetAlert).toHaveBeenCalledTimes(1);
      expect(ALERT_PROVIDER_STATIC.handleSetAlert).toHaveBeenCalledWith({
        type: "alert-auth-error",
        message: messageService,
      });
      expect(inputUsername).not.toHaveValue();
      expect(inputPassword).not.toHaveValue();
    });
  });
});
