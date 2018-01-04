import * as React from "react";
import {BrowserRouter} from "react-router-dom";


import Header from "./header";
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
        </div>
      </BrowserRouter>
  );
}

export default App;
