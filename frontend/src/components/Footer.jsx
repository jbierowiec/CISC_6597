import React from "react";
import "../assets/style.css";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="modern-footer">
      <div className="footer-container">
        <div>
          <h3>Worksheets.ai</h3>
          <p>Your dynamic STEM worksheet generator.</p>
        </div>
        <div>
          <h4>Links</h4>
          <a href="#home">Home</a>
          <a href="#about">About</a>
          <a href="#product-demo">Product Demo</a>
          <a href="#contact">Contact</a>
        </div>
        <div>
          <h4>Contact</h4>
          <p>Email: support@worksheets.ai</p>
          <p>NYC, USA</p>
        </div>
      </div>
      <p style={{ marginTop: "20px" }}>
        &copy; {currentYear} Worksheets.ai. All rights reserved.
      </p>
    </footer>
  );
};

export default Footer;
