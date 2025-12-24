import React from "react";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-dark text-light pt-5 pb-4">
      <div className="container">
        <div className="row gy-4">
          <div className="col-12 col-md-6 col-lg-4">
            <h5 className="fw-semibold">Worksheets AI</h5>
            <p className="text-secondary mb-0">
              A clean, fast, AI-powered worksheet generator for STEM practice
              and teaching.
            </p>
          </div>

          <div className="col-6 col-lg-4">
            <h6 className="text-uppercase text-secondary small">Links</h6>
            <ul className="list-unstyled mb-0">
              <li>
                <a className="footer-link" href="#home">
                  Home
                </a>
              </li>
              <li>
                <a className="footer-link" href="#about">
                  About
                </a>
              </li>
              <li>
                <a className="footer-link" href="#product-demo">
                  Plans
                </a>
              </li>
              <li>
                <a className="footer-link" href="#contact">
                  Contact
                </a>
              </li>
            </ul>
          </div>

          <div className="col-6 col-lg-4">
            <h6 className="text-uppercase text-secondary small">Demo</h6>
            <ul className="list-unstyled mb-0">
              <li>
                <a className="footer-link" href="/worksheets">
                  Try the Generator
                </a>
              </li>
              <li>
                <span className="text-secondary">
                  Email: jbierowiec@fordham.edu
                </span>
              </li>
              <li>
                <span className="text-secondary">NYC, USA</span>
              </li>
            </ul>
          </div>
        </div>

        <hr className="border-secondary my-4" />

        <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-2">
          <small className="text-secondary">
            © {currentYear} Worksheets AI. All rights reserved.
          </small>
          <small className="text-secondary">
            Built for fast practice + clean PDFs.
          </small>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
