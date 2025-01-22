import { screen, render, within } from "@testing-library/react";

import { UserWithOutPassword } from "../../entities/entities";

import { ListStats } from "./ListStats";

type RenderComponent = {
  props: {
    nameTop: string;
    arrayTop: UserWithOutPassword[];
  };
  container: HTMLElement;
};

const renderComponent = (): RenderComponent => {
  const props = {
    nameTop: "Global Top",
    arrayTop: [
      {
        _id: "672a713141aec0b5e6b0a1a2",
        score: 6925,
        username: "TITO",
      },
      {
        _id: "672b76e474e247da51a8bd3a",
        score: 234,
        username: "pipo",
      },
    ],
  };

  const { container } = render(
    <ListStats nameTop={props.nameTop} arrayTop={props.arrayTop}></ListStats>
  );

  return {
    props: props,
    container: container,
  };
};

describe("ListStats.tsx", () => {
  describe("General Tests.", () => {
    test("You must render the ListStats component.", () => {
      renderComponent();

      const listStats = screen.getByRole("article");

      expect(listStats).toBeInTheDocument();
      expect(listStats).toHaveClass("top__mode");
    });

    test("It must render the top with title, the totality of users of the top and match the first user of the top.", () => {
      const { props } = renderComponent();

      const firstUser = props.arrayTop![0];

      const heading = screen.getByRole("heading", {
        name: props.nameTop,
      });

      expect(heading).toBeInTheDocument();
      expect(heading).toHaveTextContent(props.nameTop);

      const listTop = screen.getByRole("list");

      expect(listTop).toBeInTheDocument();
      expect(listTop).toHaveClass("top__mode-list");

      const usersTop = screen.getAllByRole("listitem");

      expect(usersTop).toHaveLength(props.arrayTop!.length);

      const firstUserTop = within(listTop).getByText(
        `${firstUser.username} with ${firstUser.score} PTS`
      );

      expect(firstUserTop).toBeInTheDocument();
    });
  });
});
