import ReactDOM from "react-dom/client";

import App from "@src/App";

import { AlertProvider } from "@src/contexts/AlertContext/AlertContext";
import { UiProvider } from "@src/contexts/UiContext/UiContext";

import "@src/index.css";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <AlertProvider>
    <UiProvider>
      <App />
    </UiProvider>
  </AlertProvider>
);
