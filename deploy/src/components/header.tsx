import * as React from 'react';

function Header() {
  return (
    <div className="hero-head">
      <nav id="top" className="navbar">
        <div id="top-brand" className="navbar-brand">
          <a className="navbar-item" href="https://polyaxon.com">
            <img
              src="./public/images/logo_white.svg"
              alt="Polyaxon: An open source platform for reproducible machine learning at scale on Kubernetes."
              width="40"
              height="50"
            /> Polyaxon
          </a>
        </div>
      </nav>
    </div>
  );
}

export default Header;
