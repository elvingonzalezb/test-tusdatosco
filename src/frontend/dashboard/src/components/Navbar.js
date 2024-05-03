import React, { useState, useContext } from 'react';
import { Link } from 'react-router-dom';
import { UserContext } from '../auth/Token';

function Navbar() {
  const [isActive, setIsActive] = useState(false);

  const [token, setToken] = useContext(UserContext);

  const handleLogout = () => {    
    setToken(null);
  };

  const toggleNavbar = () => {
    setIsActive(!isActive);
  };

  return (
    <div>
      <nav className="navbar" role="navigation" aria-label="main navigation">
        <div className="navbar-brand">
          <Link className="navbar-item" to="/"></Link>
            <a
                role="button"
                className={`navbar-burger ${isActive ? 'is-active' : ''}`}
                aria-label="menu"
                aria-expanded={isActive ? 'true' : 'false'}
                onClick={toggleNavbar}
            >
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
            </a>
        </div>

        <div
          id="navbarBasicExample"
          className={`navbar-menu ${isActive ? 'is-active' : ''}`}
        >
          <div className="navbar-start">
            <Link className="navbar-item">
              Home
            </Link>          
            
            {token ? (
                <>
                <Link className="navbar-item" to="/causas">
                    Causas
                </Link>

                <Link className="navbar-item" to="/process">
                    Process
                </Link>
  
                <Link className="navbar-item" to="/data">
                    Data
                </Link>                
    
                <button className="navbar-item" onClick={handleLogout}>
                  Logout
                </button>
                </>
              ) : (
                <>
                  <Link className="navbar-item" to="/register">
                    Register
                  </Link>
                  <Link className="navbar-item" to="/login">
                    Login
                  </Link>
                </>
              )}
          </div>
        </div>
      </nav>

    
    </div>
  );
}

export default Navbar;
