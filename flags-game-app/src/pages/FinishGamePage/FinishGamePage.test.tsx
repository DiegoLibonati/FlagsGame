import { screen, render, within } from "@testing-library/react";
import user from "@testing-library/user-event";

import { MemoryRouter, Route, Routes } from "react-router-dom";

import { FinishGamePage } from "./FinishGamePage";

import { createServer } from "../../tests/msw/server";
import {
  FLAGS_DATA_STATIC_TEST,
  MODE_DATA_STATIC_TEST,
} from "../../tests/jest.constants";

import { FlagsProvider } from "../../context/FlagsContext/FlagsProvider";
import { GameProvider } from "../../context/GameContext/GameProvider";
import { AlertProvider } from "../../context/AlertContext/AlertProvider";

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
    createServer([
      {
        path: `/v1/flags/random/:quantity`,
        method: "get",
        res: () => {
          return {
            data: FLAGS_DATA_STATIC_TEST,
          };
        },
      },
    ]);

    test("It must render the main of game page.", async () => {
      await asyncRenderComponent();

      const main = screen.getByRole("main");

      expect(main).toBeInTheDocument();
    });

    test("It must render the alert without content and with the alert class only.", async () => {
      const { container } = await asyncRenderComponent();

      // eslint-disable-next-line
      const alertHeading = container.querySelector(".alert");

      expect(alertHeading).toBeInTheDocument();
    });
  });

  describe("Register Form", () => {
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

    test("It must render the register user form with its respective title.", async () => {
      const { container } = await asyncRenderComponent();

      // eslint-disable-next-line
      const articleRegisterUser = container.querySelector(
        ".register__article"
      ) as HTMLElement;

      const heading = within(articleRegisterUser).getByRole("heading", {
        name: /if you dont have a user register/i,
      });
      // eslint-disable-next-line
      const formRegister = container.querySelector(
        ".form__register"
      ) as HTMLFormElement;

      const scoreHeading = within(formRegister).getByRole("heading", {
        name: /your score was: 0 pts/i,
      });
      const inputUsername = within(formRegister).getByPlaceholderText(
        /your username goes here/i
      );
      const inputPassword = within(formRegister).getByPlaceholderText(
        /your password goes here/i
      );
      const buttonSubmit = within(formRegister).getByRole("button", {
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

    test("It must render the alert with the message in the messageService variable.", async () => {
      const username = "Pepe";
      const password = "1234";

      const { container } = await asyncRenderComponent();

      // eslint-disable-next-line
      const articleRegisterUser = container.querySelector(
        ".register__article"
      ) as HTMLElement;

      const heading = within(articleRegisterUser).getByRole("heading", {
        name: /if you dont have a user register/i,
      });
      // eslint-disable-next-line
      const formRegister = container.querySelector(
        ".form__register"
      ) as HTMLFormElement;

      const scoreHeading = within(formRegister).getByRole("heading", {
        name: /your score was: 0 pts/i,
      });
      const inputUsername = within(formRegister).getByPlaceholderText(
        /your username goes here/i
      );
      const inputPassword = within(formRegister).getByPlaceholderText(
        /your password goes here/i
      );
      const buttonSubmit = within(formRegister).getByRole("button", {
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

      // eslint-disable-next-line
      const alertHeading = container.querySelector(".alert");

      expect(alertHeading).toBeInTheDocument();
      expect(alertHeading).toHaveClass("alert success");
      expect(alertHeading).toHaveTextContent(messageService);
    });
  });

  describe("Register Form - Result not ok in addOrModifyUser service", () => {
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

    test("It must render the alert with the message in the messageService variable", async () => {
      const username = "Pepe";
      const password = "1234";

      const { container } = await asyncRenderComponent();

      // eslint-disable-next-line
      const articleRegisterUser = container.querySelector(
        ".register__article"
      ) as HTMLElement;

      const heading = within(articleRegisterUser).getByRole("heading", {
        name: /if you dont have a user register/i,
      });
      // eslint-disable-next-line
      const formRegister = container.querySelector(
        ".form__register"
      ) as HTMLFormElement;

      const scoreHeading = within(formRegister).getByRole("heading", {
        name: /your score was: 0 pts/i,
      });
      const inputUsername = within(formRegister).getByPlaceholderText(
        /your username goes here/i
      );
      const inputPassword = within(formRegister).getByPlaceholderText(
        /your password goes here/i
      );
      const buttonSubmit = within(formRegister).getByRole("button", {
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

      // eslint-disable-next-line
      const alertHeading = container.querySelector(".alert");

      expect(alertHeading).toBeInTheDocument();
      expect(alertHeading).toHaveClass("alert error");
      expect(alertHeading).toHaveTextContent(messageService);
    });
  });

  describe("Update Form", () => {
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

    test("It must render the update user form with its respective title.", async () => {
      const { container } = await asyncRenderComponent();

      // eslint-disable-next-line
      const articleUpdateUser = container.querySelector(
        ".update__article"
      ) as HTMLElement;

      const heading = within(articleUpdateUser).getByRole("heading", {
        name: /if you have a user register/i,
      });
      // eslint-disable-next-line
      const formUpdate = container.querySelector(
        ".form__update"
      ) as HTMLFormElement;

      const scoreHeading = within(formUpdate).getByRole("heading", {
        name: /your score was: 0 pts/i,
      });
      const inputUsername = within(formUpdate).getByPlaceholderText(
        /your username goes here/i
      );
      const inputPassword = within(formUpdate).getByPlaceholderText(
        /your password goes here/i
      );
      const buttonSubmit = within(formUpdate).getByRole("button", {
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
        method: "put",
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

      // eslint-disable-next-line
      const articleUpdateUser = container.querySelector(
        ".update__article"
      ) as HTMLElement;

      const heading = within(articleUpdateUser).getByRole("heading", {
        name: /if you have a user register/i,
      });
      // eslint-disable-next-line
      const formUpdate = container.querySelector(
        ".form__update"
      ) as HTMLFormElement;

      const scoreHeading = within(formUpdate).getByRole("heading", {
        name: /your score was: 0 pts/i,
      });
      const inputUsername = within(formUpdate).getByPlaceholderText(
        /your username goes here/i
      );
      const inputPassword = within(formUpdate).getByPlaceholderText(
        /your password goes here/i
      );
      const buttonSubmit = within(formUpdate).getByRole("button", {
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

      // eslint-disable-next-line
      const alertHeading = container.querySelector(".alert");

      expect(alertHeading).toBeInTheDocument();
      expect(alertHeading).toHaveClass("alert success");
      expect(alertHeading).toHaveTextContent(messageService);
    });
  });

  describe("Update Form - Result not ok in addOrModifyUser service", () => {
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
        method: "put",
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

      // eslint-disable-next-line
      const articleUpdateUser = container.querySelector(
        ".update__article"
      ) as HTMLElement;

      const heading = within(articleUpdateUser).getByRole("heading", {
        name: /if you have a user register/i,
      });
      // eslint-disable-next-line
      const updateForm = container.querySelector(
        ".form__update"
      ) as HTMLFormElement;

      const scoreHeading = within(updateForm).getByRole("heading", {
        name: /your score was: 0 pts/i,
      });
      const inputUsername = within(updateForm).getByPlaceholderText(
        /your username goes here/i
      );
      const inputPassword = within(updateForm).getByPlaceholderText(
        /your password goes here/i
      );
      const buttonSubmit = within(updateForm).getByRole("button", {
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

      // eslint-disable-next-line
      const alertHeading = container.querySelector(".alert");

      expect(alertHeading).toBeInTheDocument();
      expect(alertHeading).toHaveClass("alert error");
      expect(alertHeading).toHaveTextContent(messageService);
    });
  });
});
