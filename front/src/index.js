import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import "./styles.css"
import ProgramSelectionPage from "./pages/ProgramSelection/ProgramSelectionPage";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
      <ProgramSelectionPage />
  </React.StrictMode>
);
