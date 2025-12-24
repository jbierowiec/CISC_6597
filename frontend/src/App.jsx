import React, { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";
import AOS from "aos";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Section from "./components/Section";
import ThreeJSViewer from "./components/ThreeJSViewer";
import WorksheetsPage from "./pages/WorksheetsPage";
import "./assets/style.css";

function useSnapHashScroll() {
  const location = useLocation();

  useEffect(() => {
    // only handle on landing page
    if (location.pathname !== "/") return;

    const hash = location.hash;
    if (!hash) return;

    // Wait a tick for DOM to be ready
    window.setTimeout(() => {
      const sections = Array.from(document.querySelectorAll(".snap-section"));
      const target = document.querySelector(hash);

      if (!target || sections.length === 0) return;

      // Find which snap-section contains the target id
      const idx = sections.findIndex((s) => s === target);
      if (idx >= 0) {
        const y = idx * window.innerHeight;
        window.scrollTo({ top: y, behavior: "smooth" });
      } else {
        // Fallback: try normal scrollIntoView
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }, 80);
  }, [location.pathname, location.hash]);
}

const HomePage = () => {
  const [confirmation, setConfirmation] = useState("");
  const [showNotification, setShowNotification] = useState(false);

  // AOS init once
  useEffect(() => {
    AOS.init({
      duration: 850,
      easing: "ease-out-cubic",
      once: true,
      offset: 80,
    });
  }, []);

  useEffect(() => {
    if (!showNotification) return;

    const timer = setTimeout(() => {
      setShowNotification(false);
    }, 2000); // 2 seconds

    return () => clearTimeout(timer);
  }, [showNotification]);

  // snap-hash scrolling
  useSnapHashScroll();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const form = e.target;

    const payload = {
      name: form.name.value,
      email: form.email.value,
      message: form.message.value,
    };

    try {
      const API_BASE =
        process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

      const response = await fetch(`${API_BASE}/api/contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (response.ok && result.ok) {
        setConfirmation("Message sent successfully!");
        setShowNotification(true);
        form.reset();
      } else {
        setConfirmation(
          result.error || "Something went wrong. Please try again."
        );
        setShowNotification(true);
      }
    } catch (err) {
      setConfirmation("Submission failed. Please check your connection.");
      setShowNotification(true);
      console.error(err);
    }
  };

  return (
    <main className="snap-container">
      {/* HERO */}
      <section id="home" className="snap-section hero-wrap">
        <div className="container">
          <div className="row align-items-center g-4">
            <div className="col-12 col-lg-6" data-aos="fade-right">
              <h1 className="display-5 fw-bold mb-3">
                Generate clean, printable worksheets in seconds.
              </h1>

              <p className="lead text-secondary mb-4">
                Pick a topic, choose how many questions you want, and download a
                polished PDF — with or without an answer key.
              </p>

              <div className="d-flex flex-column flex-sm-row gap-2">
                <a className="btn btn-primary btn-lg" href="/worksheets">
                  Try the Generator
                </a>
                <a className="btn btn-outline-dark btn-lg" href="/#about">
                  Learn More
                </a>
              </div>

              <div className="mt-4 d-flex flex-wrap gap-3 text-secondary small">
                <span>✅ No login required</span>
                <span>✅ Works on mobile</span>
                <span>✅ Instant download</span>
              </div>
            </div>

            <div className="col-12 col-lg-6" data-aos="fade-left">
              <div className="three-card">
                <ThreeJSViewer />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ABOUT */}
      <Section
        id="about"
        title="Built for students and teachers"
        subtitle="A simple workflow: choose a topic → generate → download."
        aos="fade-up"
      >
        <div className="row g-3 justify-content-center">
          <div className="col-12 col-md-6 col-lg-4">
            <div className="feature-card h-100">
              <h5 className="mb-2">Fast generation</h5>
              <p className="text-secondary mb-0">
                Create focused practice sets instantly — perfect for homework,
                quizzes, or tutoring.
              </p>
            </div>
          </div>

          <div className="col-12 col-md-6 col-lg-4">
            <div className="feature-card h-100">
              <h5 className="mb-2">Answer keys</h5>
              <p className="text-secondary mb-0">
                Export with an optional answer key to speed up grading and
                feedback.
              </p>
            </div>
          </div>

          <div className="col-12 col-md-6 col-lg-4">
            <div className="feature-card h-100">
              <h5 className="mb-2">Clean PDFs</h5>
              <p className="text-secondary mb-0">
                Worksheets are formatted to print well and look professional.
              </p>
            </div>
          </div>
        </div>
      </Section>

      {/* PLANS */}
      {/*
      <Section
        id="product-demo"
        title="Simple plans"
        subtitle="Start free with the demo — upgrade later."
        aos="fade-up"
      >
        <div className="row g-3">
          <div className="col-12 col-md-4">
            <div className="pricing-card h-100">
              <h5 className="mb-1">Basic</h5>
              <div className="price">
                $5<span>/mo</span>
              </div>
              <ul className="mt-3">
                <li>Unlimited worksheet generation</li>
                <li>Answer keys</li>
                <li>PDF export</li>
              </ul>
              <a className="btn btn-outline-dark w-100 mt-3" href="/worksheets">
                Try Demo
              </a>
            </div>
          </div>

          <div className="col-12 col-md-4">
            <div className="pricing-card pricing-highlight h-100">
              <h5 className="mb-1">Premium</h5>
              <div className="price">
                $10<span>/mo</span>
              </div>
              <ul className="mt-3">
                <li>All Basic features</li>
                <li>More advanced sets</li>
                <li>Classroom tools</li>
              </ul>
              <a className="btn btn-primary w-100 mt-3" href="/worksheets">
                Try Demo
              </a>
            </div>
          </div>

          <div className="col-12 col-md-4">
            <div className="pricing-card h-100">
              <h5 className="mb-1">Enterprise</h5>
              <div className="price">
                $50<span>/mo</span>
              </div>
              <ul className="mt-3">
                <li>Admin dashboard</li>
                <li>Custom branding</li>
                <li>Priority support</li>
              </ul>
              <a className="btn btn-outline-dark w-100 mt-3" href="/#contact">
                Contact
              </a>
            </div>
          </div>
        </div>
      </Section>
      */}

      {/* CONTACT */}
      <Section
        id="contact"
        title="Contact"
        subtitle="Questions, partnerships, or feedback — send a note."
        aos="fade-up"
      >
        <div className="row justify-content-center">
          <div className="col-12 col-lg-7">
            <div className="contact-card">
              <form onSubmit={handleSubmit} className="row g-3">
                <div className="col-12 col-md-6">
                  <label className="form-label">Name</label>
                  <input
                    className="form-control"
                    type="text"
                    name="name"
                    required
                  />
                </div>

                <div className="col-12 col-md-6">
                  <label className="form-label">Email</label>
                  <input
                    className="form-control"
                    type="email"
                    name="email"
                    required
                  />
                </div>

                <div className="col-12">
                  <label className="form-label">Message</label>
                  <textarea
                    className="form-control"
                    name="message"
                    rows="5"
                    required
                  />
                </div>

                <div className="col-12 d-flex flex-column flex-sm-row gap-2">
                  <button className="btn btn-primary btn-lg" type="submit">
                    Send
                  </button>
                  <a className="btn btn-outline-dark btn-lg" href="/worksheets">
                    Try the Generator
                  </a>
                </div>
              </form>

              {showNotification && (
                <div
                  className={`alert ${
                    confirmation.includes("successfully")
                      ? "alert-success"
                      : "alert-danger"
                  } mt-3`}
                  role="alert"
                >
                  {confirmation}
                </div>
              )}
            </div>
          </div>
        </div>
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
        <Route path="/worksheets" element={<WorksheetsPage />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;
