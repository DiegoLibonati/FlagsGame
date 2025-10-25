import { useContext } from "react";

import { UseAlertContext } from "@src/entities/hooks";

import { AlertContext } from "@src/contexts/AlertContext/AlertContext";

export const useAlertContext = (): UseAlertContext => {
  const context = useContext(AlertContext);
  if (!context)
    throw new Error("useAlertContext must be used within AlertProvider");
  return context;
};
