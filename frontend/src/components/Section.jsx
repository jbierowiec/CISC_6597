import React from "react";

const Section = ({ id, title, subtitle, children, aos = "fade-up" }) => {
  return (
    <section id={id} className="snap-section">
      <div className="container" data-aos={aos}>
        <div className="text-center mb-4">
          <h2 className="section-title">{title}</h2>
          {subtitle ? <p className="section-subtitle">{subtitle}</p> : null}
        </div>
        {children}
      </div>
    </section>
  );
};

export default Section;
