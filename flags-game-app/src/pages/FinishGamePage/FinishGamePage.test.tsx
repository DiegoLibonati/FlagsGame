import { screen, render, within } from "@testing-library/react";
import user from "@testing-library/user-event";

import { MemoryRouter, Route, Routes } from "react-router-dom";

import { FinishGamePage } from "@src/pages/FinishGamePage/FinishGamePage";
import { AlertProvider } from "@src/contexts/AlertContext/AlertContext";
import { FlagsProvider } from "@src/contexts/FlagsContext/FlagsContext";
import { GameProvider } from "@src/contexts/GameContext/GameContext";

import { usersApi } from "@src/api/users";

import { createServer } from "@tests/msw/server";
import { MODE_DATA_STATIC_TEST } from "@tests/jest.constants";

type RenderComponent = {
  container: HTMLElement;
};

const currentPath = `/menu/${MODE_DATA_STATIC_TEST.name}/finishgame`;

const asyncRenderComponent = async (): Promise<RenderComponent> => {
  const { container } = render(
    <MemoryRouter
      initialEntries={[currentPath]}
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <Routes>
        <Route
          path="/menu/:mode/finishgame"
          element={
            <AlertProvider>
              <FlagsProvider>
                <GameProvider>
                  <FinishGamePage></FinishGamePage>
                </GameProvider>
              </FlagsProvider>
            </AlertProvider>
          }
        ></Route>
      </Routes>
    </MemoryRouter>
  );

  await screen.findAllByRole("heading");

  return {
    container: container,
  };
};

describe("FinishGamePage.tsx", () => {
  describe("General Tests", () => {
    test("It must render the main of game page.", async () => {
      await asyncRenderComponent();

      const main = screen.getByRole("main");

      expect(main).toBeInTheDocument();
    });

    test("It must render the alert without content and with the alert class only.", async () => {
      const { container } = await asyncRenderComponent();

      const alertHeading =
        container.querySelector<HTMLHeadingElement>(".alert");

      expect(alertHeading).toBeInTheDocument();
    });
  });

  describe("Register Form", () => {
    test("It must render the register user form with its respective title.", async () => {
      const { container } = await asyncRenderComponent();

      const articleRegisterUser = container.querySelector<HTMLElement>(
        ".finish-game-page__wrapper-register"
      );

      const heading = within(articleRegisterUser!).getByRole("heading", {
        name: /if you dont have a user register/i,
      });
      const formRegister = container.querySelector<HTMLFormElement>(
        ".form-register-user"
      );

      const scoreHeading = within(formRegister!).getByRole("heading", {
        name: /your score was: 0 pts/i,
      });
      const inputUsername = within(formRegister!).getByPlaceholderText(
        /your username goes here/i
      );
      const inputPassword = within(formRegister!).getByPlaceholderText(
        /your password goes here/i
      );
      const buttonSubmit = within(formRegister!).getByRole("button", {
        name: /send and register/i,
      });

      expect(heading).toBeInTheDocument();
      expect(formRegister).toBeInTheDocument();
      expect(scoreHeading).toBeInTheDocument();
      expect(inputUsername).toBeInTheDocument();
      expect(inputPassword).toBeInTheDocument();
      expect(buttonSubmit).toBeInTheDocument();
    });
  });

  describe("Register Form - Result ok in addOrModifyUser service", () => {
    const messageService = "Success";

    createServer([
      {
        path: `${usersApi}/`,
        method: "post",
        status: 200,
        res: () => {
          return {
            message: messageService,
          };
        },
      },
    ]);

    test("It must render the alert with the message in the messageService variable.", async () => {
      const username = "Pepe";
      const password = "1234";

      const { container } = await asyncRenderComponent();

      const articleRegisterUser = container.querySelector<HTMLElement>(
        ".finish-game-page__wrapper-register"
      );

      const heading = within(articleRegisterUser!).getByRole("heading", {
        name: /if you dont have a user register/i,
      });
      const formRegister = container.querySelector<HTMLFormElement>(
        ".form-register-user"
      );

      const scoreHeading = within(formRegister!).getByRole("heading", {
        name: /your score was: 0 pts/i,
      });
      const inputUsername = within(formRegister!).getByPlaceholderText(
        /your username goes here/i
      );
      const inputPassword = within(formRegister!).getByPlaceholderText(
        /your password goes here/i
      );
      const buttonSubmit = within(formRegister!).getByRole("button", {
        name: /send and register/i,
      });

      expect(heading).toBeInTheDocument();
      expect(formRegister).toBeInTheDocument();
      expect(scoreHeading).toBeInTheDocument();
      expect(inputUsername).toBeInTheDocument();
      expect(inputPassword).toBeInTheDocument();
      expect(buttonSubmit).toBeInTheDocument();

      await user.click(inputUsername);
      await user.keyboard(username);

      await user.click(inputPassword);
      await user.keyboard(password);

      await user.click(buttonSubmit);

      const alertHeading =
        container.querySelector<HTMLHeadingElement>(".alert");

      expect(alertHeading).toBeInTheDocument();
      expect(alertHeading).toHaveClass("alert alert--success");
      expect(alertHeading).toHaveTextContent(messageService);
    });
  });

  describe("Register Form - Result not ok in addOrModifyUser service", () => {
    const messageService = "Error";

    createServer([
      {
        path: `${usersApi}/`,
        method: "post",
        status: 400,
        res: () => {
          return {
            message: messageService,
          };
        },
      },
    ]);

    test("It must render the alert with the message in the messageService variable", async () => {
      const username = "Pepe";
      const password = "1234";

      const { container } = await asyncRenderComponent();

      const articleRegisterUser = container.querySelector<HTMLElement>(
        ".finish-game-page__wrapper-register"
      );

      const heading = within(articleRegisterUser!).getByRole("heading", {
        name: /if you dont have a user register/i,
      });
      const formRegister = container.querySelector<HTMLFormElement>(
        ".form-register-user"
      );

      const scoreHeading = within(formRegister!).getByRole("heading", {
        name: /your score was: 0 pts/i,
      });
      const inputUsername = within(formRegister!).getByPlaceholderText(
        /your username goes here/i
      );
      const inputPassword = within(formRegister!).getByPlaceholderText(
        /your password goes here/i
      );
      const buttonSubmit = within(formRegister!).getByRole("button", {
        name: /send and register/i,
      });

      expect(heading).toBeInTheDocument();
      expect(formRegister).toBeInTheDocument();
      expect(scoreHeading).toBeInTheDocument();
      expect(inputUsername).toBeInTheDocument();
      expect(inputPassword).toBeInTheDocument();
      expect(buttonSubmit).toBeInTheDocument();

      await user.click(inputUsername);
      await user.keyboard(username);

      await user.click(inputPassword);
      await user.keyboard(password);

      await user.click(buttonSubmit);

      const alertHeading =
        container.querySelector<HTMLHeadingElement>(".alert");

      expect(alertHeading).toBeInTheDocument();
      expect(alertHeading).toHaveClass("alert alert--error");
      expect(alertHeading).toHaveTextContent(messageService);
    });
  });

  describe("Update Form", () => {
    test("It must render the update user form with its respective title.", async () => {
      const { container } = await asyncRenderComponent();

      const articleUpdateUser = container.querySelector<HTMLElement>(
        ".finish-game-page__wrapper-update"
      );

      const heading = within(articleUpdateUser!).getByRole("heading", {
        name: /if you have a user register/i,
      });
      const formUpdate =
        container.querySelector<HTMLFormElement>(".form-update-user");

      const scoreHeading = within(formUpdate!).getByRole("heading", {
        name: /your score was: 0 pts/i,
      });
      const inputUsername = within(formUpdate!).getByPlaceholderText(
        /your username goes here/i
      );
      const inputPassword = within(formUpdate!).getByPlaceholderText(
        /your password goes here/i
      );
      const buttonSubmit = within(formUpdate!).getByRole("button", {
        name: /send and replace/i,
      });

      expect(heading).toBeInTheDocument();
      expect(formUpdate).toBeInTheDocument();
      expect(scoreHeading).toBeInTheDocument();
      expect(inputUsername).toBeInTheDocument();
      expect(inputPassword).toBeInTheDocument();
      expect(buttonSubmit).toBeInTheDocument();
    });
  });

  describe("Update Form - Result ok in addOrModifyUser service", () => {
    const messageService = "Success";

    createServer([
      {
        path: `${usersApi}/`,
        method: "patch",
        status: 200,
        res: () => {
          return {
            message: messageService,
          };
        },
      },
    ]);

    test("It must render the alert with the message in the messageService variable.", async () => {
      const username = "Pepe";
      const password = "1234";

      const { container } = await asyncRenderComponent();

      const articleUpdateUser = container.querySelector<HTMLElement>(
        ".finish-game-page__wrapper-update"
      );

      const heading = within(articleUpdateUser!).getByRole("heading", {
        name: /if you have a user register/i,
      });
      const formUpdate =
        container.querySelector<HTMLFormElement>(".form-update-user");

      const scoreHeading = within(formUpdate!).getByRole("heading", {
        name: /your score was: 0 pts/i,
      });
      const inputUsername = within(formUpdate!).getByPlaceholderText(
        /your username goes here/i
      );
      const inputPassword = within(formUpdate!).getByPlaceholderText(
        /your password goes here/i
      );
      const buttonSubmit = within(formUpdate!).getByRole("button", {
        name: /send and replace/i,
      });

      expect(heading).toBeInTheDocument();
      expect(formUpdate).toBeInTheDocument();
      expect(scoreHeading).toBeInTheDocument();
      expect(inputUsername).toBeInTheDocument();
      expect(inputPassword).toBeInTheDocument();
      expect(buttonSubmit).toBeInTheDocument();

      await user.click(inputUsername);
      await user.keyboard(username);

      await user.click(inputPassword);
      await user.keyboard(password);

      await user.click(buttonSubmit);

      const alertHeading =
        container.querySelector<HTMLHeadingElement>(".alert");

      expect(alertHeading).toBeInTheDocument();
      expect(alertHeading).toHaveClass("alert alert--success");
      expect(alertHeading).toHaveTextContent(messageService);
    });
  });

  describe("Update Form - Result not ok in addOrModifyUser service", () => {
    const messageService = "Error";

    createServer([
      {
        path: `${usersApi}/`,
        method: "patch",
        status: 400,
        res: () => {
          return {
            message: messageService,
          };
        },
      },
    ]);

    test("It must render the alert with the message in the messageService variable.", async () => {
      const username = "Pepe";
      const password = "1234";

      const { container } = await asyncRenderComponent();

      const articleUpdateUser = container.querySelector<HTMLElement>(
        ".finish-game-page__wrapper-update"
      );

      const heading = within(articleUpdateUser!).getByRole("heading", {
        name: /if you have a user register/i,
      });
      const updateForm =
        container.querySelector<HTMLFormElement>(".form-update-user");

      const scoreHeading = within(updateForm!).getByRole("heading", {
        name: /your score was: 0 pts/i,
      });
      const inputUsername = within(updateForm!).getByPlaceholderText(
        /your username goes here/i
      );
      const inputPassword = within(updateForm!).getByPlaceholderText(
        /your password goes here/i
      );
      const buttonSubmit = within(updateForm!).getByRole("button", {
        name: /send and replace/i,
      });

      expect(heading).toBeInTheDocument();
      expect(updateForm).toBeInTheDocument();
      expect(scoreHeading).toBeInTheDocument();
      expect(inputUsername).toBeInTheDocument();
      expect(inputPassword).toBeInTheDocument();
      expect(buttonSubmit).toBeInTheDocument();

      await user.click(inputUsername);
      await user.keyboard(username);

      await user.click(inputPassword);
      await user.keyboard(password);

      await user.click(buttonSubmit);

      const alertHeading =
        container.querySelector<HTMLHeadingElement>(".alert");

      expect(alertHeading).toBeInTheDocument();
      expect(alertHeading).toHaveClass("alert alert--error");
      expect(alertHeading).toHaveTextContent(messageService);
    });
  });
});
