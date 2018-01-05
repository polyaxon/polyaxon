import * as React from "react";

import {MenuItem, Nav, Navbar, NavDropdown} from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { getHomeUrl, getLogoutUrl, isUserAuthenticated } from "../constants/utils";
import "./header.less";


function Header() {
  return (
    <header>
      <Navbar inverse collapseOnSelect className="navbar">
        <Navbar.Header >
          <Navbar.Brand>
            <LinkContainer to={getHomeUrl()} className="nav-link brand">
              <a>
                <img src="/static/images/logo_white.svg" alt="Polyaxon"/>
              </a>
            </LinkContainer>
          </Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
        { isUserAuthenticated() &&
        <Navbar.Collapse>
          <Nav>
          </Nav>
          <Nav pullRight>
            <NavDropdown eventKey={3} title="Profile" id="basic-nav-dropdown">
              <MenuItem eventKey={3.1}>Docs</MenuItem>
              <MenuItem eventKey={3.2}>Github</MenuItem>
              <MenuItem divider />
              <MenuItem eventKey={3.3} href={getLogoutUrl()}>Logout</MenuItem>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
        }
      </Navbar>
    </header>
  );
}

export default Header;

