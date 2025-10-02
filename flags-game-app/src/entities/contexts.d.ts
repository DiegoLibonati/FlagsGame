import { Alert, Flag, Mode, UserTop } from "@src/entities/entities";
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
  refreshFlags: () => void;
};

export type UiContext = {
  navbar: boolean;
  handleManageNavbar: () => void;
};

export type UsersContext = {
  topUsers: TopUsersState;
  handleSetTopUsers: (users: UserTop[]) => void;
  handleClearTopUsers: () => void;
  refreshGeneralTopUsers: () => void;
  refreshModeTopUsers: () => void;
};

export type ModesContext = {
  modes: ModesState;
  handleSetModes: (modes: Mode[]) => void;
  handleClearModes: () => void;
  refreshModes: () => void;
};

export type ModeContext = {
  mode: ModeState;
  handleSetMode: (mode: Mode) => void;
  handleClearMode: () => void;
  refreshMode: () => void;
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
  handleNextFlagToGuess: () => void;
  handleSetScore: (score: number) => void;
};
