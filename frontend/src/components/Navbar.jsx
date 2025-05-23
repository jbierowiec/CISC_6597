// src/components/Navbar.jsx
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [userName, setUserName] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  const toggleMenu = () => setMenuOpen(!menuOpen);

  useEffect(() => {
    const name = localStorage.getItem("userName");
    setUserName(name); // even if null, it resets
  }, [location]);

  return (
    <nav>
      <div className="hamburger" onClick={toggleMenu}>
        <span></span>
        <span></span>
        <span></span>
      </div>

      <div className={`nav-left ${menuOpen ? "show" : ""}`}>
        <a href="#home">Home</a>
        <a href="#about">About</a>
        <a href="#product-demo">Product Demo</a>
        <a href="#contact">Contact</a>
      </div>

      <div className={`nav-right ${menuOpen ? "show" : ""}`}>
        {userName ? (
          <div className="user-dropdown">
            <button
              className="user-button"
              onClick={() => setMenuOpen(!menuOpen)}
            >
              {userName}
            </button>
            {menuOpen && (
              <div className="dropdown-menu">
                <a
                  href={`http://localhost:5000/welcome?name=${encodeURIComponent(
                    userName
                  )}`}
                >
                  Profile
                </a>
                <button
                  onClick={() => {
                    localStorage.removeItem("userName");
                    window.location.href = "/";
                  }}
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        ) : (
          <button onClick={() => navigate("/login")}>Login</button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
