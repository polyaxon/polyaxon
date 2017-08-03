import * as React from "react";
import * as ReactDOM from "react-dom";
import {Provider} from "react-redux";
import "bootstrap/dist/css/bootstrap.min.css";

import App from "./components/App";
import configureStore from "./configureStore";


const store = configureStore();
store.subscribe(() => console.log(store.getState()));
// store.dispatch(createExperiment({id:123212313 * Math.random(), name:'Learn about actions'}));

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root") as HTMLElement
);

