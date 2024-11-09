// Types

// ** CONTEXTS **
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
  handleSetTopUsers: (users: UserWithOutPassword[]) => void;
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

// ** CONTEXTS STATES **

export type GeneralState = {
  loading: boolean;
  error: string | null;
};

export type TopUsersState = {
  users: UserWithOutPassword[];
} & GeneralState;

export type ModesState = {
  modes: Mode[];
} & GeneralState;

export type ModeState = {
  mode: Mode | null;
} & GeneralState;

export type FlagsState = {
  flags: Flag[];
} & GeneralState;

// ** GENERAL **

export type Alert = {
  type: string;
  message: string;
};

export type Flag = {
  _id: string;
  image: string;
  name: string;
};

export type Mode = {
  _id: string;
  name: string;
  description: string;
  timeleft: number;
  multiplier: number;
};

export type User = {
  _id: string;
  username: string;
  password: string;
  score: number;
};

export type UserWithOutPassword = Omit<User, "password">;
