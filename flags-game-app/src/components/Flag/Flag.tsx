import { FlagProps } from "@src/entities/props";

import "@src/components/Flag/Flag.css";

export const Flag = ({ image, name }: FlagProps): JSX.Element => {
  return <img src={image} alt={name} className="flag"></img>;
};
