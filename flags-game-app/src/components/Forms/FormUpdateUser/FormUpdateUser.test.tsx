import { screen, render } from "@testing-library/react";
import user from "@testing-library/user-event";

import { MemoryRouter } from "react-router-dom";

import { FormUpdateUser } from "./FormUpdateUser";

import { AlertContext } from "../../../context/AlertContext/AlertContext";
import { GameProvider } from "../../../context/GameContext/GameProvider";
import { FlagsProvider } from "../../../context/FlagsContext/FlagsProvider";

import { createServer } from "../../../tests/msw/server";
import {
  ALERT_PROVIDER_STATIC,
  FLAGS_DATA_STATIC_TEST,
} from "../../../tests/constants/constants";

type RenderComponent = {
  container: HTMLElement;
};

const renderComponent = async (): Promise<RenderComponent> => {
  const { container } = render(
    <MemoryRouter>
      <AlertContext.Provider value={{ ...ALERT_PROVIDER_STATIC }}>
        <FlagsProvider>
          <GameProvider>
            <FormUpdateUser></FormUpdateUser>
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

describe("General Tests", () => {
  createServer([
    {
      path: "/v1/flags/:mode",
      method: "get",
      res: () => {
        return {
          data: FLAGS_DATA_STATIC_TEST,
        };
      },
    },
  ]);

  test("It must render the form.", async () => {
    const { container } = await renderComponent();

    //eslint-disable-next-line
    const form = container.querySelector(".send_points_container_mini_form");

    expect(form).toBeInTheDocument();
    expect(form).toHaveClass("send_points_container_mini_form");
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
      name: /send and replace/i,
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
      path: "/v1/flags/:mode",
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
      res: () => {
        return {
          message: messageService,
        };
      },
    },
  ]);

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
      name: /send and replace/i,
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
      type: "success",
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
      path: "/v1/flags/:mode",
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
      name: /send and replace/i,
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
      type: "error",
      message: messageService,
    });
    expect(inputUsername).not.toHaveValue();
    expect(inputPassword).not.toHaveValue();
  });
});
