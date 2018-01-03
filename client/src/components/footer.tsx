import * as React from "react";
import {MenuItem} from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";

import "./footer.less";

function Footer() {
  return (
    <footer className="site-footer">
        <div className="footer-container">
            &copy; 2017 Polyaxon

            <nav>
                <MenuItem href="https://polyaxon.com/about">About</MenuItem>
            </nav>

            <nav className="social">
              <a href="https://twitter.com/polyaxonai" title="Follow on Twitter" target="_blank"><i className="icon icon-twitter"></i></a>
              <a href="https://github.com/polyaxon" title="Watch on Github" target="_blank"><i className="icon icon-github"></i></a>
            </nav>
            <div>Made with <i className="love">♥</i></div>
        </div>
    </footer>
  );
}

export default Footer;

