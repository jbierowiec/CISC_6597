import React from "react";

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark fixed-top shadow-sm">
      <div className="container">
        <a className="navbar-brand fw-semibold" href="/#home">
          Worksheets.ai
        </a>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#mainNav"
          aria-controls="mainNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>

        <div className="collapse navbar-collapse" id="mainNav">
          <ul className="navbar-nav ms-auto align-items-lg-center gap-lg-2">
            <li className="nav-item">
              <a className="nav-link" href="/#about">
                About
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/#product-demo">
                Plans
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/#contact">
                Contact
              </a>
            </li>

            <li className="nav-item mt-2 mt-lg-0 ms-lg-2">
              <a className="btn btn-primary btn-sm px-3" href="/worksheets">
                Try the Generator
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
