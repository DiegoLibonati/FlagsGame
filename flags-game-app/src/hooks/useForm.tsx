import { useState } from "react";

type UseForm<T> = {
  formState: T;
  onInputChange: React.ChangeEventHandler<HTMLInputElement>;
  onResetForm: () => void;
};

export const useForm = <T,>(initialForm: T): UseForm<T> => {
  const [formState, setformState] = useState(initialForm);

  const onInputChange: React.ChangeEventHandler<HTMLInputElement> = (e) => {
    const target = e.target as HTMLInputElement;
    const { name, value } = target;

    setformState({
      ...formState,
      [name]: value,
    });
  };

  const onResetForm = (): void => {
    setformState(initialForm);
  };

  return {
    formState,
    onInputChange,
    onResetForm,
  };
};
