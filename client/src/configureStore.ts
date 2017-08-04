import {createStore, applyMiddleware} from "redux";
import "bootstrap/dist/css/bootstrap.min.css";
import {throttle} from 'lodash'
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'


import appReducer from "./reducers/app";
import {AppState} from "./types/index";
import { loadState, saveState } from './localStorage'

const configureStore = () => {
  const persistedState = loadState();
  const loggerMiddleware = createLogger();

  const store = createStore<AppState>(
    appReducer,
    persistedState,
    applyMiddleware(
      thunkMiddleware,
      loggerMiddleware
    )
  );

  store.subscribe(throttle(() => {
    saveState(store.getState())
  }, 1000));

  return store;
};

export default configureStore
