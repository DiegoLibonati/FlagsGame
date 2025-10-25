import { createContext, useEffect, useState } from "react";

import { Alert } from "@src/entities/app";
import { AlertContext as AlertContextT } from "@src/entities/contexts";
import { AlertProviderProps } from "@src/entities/props";

export const AlertContext = createContext<AlertContextT | null>(null);

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
