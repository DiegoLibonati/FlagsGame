import ReactDOM from "react-dom/client";

import App from "./App";

import { UiProvider } from "./context/UiContext/UiProvider";
import { AlertProvider } from "./context/AlertContext/AlertProvider";

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
