// Types

export type FlagsContext = {
  flags: Flag[];
  score: number;
  currentFlagToGuess: Flag;
  completeGuess: boolean;
  handleSetFlags: (flags: Flag[]) => void;
  handleSetScore: (score: number) => void;
  handleClearFlags: () => void;
  handleNextFlagToGuess: () => void;
  handleClearCurrentFlagToGuess: () => void;
  handleSetFlagToGuess: (flag: Flag) => void;
};

export type UiContext = {
  navbar: boolean;
  handleManageNavbar: () => void;
};

export type UsersContext = {
  topUsers: User[];
  handleSetTopUsers: (users: User[]) => void;
  handleClearTopUsers: () => void;
};

export type ModesContext = {
  modes: Mode[];
  actualMode: Mode;
  handleSetActualMode: (mode: Mode) => void;
  handleSetModes: (modes: Mode[]) => void;
  handleClearModes: () => void;
  handleClearActualMode: () => void;
};

export type AlertContext = {
  alert: Alert;
  handleSetAlert: (alert: Alert) => void;
  handleClearAlert: () => void;
};

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
  score: string;
};

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

// Interfaces

export interface FlagsProviderProps {
  children: React.ReactNode;
}

export interface UiProviderProps {
  children: React.ReactNode;
}

export interface UsersProviderProps {
  children: React.ReactNode;
}

export interface ModesProviderProps {
  children: React.ReactNode;
}

export interface AlertProviderProps {
  children: React.ReactNode;
}

export interface HamburgerProps {
  navbar: boolean;
  manageNavbar: () => void;
}

export interface ListStatsProps {
  nametop: string;
  arrayTop: User[];
}

export interface FlagProps {
  image: string;
  name: string;
}
