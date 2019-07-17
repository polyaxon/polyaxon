import { Action } from 'redux';

import { discardUser, fetchUser } from '../actions/user';
import { BASE_API_URL } from '../constants/api';
import { TokenModel } from '../models/token';

export enum actionTypes {
  FETCH_TOKEN_REQUEST = 'FETCH_TOKEN_REQUEST',
  FETCH_TOKEN_SUCCESS = 'FETCH_TOKEN_SUCCESS',
  FETCH_TOKEN_ERROR = 'FETCH_TOKEN_ERROR',
  DISCARD_TOKEN = 'DISCARD_TOKEN',
}

export interface FetchTokenRequestAction extends Action {
  type: actionTypes.FETCH_TOKEN_REQUEST;
  username: string;
  password: string;
}

export interface FetchTokenSuccessAction extends Action {
  type: actionTypes.FETCH_TOKEN_SUCCESS;
  username: string;
  token: TokenModel;
}

export interface FetchTokenErrorAction extends Action {
  type: actionTypes.FETCH_TOKEN_ERROR;
}

export interface DiscardTokenAction extends Action {
  type: actionTypes.DISCARD_TOKEN;
}

export function fetchTokenSuccessActionCreator(username: string, token: TokenModel): FetchTokenSuccessAction {
  return {
    type: actionTypes.FETCH_TOKEN_SUCCESS,
    username,
    token
  };
}

export function discardTokenActionCreator(): DiscardTokenAction {
  return {
    type: actionTypes.DISCARD_TOKEN,
  };
}

export type TokenAction =
  FetchTokenRequestAction
  | FetchTokenSuccessAction
  | FetchTokenErrorAction
  | DiscardTokenAction ;

export function logout(): any {
  function handleErrors(response: any) {
    if (!response.ok) {
      return Promise.reject(response.statusText);
    }
    return response;
  }

  return (dispatch: any) => {
    return fetch(BASE_API_URL + '/users/logout', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    })
      .then(handleErrors)
      .then((json) => dispatch(discardToken()));
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

  const credentials = {
    username,
    password,
    login: true
  };
  return (dispatch: any) => {
    return fetch(BASE_API_URL + '/users/token', {
      method: 'POST',
      body: JSON.stringify(credentials),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    })
      .then(handleErrors)
      .then((response) => response.json())
      .then((json) => dispatch(fetchTokenSuccessActionCreator(username, json)))
      .then(() => dispatch(fetchUser()));
  };
}

export function discardToken(): any {
  return (dispatch: any, getState: any) => {
    return fetch(BASE_API_URL + '/users/logout', {
      method: 'GET',
      headers: {
        'X-CSRFToken': getState().auth.csrftoken
      },
      credentials: 'include',
    }).then(dispatch(discardTokenActionCreator()))
      .then(dispatch(discardUser()))
      .then(() => {
          window.location.reload();
        }
      );
  };
}

export function refreshSession(): any {
  function handleErrors(response: any) {
    if (!response.ok) {
      return Promise.reject(response.statusText);
    }
    return response;
  }

  return (dispatch: any, getState: any) => fetch(BASE_API_URL + '/users/session/refresh', {
    method: 'POST',
    headers: {
        Authorization: 'token ' + getState().auth.token
    },
    credentials: 'include'
  })
    .then(handleErrors);
}
