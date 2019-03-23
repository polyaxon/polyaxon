import { Action } from 'redux';

import { discardToken } from '../actions/token';
import { BASE_API_URL } from '../constants/api';
import { getToken } from '../constants/utils';
import { UserModel } from '../models/user';

export enum actionTypes {
  FETCH_USER_REQUEST = 'FETCH_USER_REQUEST',
  FETCH_USER_SUCCESS = 'FETCH_USER_SUCCESS',
  FETCH_USER_ERROR = 'FETCH_USER_ERROR',
  DISCARD_USER = 'DISCARD_USER',
}

export interface FetchUserRequestAction extends Action {
  type: actionTypes.FETCH_USER_REQUEST;
}

export interface FetchUserSuccessAction extends Action {
  type: actionTypes.FETCH_USER_SUCCESS;
  user: UserModel;
}

export interface FetchUserErrorAction extends Action {
  type: actionTypes.FETCH_USER_ERROR;
  statusCode: number;
  error: any;
}

export interface DiscardUserAction extends Action {
  type: actionTypes.DISCARD_USER;
}

export function fetchUserRequestActionCreator(): FetchUserRequestAction {
  return {
    type: actionTypes.FETCH_USER_REQUEST,
  };
}

export function fetchUserSuccessActionCreator(user: UserModel): FetchUserSuccessAction {
  return {
    type: actionTypes.FETCH_USER_SUCCESS,
    user
  };
}

export function fetchUserErrorActionCreator(statusCode: number, error: any): FetchUserErrorAction {
  return {
    type: actionTypes.FETCH_USER_ERROR,
    statusCode,
    error
  };
}

export function discardUserActionCreator(): DiscardUserAction {
  return {
    type: actionTypes.DISCARD_USER,
  };
}

export type UserAction =
  DiscardUserAction
  | FetchUserRequestAction
  | FetchUserSuccessAction
  | FetchUserErrorAction;

export function fetchUser(): any {
  function handleAuthError(response: any, dispatch: any) {
    if (!response.ok) {
      dispatch(fetchUserErrorActionCreator(response.status, response.statusText));
      dispatch(discardToken());
      return Promise.reject(response.statusText);
    }
    return response;
  }

  return (dispatch: any) => {
    dispatch(fetchUserRequestActionCreator());

    const token = getToken();
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
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) =>
        new Promise(function (resolve: any, reject: any) {
          dispatch(fetchUserSuccessActionCreator(json));
          resolve();
        }))
      .catch((error) => undefined);
  };
}

export function discardUser(): any {
  return (dispatch: any) =>
    new Promise(function (resolve: any, reject: any) {
      dispatch(discardUserActionCreator());
      resolve();
    });
}
