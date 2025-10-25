import { UserTop } from "@src/entities/app";

interface DefaultProps {
  children?: React.ReactNode;
  className?: string;
}

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

export interface AlertProviderProps extends DefaultProps {}

export interface FlagsProviderProps extends DefaultProps {}

export interface GameProviderProps extends DefaultProps {}

export interface ModeProviderProps extends DefaultProps {}

export interface ModesProviderProps extends DefaultProps {}

export interface UiProviderProps extends DefaultProps {}

export interface UsersProviderProps extends DefaultProps {}
