import * as React from 'react';
import { BrowserRouter } from 'react-router-dom';

import Routes from './routes';

import './app.less';

function App() {
  return (
    <BrowserRouter>
      <div>
        <Routes/>
      </div>
    </BrowserRouter>
  );
}

export default App;
