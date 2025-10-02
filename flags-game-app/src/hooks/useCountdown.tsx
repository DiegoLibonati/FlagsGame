import { useState, useEffect, useRef } from "react";

import { UseCountdown } from "@src/entities/hooks";

import { parseZero } from "@src/helpers/parseZero";

export const useCountdown = (timeleft: number): UseCountdown => {
  const [secondsLeft, setSecondsLeft] = useState<number>(-1);
  const [timerText, setTimerText] = useState<string>("00:00:00");
  const [endTime, setEndTime] = useState<boolean>(false);

  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const restASecond = (seconds: number) => {
    if (endTime) return;

    timerRef.current = setTimeout(() => {
      const newSecondsLeft = secondsLeft - 1;
      setSecondsLeft(newSecondsLeft);
      secondsToTimer(newSecondsLeft);

      if (!newSecondsLeft) setEndTime(true);
    }, 1000);

    return () => clearTimeout(timerRef.current!);
  };

  const secondsToTimer = (seconds: number) => {
    const hours = parseZero(Math.floor(seconds / 3600));
    const minutes = parseZero(Math.floor((seconds % 3600) / 60));
    const secs = parseZero(seconds % 60);

    setSecondsLeft(seconds);
    setTimerText(`${hours}:${minutes}:${secs}`);
  };

  const onCountdownReset = () => {
    setTimerText("");
    clearTimeout(timerRef.current!);
    timerRef.current = null;
  };

  useEffect(() => {
    if (!timeleft) return;

    secondsToTimer(timeleft);
  }, [timeleft]);

  useEffect(() => {
    if (secondsLeft === -1) return;

    restASecond(secondsLeft);
  }, [secondsLeft]);

  return {
    timerText: timerText,
    secondsLeft: secondsLeft,
    endTime: endTime,
    onCountdownReset: onCountdownReset,
  };
};
