import * as React from "react";
import {BrowserRouter} from "react-router-dom";


import Header from "./Header";
import Footer from "./Footer";
import Routes from "./Routes";

import "./App.less";


function App() {
  return (
      <BrowserRouter>
        <div>
          <Header />
          <Routes />
          <Footer />
        </div>
      </BrowserRouter>
  );
}

export default App;
