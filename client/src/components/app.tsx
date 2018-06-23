import * as React from 'react';
import { Router } from 'react-router-dom';

import Routes from './routes';
import history from '../history';

import './app.less';

function App() {
  return (
    <Router history={history}>
      <div>
        <Routes/>
      </div>
    </Router>
  );
}

export default App;
