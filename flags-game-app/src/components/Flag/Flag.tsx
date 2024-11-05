import { FlagProps } from "../../entities/entities";

import "./Flag.css";

export const Flag = ({ image, name }: FlagProps): JSX.Element => {
  return <img src={image} alt={name}></img>;
};
