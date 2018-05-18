import { Action } from 'redux';

import { BASE_API_URL } from '../constants/api';
import { UserModel } from '../models/user';
import { discardToken } from '../actions/token';
import { delay, getToken } from '../constants/utils';

export enum actionTypes {
  RECEIVE_USER = 'RECEIVE_USER',
  DISCARD_USER = 'DISCARD_USER',
}

export interface ReceiveUserAction extends Action {
  type: actionTypes.RECEIVE_USER;
  user: UserModel;
}

export interface DiscardUserAction extends Action {
  type: actionTypes.DISCARD_USER;
}

export type UserAction = DiscardUserAction | ReceiveUserAction;

export function receiveUserActionCreator(user: UserModel): ReceiveUserAction {
  return {
    type: actionTypes.RECEIVE_USER,
    user
  };
}

export function discardUserActionCreator(): DiscardUserAction {
  return {
    type: actionTypes.DISCARD_USER,
  };
}

export function fetchUser(): any {
  function handleAuthError(response: any, dispatch: any) {
    if (!response.ok) {
      dispatch(discardToken());
      return Promise.reject(response.statusText);
    }
    return response;
  }

  return (dispatch: any) => {
    let token = getToken();
    if (token === null) {
      return dispatch(discardToken());
    }

    return fetch(BASE_API_URL + '/users', {
      method: 'GET',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + token.token
      }
    })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json =>
        new Promise(function(resolve: any, reject: any) {
          dispatch(receiveUserActionCreator(json));
          resolve();
        }))
      .catch(error => undefined);
  };
}

export function discardUser(): any {
  return (dispatch: any) =>
    new Promise(function(resolve: any, reject: any) {
      dispatch(discardUserActionCreator());
      resolve();
    });
}
