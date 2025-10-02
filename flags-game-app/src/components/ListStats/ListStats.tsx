import { ListStatsProps } from "@src/entities/props";

import "@src/components/ListStats/ListStats.css";

export const ListStats = ({
  nameTop,
  arrayTop,
}: ListStatsProps): JSX.Element => {
  return (
    <article className="list-stats">
      <h2 className="list-stats__title">{nameTop}</h2>

      <ul className="list-stats__users">
        {arrayTop.map((top) => {
          const { _id, username, score } = top;

          return (
            <li key={_id} className="list-stats__user">
              {username} with {score} PTS
            </li>
          );
        })}
      </ul>
    </article>
  );
};
