import * as React from "react";
import * as ReactDOM from "react-dom";
import {createStore} from "redux";
import {Provider} from "react-redux";
import 'bootstrap/dist/css/bootstrap.min.css';

import appReducer from './reducers/app';
import {AppState} from './types/index';
import App from './components/App';

const store = createStore<AppState>(appReducer);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root') as HTMLElement
);

