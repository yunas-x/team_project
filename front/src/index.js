import React from 'react';
import ReactDOM from 'react-dom/client';
import "./styles.css"
import ProgramSelectionContainer from "./components/ProgramSelection/ProgramSelectionContainer";
import {ProgramsPage} from "./pages/ProgramsPage/ProgramsPage";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
      <ProgramsPage />
  </React.StrictMode>
);
