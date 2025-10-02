import { useContext, useEffect, useState } from "react";

import { Alert } from "@src/entities/entities";
import { AlertContext as AlertContextT } from "@src/entities/contexts";
import { AlertProviderProps } from "@src/entities/props";

import { AlertContext } from "@src/context/AlertContext/AlertContext";

export const AlertProvider = ({ children }: AlertProviderProps) => {
  // Top
  const [alert, setAlert] = useState<Alert>({
    message: "",
    type: "",
  });

  const handleSetAlert = (alert: Alert) => {
    setAlert(alert);
  };

  const handleClearAlert = () => {
    setAlert({
      type: "",
      message: "",
    });
  };

  useEffect(() => {
    if (!alert.type) return;

    const timeout = setTimeout(() => {
      handleClearAlert();
    }, 2000);

    return () => {
      clearTimeout(timeout);
    };
  }, [alert.type]);

  return (
    <AlertContext.Provider
      value={{
        alert: alert,
        handleSetAlert: handleSetAlert,
        handleClearAlert: handleClearAlert,
      }}
    >
      {children}
    </AlertContext.Provider>
  );
};

export const useAlertContext = (): AlertContextT => {
  return useContext(AlertContext)!;
};
