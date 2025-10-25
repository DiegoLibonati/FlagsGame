import {
  AlertContext,
  FlagsContext,
  GameContext,
  ModeContext,
  ModesContext,
  UiContext,
  UsersContext,
} from "@src/entities/contexts";

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

export type UseAlertContext = AlertContext;
export type UseFlagsContext = FlagsContext;
export type UseGameContext = GameContext;
export type UseModeContext = ModeContext;
export type UseModesContext = ModesContext;
export type UseUiContext = UiContext;
export type UseUsersContext = UsersContext;
