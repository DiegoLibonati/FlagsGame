import ReactDOM from "react-dom/client";

import App from "./App";

import { FlagsProvider } from "./context/FlagsContext/FlagsProvider";
import { UiProvider } from "./context/UiContext/UiProvider";
import { UsersProvider } from "./context/UsersContext/UsersProvider";
import { ModesProvider } from "./context/ModesContext/ModesProvider";
import { AlertProvider } from "./context/AlertContext/AlertProvider";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <AlertProvider>
    <UiProvider>
      <ModesProvider>
        <UsersProvider>
          <FlagsProvider>
            <App />
          </FlagsProvider>
        </UsersProvider>
      </ModesProvider>
    </UiProvider>
  </AlertProvider>
);
