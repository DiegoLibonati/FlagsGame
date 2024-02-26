import { useState, useRef } from "react";
import { UseCountdown } from "../entities/entities";

export const useCountdown = (timeleft: number, mode: string): UseCountdown => {
  const [timer, setTimer] = useState<string>("00:00:10");
  const Ref = useRef<NodeJS.Timeout | null>(null);

  const getTimeRemaining = (e: Date): Record<string, number> => {
    const total = Date.parse(String(e)) - Date.parse(String(new Date()));
    const seconds = Math.floor((total / 1000) % 60);
    const minutes = Math.floor((total / 1000 / 60) % 60);
    const hours = Math.floor((total / 1000 / 60 / 60) % 24);
    return {
      total,
      hours,
      minutes,
      seconds,
    };
  };

  const startTimer = (e: Date): void => {
    let { total, hours, minutes, seconds } = getTimeRemaining(e);
    if (total >= 0) {
      setTimer(
        (hours > 9 ? hours : "0" + hours) +
          ":" +
          (minutes > 9 ? minutes : "0" + minutes) +
          ":" +
          (seconds > 9 ? seconds : "0" + seconds)
      );
    }
  };

  const clearTimer = (e: Date): void => {
    if (mode === "hardcore") {
      setTimer(`00:00:10`);
    } else if (timeleft < 10) {
      setTimer(`00:0${timeleft}:00`);
    } else {
      setTimer(`00:${timeleft}:00`);
    }

    if (Ref.current) clearInterval(Ref.current);
    const id = setInterval(() => {
      startTimer(e);
    }, 1000);
    Ref.current = id;
  };

  const getDeadTime = (): Date => {
    let deadline = new Date();

    if (mode === "hardcore") {
      deadline.setSeconds(deadline.getSeconds() + 0.18 * 60);
    } else {
      deadline.setSeconds(deadline.getSeconds() + timeleft * 60);
    }
    return deadline;
  };

  const onClickReset = (): void => {
    clearTimer(getDeadTime());
  };

  return {
    timer,
    onClickReset,
  };
};
