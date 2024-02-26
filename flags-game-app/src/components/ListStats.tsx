import { getTop } from "../helpers/getTop";
import { Loader } from "./Loader";
import { ListStatsProps } from "../entities/entities";
import "./ListStats.css";

export const ListStats = ({
  nametop,
  arrayTop,
  isLoadingTop,
  actualMode,
}: ListStatsProps): JSX.Element => {
  if (isLoadingTop) {
    return <Loader></Loader>;
  } else {
    return (
      <article className="list_stats_container_top menu_mode_top">
        <h2>{nametop}</h2>

        <ul className="list_stats_container_top_list menu_mode_top_list">
          {arrayTop.map((top) => {
            const { username, modes } = top;

            const score = getTop(modes, actualMode);

            return (
              <li key={username}>
                {username} with {score} PTS
              </li>
            );
          })}
        </ul>
      </article>
    );
  }
};
