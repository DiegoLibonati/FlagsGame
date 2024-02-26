import { Flag } from "../entities/entities";

export const getFinishGame = (
  timeleft: string,
  index: number,
  array: Flag[],
  setFinishGame: React.Dispatch<React.SetStateAction<boolean>>
): void => {
  const timeleftSplit = timeleft.split(":");

  const mins = timeleftSplit[1];
  const secs = timeleftSplit[2];

  if (
    (mins === "00" && secs === "00") ||
    (array.length - 1 < index && index && array)
  ) {
    setFinishGame(true);
  }
};
