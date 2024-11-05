import { useContext, useState } from "react";

import {
  UiContext as UiContextT,
  UiProviderProps,
} from "../../entities/entities";

import { UiContext } from "./UiContext";

export const UiProvider = ({ children }: UiProviderProps) => {
  // NavBar
  const [navbar, setNavbar] = useState<boolean>(false);

  const handleManageNavbar = (): void => {
    setNavbar(!navbar);
  };

  return (
    <UiContext.Provider
      value={{
        navbar: navbar,
        handleManageNavbar: handleManageNavbar,
      }}
    >
      {children}
    </UiContext.Provider>
  );
};

export const useUiContext = (): UiContextT => {
  return useContext(UiContext)!;
};
