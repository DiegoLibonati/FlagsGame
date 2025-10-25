import { BrowserRouter } from "react-router-dom";

import { AppRouter } from "@src/router/AppRouter";

function App(): JSX.Element {
  return (
    <BrowserRouter
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <AppRouter></AppRouter>
    </BrowserRouter>
  );
}

export default App;
