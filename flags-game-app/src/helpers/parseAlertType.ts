import { AlertType } from "../entities/entities";

export const parseAlertType = (type: AlertType): string => {
  const alertTypes: Record<AlertType, string> = {
    "alert-auth-error": "error",
    "alert-auth-success": "success",
    "": "unknown",
  };

  return alertTypes[type];
};
