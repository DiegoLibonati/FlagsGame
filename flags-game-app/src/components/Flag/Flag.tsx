import "./Flag.css";

interface FlagProps {
  image: string;
  name: string;
}

export const Flag = ({ image, name }: FlagProps): JSX.Element => {
  return <img src={image} alt={name} className="flag"></img>;
};
