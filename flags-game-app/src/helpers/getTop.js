export const getTop = (modes, modeName) => {
  let finalScore = 0;

  modes.forEach(function (mode) {
    if (mode[modeName]) {
      finalScore = mode[modeName];
    }
  });

  return finalScore;
};
