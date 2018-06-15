import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import 'bootstrap/dist/css/bootstrap.min.css';

import App from './components/app';
import configureStore from './configureStore';
import configureRaven from './configureRaven';

const store = configureStore();
configureRaven();
ReactDOM.render(
  <Provider store={store}>
      <App />
  </Provider>,
  document.getElementById('root') as HTMLElement
);
