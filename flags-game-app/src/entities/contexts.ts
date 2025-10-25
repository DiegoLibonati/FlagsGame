import { Alert, Flag, Mode, UserTop } from "@src/entities/app";
import {
  FlagsState,
  ModesState,
  ModeState,
  TopUsersState,
} from "@src/entities/states";

export type FlagsContext = {
  flags: FlagsState;
  handleSetFlags: (flags: Flag[]) => void;
  handleClearFlags: () => void;
  handleStartFetchFlags: () => void;
  handleEndFetchFlags: () => void;
  handleSetErrorFlags: (error: string) => void;
};

export type UiContext = {
  navbar: boolean;
  handleManageNavbar: () => void;
};

export type UsersContext = {
  topUsers: TopUsersState;
  handleSetTopUsers: (users: UserTop[]) => void;
  handleClearTopUsers: () => void;
  handleStartFetchUsers: () => void;
  handleEndFetchUsers: () => void;
  handleSetErrorUsers: (error: string) => void;
};

export type ModesContext = {
  modes: ModesState;
  handleSetModes: (modes: Mode[]) => void;
  handleClearModes: () => void;
  handleStartFetchModes: () => void;
  handleEndFetchModes: () => void;
  handleSetErrorModes: (error: string) => void;
};

export type ModeContext = {
  mode: ModeState;
  handleSetMode: (mode: Mode) => void;
  handleClearMode: () => void;
  handleStartFetchMode: () => void;
  handleEndFetchMode: () => void;
  handleSetErrorMode: (error: string) => void;
};

export type AlertContext = {
  alert: Alert;
  handleSetAlert: (alert: Alert) => void;
  handleClearAlert: () => void;
};

export type GameContext = {
  currentFlagToGuess: Flag | null;
  completeGuess: boolean;
  score: number;
  handleNextFlagToGuess: (flags: Flag[]) => void;
  handleSetScore: (score: number) => void;
  handleSetFlagToGuess: (flag: Flag) => void;
  handleClearCurrentFlagToGuess: () => void;
};
