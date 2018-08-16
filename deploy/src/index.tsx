import * as React from 'react';
import * as ReactDOM from 'react-dom';

import App from './components/app';
import configureRaven from './configureRaven';

configureRaven();
ReactDOM.render(
  <App/>,
  document.getElementById('root') as HTMLElement
);
