import { screen, render } from "@testing-library/react";

import { MemoryRouter } from "react-router-dom";

import { FormRegisterUser } from "@src/components/Forms/FormRegisterUser/FormRegisterUser";

import { AlertContext } from "@src/contexts/AlertContext/AlertContext";
import { FlagsProvider } from "@src/contexts/FlagsContext/FlagsContext";
import { GameProvider } from "@src/contexts/GameContext/GameContext";

import { ALERT_PROVIDER_STATIC } from "@tests/jest.constants";

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
    beforeEach(() => {
      jest.clearAllMocks();
    });

    test("It must render the form.", async () => {
      const { container } = await renderComponent();

      const form = container.querySelector<HTMLFormElement>(
        ".form-register-user"
      );

      expect(form).toBeInTheDocument();
      expect(form).toHaveClass("form-register-user");
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
});
