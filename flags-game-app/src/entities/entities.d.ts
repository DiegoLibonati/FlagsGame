// Types

export type FlagsContextT = {
  navbar: boolean;
  btnStart: boolean;
  score: number;
  flagsArr: Flag[];
  topArr: User[];
  actualMode: Mode | null;
  flagsLoading: boolean;
  modeLoading: boolean;
  topLoading: boolean;
  manageNavbar: () => void;
  setBtnStart: React.Dispatch<React.SetStateAction<boolean>>;
  setScore: React.Dispatch<React.SetStateAction<number>>;
  setFlagsArr: React.Dispatch<React.SetStateAction<Flag[]>>;
  setFlagsLoading: React.Dispatch<React.SetStateAction<boolean>>;
  setActualMode: React.Dispatch<React.SetStateAction<Mode | null>>;
  setModeLoading: React.Dispatch<React.SetStateAction<boolean>>;
  setTopArr: React.Dispatch<React.SetStateAction<User[]>>;
  setTopLoading: React.Dispatch<React.SetStateAction<boolean>>;
};

export type Flag = {
  _id?: {
    $oid: string;
  };
  image: string;
  name: string;
};

export type Mode = {
  name: string;
  description: string;
  timeleft: number;
};

export type User = {
  username: string;
  password: string;
  modes: Mode[];
};

export type UseCountdown = {
  timer: string;
  onClickReset: () => void;
};

export type UseForm<T> = {
  formState: T;
  onInputChange: React.ChangeEventHandler<HTMLInputElement>;
  onResetForm: () => void;
};

export type UseLogic = {
  currentItem: Flag | null;
  onSubmit: React.FormEventHandler<HTMLFormElement>;
  setFinishGame: React.Dispatch<React.SetStateAction<boolean>>;
};

// Interfaces

export interface FlagsProviderProps {
  children: React.ReactNode;
}

export interface HamburgerProps {
  navbar: boolean;
  manageNavbar: () => void;
}

export interface ListStatsProps {
  nametop: string;
  arrayTop: User[];
  isLoadingTop: boolean;
  actualMode: string;
}

export interface FlagProps {
  image: string;
  name: string;
}