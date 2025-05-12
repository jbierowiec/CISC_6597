// src/Login.jsx
import React from "react";
import { auth, provider, signInWithPopup } from "../firebase";
import "../assets/style.css";

function Login() {
  const handleLogin = async (role) => {
    try {
      const result = await signInWithPopup(auth, provider);
      const email = result.user.email;
      const displayName = result.user.displayName;

      localStorage.setItem("userName", displayName);

      const res = await fetch("https://cisc-6597-backend.onrender.com/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          email: email,
          name: displayName,
          role: role,
        }),
      });

      const data = await res.json();
      window.location.href = data.redirect;
    } catch (error) {
      alert("Login failed");
      console.error(error);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1 className="login-title">Welcome to the App</h1>
        <p className="login-subtext">Please choose your login type</p>
        <div className="login-buttons">
          <button className="login-button" onClick={() => handleLogin("admin")}>
            Login as Admin
          </button>
          <button className="login-button" onClick={() => handleLogin("user")}>
            Login as User
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;
