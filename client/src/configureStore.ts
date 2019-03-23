import * as _ from 'lodash';
import { applyMiddleware, createStore } from 'redux';

import { createLogger } from 'redux-logger';
import thunk from 'redux-thunk';

import { fetchTokenSuccessActionCreator } from './actions/token';
import { getToken } from './constants/utils';
// import { AppState } from './constants/types';
import { loadState, saveState, setLocalUser } from './localStorage';
import appReducer from './reducers/app';

const configureStore = () => {
  // const persistedState = loadState();

  const middleware = [thunk];
  let newMiddleware = [];
  if (process.env.NODE_ENV !== 'production') {
    setLocalUser();
    const loggerMiddleware = createLogger();
    newMiddleware = [...middleware, loggerMiddleware];
  } else {
    newMiddleware = middleware;
  }

  const store = createStore(
    appReducer,
    // persistedState,
    applyMiddleware(...newMiddleware)
  );

  const token = getToken();
  if (token !== null) {
    store.dispatch(fetchTokenSuccessActionCreator(token.user, token));
  }

  store.subscribe(_.throttle(() => {
    saveState(store.getState());
  },                         1000));

  return store;
};

export default configureStore;
