import { Mode } from "../entities/entities";

export const getTop = (modes: Mode[], modeName: string): number => {
  let finalScore = 0;

  modes.forEach(function (mode) {
    if (mode[modeName as keyof typeof mode]) {
      finalScore = Number(mode[modeName as keyof typeof mode]);
    }
  });

  return finalScore;
};
