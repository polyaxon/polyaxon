import * as React from "react";
import {BrowserRouter} from "react-router-dom";


import Header from "./header";
import Footer from "./footer";
import Routes from "./routes";

import "./app.less";


function App() {
  return (
      <BrowserRouter>
        <div>
          <Header />
          <div className="container container-fluid">
            <Routes />
          </div>
          <Footer />
        </div>
      </BrowserRouter>
  );
}

export default App;
