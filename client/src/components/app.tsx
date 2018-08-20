import * as React from 'react';
import { Router } from 'react-router-dom';

import history from '../history';
import Routes from './routes';

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
