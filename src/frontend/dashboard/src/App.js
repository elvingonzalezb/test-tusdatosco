import React, { useContext, useEffect, useState } from "react";
import { BrowserRouter as Router } from 'react-router-dom';
import Header from "./components/Header";
import Dashboard from "./components/Dashboard";
import Navbar from "./components/Navbar";
import { UserContext } from "./auth/Token";

const App = () => {
  const [message, setMessage] = useState("Header");
  const [token] = useContext(UserContext);

  const getMessage = async () => {
    if (token) {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      };
      const response = await fetch("/auth", requestOptions);
      const data = await response.json();

      if (!response.ok) {
        console.log("something wrong");
      } else {
        setMessage(data.message);
      }
    }
  };

  useEffect(() => {
    getMessage();
  }, [token]); // Asegurar que getMessage se ejecute cada vez que el token cambie

  return (  
    <Router>
        <>
          <Navbar />
            <Header title={message} />
            <div className="columns">
              <div className="column"></div>
                <div className="column m-5 is-two-thirds">
                  <Dashboard />
                </div>
              <div className="column"></div>
            </div>
        </>
    </Router>
  );
};

export default App;
