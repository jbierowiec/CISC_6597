import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Login from "./components/Login";
import Logout from "./components/Logout";
import Section from "./components/Section";
import ThreeJSViewer from "./components/ThreeJSViewer";

import "./assets/style.css";

const HomePage = () => {
  const [confirmation, setConfirmation] = useState("");
  const [showNotification, setShowNotification] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    try {
      const response = await fetch(
        "https://script.google.com/macros/s/AKfycbwyqr2Hks5-TOOrjy-fqTGflKLfHh8QTvi1PVPFbxcXVtBz7y5TxXL_AwCMaGU-Ibzp/exec",
        {
          method: "POST",
          body: formData,
        }
      );

      const result = await response.json();
      if (result.result === "success") {
        setConfirmation("✅ Your message was sent successfully!");
        setShowNotification(true);
        form.reset();
      } else {
        setConfirmation("⚠️ Something went wrong. Please try again.");
        setShowNotification(true);
      }
    } catch (err) {
      setConfirmation("⚠️ Submission failed. Please check your connection.");
      setShowNotification(true);
      console.error(err);
    }
  };

  return (
    <main>
      {/* Hero Section */}
      <section id="home" className="hero-section">
        <div className="hero-content">
          <h1>Welcome to Worksheets.ai!</h1>
          <p>
            Explore dynamically generated worksheets covering all subjects of
            STEM!
          </p>
        </div>
        <ThreeJSViewer />
      </section>

      <hr />

      {/* About Section */}
      <Section id="about" title="About Worksheets.ai">
        <div className="about-box">
          <p>
            Worksheets.ai is a dynamic STEM learning platform that blends the
            power of AI with the needs of modern education. Whether you're a
            student aiming to sharpen your skills or a teacher looking to create
            engaging material instantly, we have you covered.
          </p>
          <ul>
            <li>✅ AI-powered worksheet generation in seconds</li>
            <li>✅ Built-in answer keys for quick feedback</li>
            <li>✅ Export to clean, printable PDFs</li>
            <li>✅ Powerful analytics and usage tracking for instructors</li>
            <li>✅ Tailored problem sets across math, science, and more</li>
          </ul>
        </div>
      </Section>

      <hr />

      {/* Pricing Section */}
      <Section id="product-demo" title="Pricing Plans">
        <div className="pricing-cards-rectangular">
          <div className="card basic">
            <h3>$5/month - Basic</h3>
            <ul>
              <li>Unlimited worksheet generation</li>
              <li>Answer keys included</li>
              <li>PDF export</li>
            </ul>
          </div>
          <div className="card premium">
            <h3>$10/month - Premium</h3>
            <ul>
              <li>All Basic features</li>
              <li>AI-enhanced problem sets</li>
              <li>Classroom tools</li>
              <li>Worksheet analytics</li>
            </ul>
          </div>
          <div className="card enterprise">
            <h3>$50/month - Enterprise</h3>
            <ul>
              <li>All Premium features</li>
              <li>Custom branding</li>
              <li>Admin dashboard</li>
              <li>Priority support</li>
            </ul>
          </div>
        </div>
      </Section>

      <hr />

      {/* Contact Section */}
      <Section id="contact" title="Contact Us">
        <p>Reach out to us with feedback or collaboration opportunities!</p>
        <form className="contact-form" onSubmit={handleSubmit}>
          <input type="text" name="name" placeholder="Your Name" required />
          <input type="email" name="email" placeholder="Your Email" required />
          <textarea name="message" placeholder="Your Message" rows="5" required />
          <button type="submit">Send Message</button>
        </form>

        {showNotification && (
          <div className="popup-notification">
            {confirmation}
            <button onClick={() => setShowNotification(false)} className="close-btn">
              &times;
            </button>
          </div>
        )}
      </Section>
    </main>
  );
};

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;
