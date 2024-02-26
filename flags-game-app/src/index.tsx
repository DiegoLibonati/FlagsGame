import React from 'react';
import ReactDOM from 'react-dom/client';
import { FlagsProvider } from './context/FlagsProvider';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <React.StrictMode>
    <FlagsProvider>
      <App />
    </FlagsProvider>
  </React.StrictMode>
);

