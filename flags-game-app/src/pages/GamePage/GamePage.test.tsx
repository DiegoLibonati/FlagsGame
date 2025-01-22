import { screen, render, within } from "@testing-library/react";
import user from "@testing-library/user-event";

import { MemoryRouter, Route, Routes } from "react-router-dom";

import { GamePage } from "./GamePage";

import { createServer } from "../../tests/msw/server";
import {
  FLAG_DATA_STATIC_TEST,
  FLAGS_DATA_STATIC_TEST,
  MODE_DATA_STATIC_TEST,
} from "../../tests/jest.constants";

import { FlagsProvider } from "../../context/FlagsContext/FlagsProvider";
import { GameProvider } from "../../context/GameContext/GameProvider";
import { ModeProvider } from "../../context/ModeContext/ModeProvider";
import { parseZero } from "../../helpers/parseZero";

type RenderComponent = {
  container: HTMLElement;
};

const currentPath = `/menu/${MODE_DATA_STATIC_TEST.name}/game`;

const renderComponent = (): RenderComponent => {
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
          path="/menu/:mode/game"
          element={
            <ModeProvider>
              <FlagsProvider>
                <GameProvider>
                  <GamePage></GamePage>
                </GameProvider>
              </FlagsProvider>
            </ModeProvider>
          }
        ></Route>
      </Routes>
    </MemoryRouter>
  );

  return {
    container: container,
  };
};

const renderComponentAsync = async (): Promise<RenderComponent> => {
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
          path="/menu/:mode/game"
          element={
            <ModeProvider>
              <FlagsProvider>
                <GameProvider>
                  <GamePage></GamePage>
                </GameProvider>
              </FlagsProvider>
            </ModeProvider>
          }
        ></Route>
      </Routes>
    </MemoryRouter>
  );

  await screen.findByRole("img");

  return {
    container: container,
  };
};

const secondsToTimer = (seconds: number) => {
  const hours = parseZero(Math.floor(seconds / 3600));
  const minutes = parseZero(Math.floor((seconds % 3600) / 60));
  const secs = parseZero(seconds % 60);

  return `${hours}:${minutes}:${secs}`;
};

describe("GamePage.tsx", () => {
  describe("General Tests.", () => {
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
      {
        path: `/v1/modes/findmode/:mode`,
        method: "get",
        res: () => {
          return {
            data: MODE_DATA_STATIC_TEST,
          };
        },
      },
    ]);

    test("It must render the main of game page.", async () => {
      await renderComponentAsync();

      const main = screen.getByRole("main");

      expect(main).toBeInTheDocument();
    });

    test("It must render a loader before render modes in menu page.", () => {
      const { container } = renderComponent();

      //eslint-disable-next-line
      const loader = container.querySelector(".loader");
      const linkGoHome = screen.queryByRole("link", {
        name: /go home/i,
      });

      expect(loader).toBeInTheDocument();
      expect(linkGoHome).not.toBeInTheDocument();
    });

    test("It should render the page title, the flag to guess, the form to guess, the score and the remaining time.", async () => {
      const { container } = await renderComponentAsync();

      const heading = screen.getByRole("heading", {
        name: /guess the flag/i,
      });
      const flag = screen.getByRole("img");
      // eslint-disable-next-line
      const form = container.querySelector(".form-guess-flag");
      const score = screen.getByRole("heading", {
        name: /score: 0 pts/i,
      });
      const timeleft = screen.getByRole("heading", {
        name: /time left: /i,
      });

      expect(heading).toBeInTheDocument();

      expect(flag).toBeInTheDocument();
      expect(flag).toHaveAttribute("src", FLAG_DATA_STATIC_TEST.image);
      expect(flag).toHaveAttribute("alt", FLAG_DATA_STATIC_TEST.name);

      expect(form).toBeInTheDocument();
      expect(score).toBeInTheDocument();

      expect(timeleft).toBeInTheDocument();
      expect(timeleft).toHaveTextContent(
        `Time left: ${secondsToTimer(MODE_DATA_STATIC_TEST.timeleft)}`
      );
    });
  });

  describe("If you guess the flag.", () => {
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
      {
        path: `/v1/modes/findmode/:mode`,
        method: "get",
        res: () => {
          return {
            data: MODE_DATA_STATIC_TEST,
          };
        },
      },
    ]);

    test("It should change the score, reset the form and the flag should change to the next one.", async () => {
      const firstFlag = FLAG_DATA_STATIC_TEST;
      const secondFlag = FLAGS_DATA_STATIC_TEST[1];
      const initialScore = 0;

      const { container } = await renderComponentAsync();

      //eslint-disable-next-line
      const form = container.querySelector(".form-guess-flag") as HTMLFormElement;
      const input = within(form).getByPlaceholderText(
        /enter a country name.../i
      );
      const submitButton = within(form).getByRole("button", {
        name: /submit/i,
      });

      expect(form).toBeInTheDocument();
      expect(input).toBeInTheDocument();
      expect(submitButton).toBeInTheDocument();

      const flag = screen.getByRole("img");
      const score = screen.getByRole("heading", {
        name: /score: 0 pts/i,
      });

      expect(flag).toBeInTheDocument();
      expect(flag).toHaveAttribute("src", firstFlag.image);
      expect(flag).toHaveAttribute("alt", firstFlag.name);
      expect(score).toBeInTheDocument();

      await user.click(input);
      await user.keyboard(firstFlag.name);

      await user.click(submitButton);

      expect(input).not.toHaveValue();
      expect(input).toHaveStyle("borderColor: green;");

      const nextFlag = screen.getByRole("img");

      expect(flag).not.toBeInTheDocument();
      expect(nextFlag).toBeInTheDocument();
      expect(nextFlag).toHaveAttribute("src", secondFlag.image);
      expect(nextFlag).toHaveAttribute("alt", secondFlag.name);

      const totalScore =
        initialScore +
        MODE_DATA_STATIC_TEST.timeleft * MODE_DATA_STATIC_TEST.multiplier;

      expect(score).toHaveTextContent(`Score: ${totalScore} PTS`);
    });
  });

  describe("If the flag is NOT guessed.", () => {
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
      {
        path: `/v1/modes/findmode/:mode`,
        method: "get",
        res: () => {
          return {
            data: MODE_DATA_STATIC_TEST,
          };
        },
      },
    ]);

    test("The score must remain the same, reset the form and the flag must be the same.", async () => {
      const firstFlag = FLAG_DATA_STATIC_TEST;
      const secondFlag = FLAGS_DATA_STATIC_TEST[1];
      const wrongFlagName = "Asd";
      const initialScore = 0;

      const { container } = await renderComponentAsync();

      //eslint-disable-next-line
      const form = container.querySelector(".form-guess-flag") as HTMLFormElement;
      const input = within(form).getByPlaceholderText(
        /enter a country name.../i
      );
      const submitButton = within(form).getByRole("button", {
        name: /submit/i,
      });

      expect(form).toBeInTheDocument();
      expect(input).toBeInTheDocument();
      expect(submitButton).toBeInTheDocument();

      const flag = screen.getByRole("img");
      const score = screen.getByRole("heading", {
        name: /score: 0 pts/i,
      });

      expect(flag).toBeInTheDocument();
      expect(flag).toHaveAttribute("src", firstFlag.image);
      expect(flag).toHaveAttribute("alt", firstFlag.name);
      expect(score).toBeInTheDocument();

      await user.click(input);
      await user.keyboard(wrongFlagName);

      await user.click(submitButton);

      expect(input).not.toHaveValue();
      expect(input).toHaveStyle("borderColor: red;");

      expect(flag).toBeInTheDocument();
      expect(flag).toHaveAttribute("src", firstFlag.image);
      expect(flag).toHaveAttribute("alt", firstFlag.name);
      expect(flag).not.toHaveAttribute("src", secondFlag.image);
      expect(flag).not.toHaveAttribute("alt", secondFlag.name);

      const totalScore = initialScore;

      expect(score).toHaveTextContent(`Score: ${totalScore} PTS`);
    });
  });
});
