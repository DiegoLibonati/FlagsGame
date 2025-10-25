export type AlertType = "alert-auth-error" | "alert-auth-success" | "";

export type Alert = {
  type: AlertType;
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
  total_score: number;
  scores: Record<string, number>;
};

export type UserTop = Pick<User, "_id" | "username"> & {
  score: number;
};

export type UserWithOutPassword = Omit<User, "password">;
