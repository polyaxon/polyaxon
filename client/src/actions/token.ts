import { Action } from 'redux';

import { TokenModel } from '../models/token';
import { BASE_URL } from '../constants/api';
import { discardUser, fetchUser } from '../actions/user';
import { delay } from '../constants/utils';

export enum actionTypes {
  FETCH_TOKEN = 'FETCH_TOKEN',
  RECEIVE_TOKEN = 'RECEIVE_TOKEN',
  DISCARD_TOKEN = 'DISCARD_TOKEN',
}

export interface FetchTokenAction extends Action {
  type: actionTypes.FETCH_TOKEN;
  username: string;
  password: string;
}

export interface ReceiveTokenAction extends Action {
  type: actionTypes.RECEIVE_TOKEN;
  username: string;
  token: TokenModel;
}

export interface DiscardTokenAction extends Action {
  type: actionTypes.DISCARD_TOKEN;
}

export type TokenAction = FetchTokenAction | DiscardTokenAction | ReceiveTokenAction;

export function receiveTokenActionCreator(username: string, token: TokenModel): ReceiveTokenAction {
  return {
    type: actionTypes.RECEIVE_TOKEN,
    username,
    token
  };
}

export function discardTokenActionCreator(): DiscardTokenAction {
  return {
    type: actionTypes.DISCARD_TOKEN,
  };
}

export function logout(): any {
  function handleErrors(response: any) {
    if (!response.ok) {
      return Promise.reject(response.statusText);
    }
    return response;
  }

  return (dispatch: any) => {
    return fetch(BASE_URL + '/users/logout', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    })
      .then(handleErrors)
      .then(json => dispatch(discardToken()));
  };
}

export function login(username: string, password: string): any {
  return (dispatch: any) => {
    return dispatch(logout()).then(() => dispatch(fetchToken(username, password)));
  };
}

export function fetchToken(username: string, password: string): any {
  function handleErrors(response: any) {
    if (!response.ok) {
      return Promise.reject(response.statusText);
    }
    return response;
  }

  let credentials = {
    username: username,
    password: password,
    login: true
  };
  return (dispatch: any) => {
    return fetch(BASE_URL + '/users/token', {
      method: 'POST',
      body: JSON.stringify(credentials),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    })
      .then(handleErrors)
      .then(response => response.json())
      .then(json => dispatch(receiveTokenActionCreator(username, json)))
      .then(() => dispatch(fetchUser()));
  };
}

export function discardToken(): any {
  return (dispatch: any) =>
    new Promise(function(resolve: any, reject: any) {
      dispatch(discardTokenActionCreator());
      dispatch(discardUser()).then(
        () => resolve()
    ).catch((error: any) => reject(error))
    });
}

export function refreshSession(): any {
  function handleErrors(response: any) {
    if (!response.ok) {
      return Promise.reject(response.statusText);
    }
    return response;
  }

  return (dispatch: any, getState: any) => fetch(BASE_URL + '/users/session/refresh', {
    method: 'POST',
    headers: {
        'Authorization': 'token ' + getState().auth.token
    },
    credentials: 'include'
  })
    .then(handleErrors);
}
