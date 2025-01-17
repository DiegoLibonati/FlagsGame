import { UserWithOutPassword } from "../../entities/entities";

import "./ListStats.css";

interface ListStatsProps {
  nameTop: string;
  arrayTop: UserWithOutPassword[];
}

export const ListStats = ({
  nameTop,
  arrayTop,
}: ListStatsProps): JSX.Element => {
  return (
    <article className="top mode__top">
      <h2>{nameTop}</h2>

      <ul className="top__list mode__top__list">
        {arrayTop.map((top) => {
          const { _id, username, score } = top;

          return (
            <li key={_id}>
              {username} with {score} PTS
            </li>
          );
        })}
      </ul>
    </article>
  );
};
