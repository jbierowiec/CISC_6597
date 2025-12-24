import React, { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

const API_BASE = process.env.REACT_APP_API_BASE_URL || "";

export default function WorksheetsPage() {
  const navigate = useNavigate();

  const goTo = (hash) => {
    navigate(`/${hash}`);
  };

  const [topic, setTopic] = useState("");
  const [subTopic, setSubTopic] = useState("");
  const [subSubTopic, setSubSubTopic] = useState("");
  const [questionCount, setQuestionCount] = useState(10);

  const [toast, setToast] = useState({ show: false, ok: true, msg: "" });
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const subTopics = useMemo(
    () => ({
      Mathematics: ["Algebra 1", "Calculus 1"],
    }),
    []
  );

  const subSubTopics = useMemo(
    () => ({
      "Algebra 1": [
        "Basic Addition",
        "Basic Subtraction",
        "Basic Multiplication",
        "Basic Division",
        "Negative Addition",
        "Negative Subtraction",
        "Negative Multiplication",
        "Negative Division",
        "Fraction Addition",
        "Fraction Subtraction",
        "Fraction Multiplication",
        "Fraction Division",
        "Distributive Property",
        "Quadratic Formula",
      ],
      "Calculus 1": ["Definite Integrals", "Indefinite Integrals", "Derivatives"],
    }),
    []
  );

  const showToast = (ok, msg) => {
    setToast({ show: true, ok, msg });
    setTimeout(() => setToast((t) => ({ ...t, show: false })), 2600);
  };

  const generateWorksheet = async (includeAnswerKey) => {
    if (!topic || !subTopic || !subSubTopic) {
      showToast(false, "Please select a topic, sub-topic, and sub-sub-topic.");
      return;
    }

    const formatted = subSubTopic.toLowerCase().replace(/\s+/g, "-");
    const url = `${API_BASE}/generate-${formatted}`;

    setLoading(true);
    setProgress(0);

    const interval = setInterval(() => {
      setProgress((p) => (p < 90 ? p + 5 : p));
    }, 350);

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          includeAnswerKey,
          questionCount: Number(questionCount),
        }),
      });

      const data = await res.json();
      clearInterval(interval);

      if (data?.downloadUrl) {
        setProgress(100);
        setTimeout(() => {
          setLoading(false);
          showToast(
            true,
            data.message || "Worksheet generated! Download starting…"
          );

          const downloadLink = data.downloadUrl.startsWith("http")
            ? data.downloadUrl
            : `${API_BASE}${data.downloadUrl}`;

          window.location.href = downloadLink;
        }, 600);
      } else {
        setLoading(false);
        showToast(false, "Failed to generate worksheet. Try again.");
      }
    } catch (e) {
      clearInterval(interval);
      setLoading(false);
      showToast(false, "Server error. Please try again.");
      console.error(e);
    }
  };

  return (
    <div className="bg-light min-vh-100">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm sticky-top">
        <div className="container">
          <button
            className="navbar-brand btn btn-link p-0 m-0 text-decoration-none text-white fw-semibold"
            onClick={() => goTo("#home")}
            type="button"
          >
            Worksheets.ai
          </button>

          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#worksheetsNav"
            aria-controls="worksheetsNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon" />
          </button>

          <div className="collapse navbar-collapse" id="worksheetsNav">
            <ul className="navbar-nav ms-auto align-items-lg-center gap-lg-2 mt-3 mt-lg-0">
              <li className="nav-item">
                <button
                  className="nav-link btn btn-link"
                  onClick={() => goTo("#home")}
                  type="button"
                >
                  Home
                </button>
              </li>
              <li className="nav-item">
                <button
                  className="nav-link btn btn-link"
                  onClick={() => goTo("#about")}
                  type="button"
                >
                  About
                </button>
              </li>
              <li className="nav-item">
                <button
                  className="nav-link btn btn-link"
                  onClick={() => goTo("#product-demo")}
                  type="button"
                >
                  Plans
                </button>
              </li>
              <li className="nav-item">
                <button
                  className="nav-link btn btn-link"
                  onClick={() => goTo("#contact")}
                  type="button"
                >
                  Contact
                </button>
              </li>
              <li className="nav-item ms-lg-2">
                <button
                  className="btn btn-primary btn-sm px-3"
                  onClick={() => goTo("#home")}
                  type="button"
                >
                  Back to Landing
                </button>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <main className="py-5">
        <div className="container">
          <div className="row justify-content-center">
            <div className="col-12 col-xl-8">
              <div className="card shadow-sm border-0 rounded-4">
                <div className="card-body p-4 p-md-5">
                  <h2 className="h4 fw-bold mb-3">Create a worksheet</h2>
                  <p className="text-secondary mb-4">
                    Select your options below. Your PDF will download
                    automatically.
                  </p>

                  <div className="row g-3">
                    <div className="col-12 col-md-6">
                      <label className="form-label">Topic</label>
                      <select
                        className="form-select"
                        value={topic}
                        onChange={(e) => {
                          setTopic(e.target.value);
                          setSubTopic("");
                          setSubSubTopic("");
                        }}
                      >
                        <option value="">Select…</option>
                        <option value="Mathematics">Mathematics</option>
                      </select>
                    </div>

                    <div className="col-12 col-md-6">
                      <label className="form-label">Sub-topic</label>
                      <select
                        className="form-select"
                        value={subTopic}
                        onChange={(e) => {
                          setSubTopic(e.target.value);
                          setSubSubTopic("");
                        }}
                        disabled={!topic}
                      >
                        <option value="">Select…</option>
                        {(subTopics[topic] || []).map((s) => (
                          <option key={s} value={s}>
                            {s}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="col-12 col-md-8">
                      <label className="form-label">Sub-sub-topic</label>
                      <select
                        className="form-select"
                        value={subSubTopic}
                        onChange={(e) => setSubSubTopic(e.target.value)}
                        disabled={!subTopic}
                      >
                        <option value="">Select…</option>
                        {(subSubTopics[subTopic] || []).map((s) => (
                          <option key={s} value={s}>
                            {s}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="col-12 col-md-4">
                      <label className="form-label">Question count</label>
                      <input
                        type="number"
                        className="form-control"
                        min="1"
                        max="100"
                        value={questionCount}
                        onChange={(e) => setQuestionCount(e.target.value)}
                      />
                    </div>

                    <div className="col-12 d-grid d-sm-flex gap-2 mt-2">
                      <button
                        className="btn btn-primary btn-lg"
                        type="button"
                        onClick={() => generateWorksheet(false)}
                        disabled={loading}
                      >
                        Generate Worksheet
                      </button>
                      <button
                        className="btn btn-outline-dark btn-lg"
                        type="button"
                        onClick={() => generateWorksheet(true)}
                        disabled={loading}
                      >
                        + Answer Key
                      </button>
                    </div>
                  </div>

                  {loading && (
                    <div className="mt-4">
                      <div className="d-flex align-items-center gap-3">
                        <div
                          className="spinner-border"
                          role="status"
                          aria-label="Loading"
                        />
                        <div className="flex-grow-1">
                          <div className="fw-semibold">
                            Generating... {progress}%
                          </div>
                          <div className="progress mt-2" style={{ height: 10 }}>
                            <div
                              className="progress-bar"
                              style={{ width: `${progress}%` }}
                            />
                          </div>
                        </div>
                      </div>
                      <div className="text-secondary small mt-2">
                        Please keep this tab open while the PDF is generating.
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {toast.show && (
                <div
                  className={`alert mt-3 ${
                    toast.ok ? "alert-success" : "alert-danger"
                  }`}
                  role="alert"
                >
                  {toast.msg}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
