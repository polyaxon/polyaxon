import * as React from 'react';

function Header() {
  return (
    <nav id="top" className="navbar">
      <div id="top-brand" className="navbar-brand">
        <a className="navbar-item" href="https://polyaxon.com">
          <img
            src="/public/img/logo_white.svg"
            alt="Polyaxon: An open source platform for reproducible machine learning at scale on Kubernetes."
            width="40"
            height="50"
          /> Polyaxon
        </a>
      </div>

      <div id="navbarExampleTransparentExample" className="navbar-menu">
        <div className="navbar-end">
          <div className="navbar-item has-dropdown is-transparent is-hoverable">
            <a className="navbar-link">
              Right
            </a>

            <div className="navbar-dropdown is-right is-boxed">
              <a className="navbar-item">
                Overview
              </a>
              <a className="navbar-item">
                Elements
              </a>
              <a className="navbar-item">
                Components
              </a>
              <hr className="navbar-divider"/>
              <div className="navbar-item">
                Version 0.7.1
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Header;
