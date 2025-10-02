import { useContext, useState } from "react";

import { UiContext as UiContextT } from "@src/entities/contexts";
import { UiProviderProps } from "@src/entities/props";

import { UiContext } from "@src/context/UiContext/UiContext";

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
