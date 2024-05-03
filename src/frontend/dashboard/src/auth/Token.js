import React, { createContext, useState } from "react";

export const UserContext = createContext();

export const UserProvider = (props) => {
  const [token, setTokenState] = useState(localStorage.getItem("auth_token"));

  const setToken = (newToken) => {
    if (newToken === null) {
      localStorage.removeItem("auth_token");
    } else {
      localStorage.setItem("auth_token", newToken); 
    }
    setTokenState(newToken);
  };

  return (
    <UserContext.Provider value={[token, setToken]}>
      {props.children}
    </UserContext.Provider>
  );
};
