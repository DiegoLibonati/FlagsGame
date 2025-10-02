import { UserTop } from "@src/entities/entities";

export interface FlagProps {
  image: string;
  name: string;
}

export interface FormGuessFlagProps {
  secondsLeft: number;
}

export interface HamburgerProps {
  navbar: boolean;
  manageNavbar: () => void;
}

export interface ListStatsProps {
  nameTop: string;
  arrayTop: UserTop[];
}

export interface AlertProviderProps {
  children: React.ReactNode;
}

export interface FlagsProviderProps {
  children: React.ReactNode;
}

export interface GameProviderProps {
  children: React.ReactNode;
}

export interface ModeProviderProps {
  children: React.ReactNode;
}

export interface ModesProviderProps {
  children: React.ReactNode;
}

export interface UiProviderProps {
  children: React.ReactNode;
}

export interface UsersProviderProps {
  children: React.ReactNode;
}
