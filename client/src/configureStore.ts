import { createStore, applyMiddleware } from 'redux';
import * as _ from 'lodash';

import thunk from 'redux-thunk';
import { createLogger } from 'redux-logger';

import appReducer from './reducers/app';
// import { AppState } from './constants/types';
import { loadState, saveState, setLocalUser } from './localStorage';
import { getToken } from './constants/utils';
import { receiveTokenActionCreator } from './actions/token';

const configureStore = () => {
  // const persistedState = loadState();

  let middleware = [thunk];
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

  let token = getToken();
  if (token !== null) {
    store.dispatch(receiveTokenActionCreator(token.user, token));
  }

  store.subscribe(_.throttle(() => {
    saveState(store.getState());
  },                         1000));

  return store;
};

export default configureStore;
