import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Provider } from 'react-redux';

import App from './components/app';
import configureRaven from './configureRaven';
import configureStore from './configureStore';

const store = configureStore();
configureRaven();
ReactDOM.render(
  <Provider store={store}>
      <App />
  </Provider>,
  document.getElementById('root') as HTMLElement
);
