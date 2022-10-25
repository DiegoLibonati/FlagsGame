export const getFinishGame = (timeleft, index, array, setFinishGame) => {
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
