export type UseCountdown = {
  timerText: string;
  secondsLeft: number;
  endTime: boolean;
  onCountdownReset: () => void;
};

export type UseForm<T> = {
  formState: T;
  onInputChange: React.ChangeEventHandler<HTMLInputElement>;
  onResetForm: () => void;
};
