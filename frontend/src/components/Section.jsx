import React, { useEffect, useRef } from "react";

const Section = ({ id, title, children }) => {
  const ref = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate-in");
        }
      },
      { threshold: 0.3 }
    );
    if (ref.current) observer.observe(ref.current);
  }, []);

  return (
    <section id={id} ref={ref} className="section fade-section">
      <div className="section-container">
        <div className="section-title">
          <h2>{title}</h2>
        </div>
        <div className="section-content">{children}</div>
      </div>
    </section>
  );
};

export default Section;
