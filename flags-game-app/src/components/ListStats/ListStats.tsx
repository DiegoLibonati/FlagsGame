import { ListStatsProps } from "../../entities/entities";

import { Loader } from "../Loader/Loader";

import "./ListStats.css";

export const ListStats = ({
  nametop,
  arrayTop,
}: ListStatsProps): JSX.Element => {
  if (!arrayTop) return <Loader></Loader>;

  return (
    <article className="list_stats_container_top menu_mode_top">
      <h2>{nametop}</h2>

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
