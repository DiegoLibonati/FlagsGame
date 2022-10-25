import React from "react";
import { getTop } from "../helpers/getTop";
import "./ListStats.css";
import { Loader } from "./Loader";

export const ListStats = ({ nametop, arrayTop, isLoadingTop, actualMode }) => {
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
