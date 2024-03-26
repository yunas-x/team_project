import React from 'react';
import ReactDOM from 'react-dom/client';
import "./styles.css"
import {ComparisonController} from "./controllers/comparisonController";
import {App} from "./App";

export const comparisonController = new ComparisonController()

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
      <App/>
  </React.StrictMode>
);
