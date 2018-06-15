import { AppState } from './constants/types';
import * as Cookies from 'js-cookie';

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
  Cookies.set('token', '8ff04973157b2a5831329fbb1befd37f93e4de4f');
  Cookies.set('user', 'admin');
};
