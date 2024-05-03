import React from 'react';
import { createRoot } from 'react-dom';
import App from './App.js';
import "bulma/css/bulma.min.css"

import { UserProvider } from './auth/Token.js';

createRoot(document.getElementById('root')).render(
  <UserProvider>
    <App />
  </UserProvider>
);
