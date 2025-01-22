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
    <article className="top__mode">
      <h2 className="top__mode-title">{nameTop}</h2>

      <ul className="top__mode-list">
        {arrayTop.map((top) => {
          const { _id, username, score } = top;

          return (
            <li key={_id} className="top__mode-list-item">
              {username} with {score} PTS
            </li>
          );
        })}
      </ul>
    </article>
  );
};
