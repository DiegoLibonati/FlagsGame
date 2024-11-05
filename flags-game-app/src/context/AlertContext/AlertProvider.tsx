import { useContext, useEffect, useState } from "react";

import {
  AlertContext as AlertContextT,
  AlertProviderProps,
  Alert,
} from "../../entities/entities";

import { AlertContext } from "./AlertContext";

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
    const timeout = setTimeout(() => {
      handleClearAlert();
    }, 2000);

    return () => {
      clearTimeout(timeout);
    };
  }, [alert]);

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
