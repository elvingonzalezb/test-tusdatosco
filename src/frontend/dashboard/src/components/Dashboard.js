import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import Process from './Process';
import Data from './Data';
import Causas from './Causas';
import Register from "./Register";
import Login from "./Login";
import { UserContext } from "../auth/Token";

const Dashboard = () => {

  const [token, setToken] = useContext(UserContext);

  return (
      <div className="App">          
        <div class="card">       
          <div class="card-image">
              {token ? (
                  <Routes>
                      <Route path="/" element={<Navigate to="/process" />} />
                      <Route path="/process" element={<Process />} />
                      <Route path="/data" element={<Data />} />
                      <Route path="/causas" element={<Causas />} />
                  </Routes>
              ) : (
                  <Routes>
                      <Route path="/" element={<Navigate to="/login" />} />
                      <Route path="/register" element={<Register />} />
                      <Route path="/login" element={<Login />} />
                      <Route path="/logout" element={<Navigate to="/login" />} />
                  </Routes>
              )}
          </div> 
        </div>          
      </div> 
  );
}
export default Dashboard;
