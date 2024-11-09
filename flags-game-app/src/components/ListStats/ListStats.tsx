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
    <article className="list_stats_container_top menu_mode_top">
      <h2>{nameTop}</h2>

      <ul className="list_stats_container_top_list menu_mode_top_list">
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
