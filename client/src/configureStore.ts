import {createStore} from "redux";
import "bootstrap/dist/css/bootstrap.min.css";
import {throttle} from 'lodash'


import appReducer from "./reducers/app";
import {AppState} from "./types/index";
import { loadState, saveState } from './localStorage'

const configureStore = () => {
  const persistedState = loadState();
  const store = createStore<AppState>(appReducer, persistedState);

  store.subscribe(throttle(() => {
    saveState(store.getState())
  }, 1000));

  return store;
};

export default configureStore
