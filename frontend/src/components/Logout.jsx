// src/components/Logout.jsx
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem("userName"); // ✅ clear user
    navigate("/"); // go home
  }, [navigate]);

  return null;
};

export default Logout;
