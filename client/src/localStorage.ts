import * as Cookies from 'js-cookie';
import { DEV_TOKEN, DEV_USER } from './constants/dev.env';
import { AppState } from './constants/types';

export const loadState = () => {
  try {
    const serializedState = localStorage.getItem('state');
    if (serializedState === null) {
      return undefined;
    }
    return JSON.parse(serializedState);
  } catch (err) {
    return undefined;
  }
};

export const saveState = (state: AppState) => {
  try {
    const serializedState = JSON.stringify(state);
    localStorage.setItem('state', serializedState);
  } catch (err) {
    // Ignore write errors.
  }
};

export const setLocalUser = () => {
  Cookies.set('token', DEV_TOKEN);
  Cookies.set('user', DEV_USER);
};
