import { Flag, Mode, User, UserTop } from "@src/entities/app";

export type AddUserResponse = {
  message: string;
  code: string;
  data: User;
};

export type AddFlagResponse = {
  message: string;
  code: string;
  data: Flag;
};

export type AddModeResponse = {
  message: string;
  code: string;
  data: Mode;
};

export type PatchUserResponse = {
  message: string;
  code: string;
  data: User;
};

export type GetTopGeneralResponse = {
  message: string;
  code: string;
  data: UserTop[];
};

export type GetModesResponse = {
  message: string;
  code: string;
  data: Mode[];
};

export type GetTopModeResponse = {
  message: string;
  code: string;
  data: UserTop[];
};

export type GetModeResponse = {
  message: string;
  code: string;
  data: Mode;
};

export type GetRandomFlagsResponse = {
  message: string;
  code: string;
  data: Flag[];
};

export type GetFlagsResponse = {
  message: string;
  code: string;
  data: Flag[];
};
