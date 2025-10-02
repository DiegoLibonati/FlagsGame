import ReactDOM from "react-dom/client";

import App from "@src/App";

import { UiProvider } from "@src/context/UiContext/UiProvider";
import { AlertProvider } from "@src/context/AlertContext/AlertProvider";

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
