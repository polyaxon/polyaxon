import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { fetchOptionsSuccessActionCreator } from './fetch';

export interface PostOptionsRequestAction extends Action {
  type: actionTypes.POST_OPTIONS_REQUEST;
  section: string;
}

export interface PostOptionsSuccessAction extends Action {
  type: actionTypes.POST_OPTIONS_SUCCESS;
  section: string;
}

export interface PostOptionsErrorAction extends Action {
  type: actionTypes.POST_OPTIONS_ERROR;
  section: string;
  statusCode: number;
  error: any;
}

export function postOptionsRequestActionCreator(section: string): PostOptionsRequestAction {
  return {
    type: actionTypes.POST_OPTIONS_REQUEST,
    section
  };
}

export function postOptionsSuccessActionCreator(section: string): PostOptionsSuccessAction {
  return {
    type: actionTypes.POST_OPTIONS_SUCCESS,
    section
  };
}

export function postOptionsErrorActionCreator(section: string, statusCode: number, error: any): PostOptionsErrorAction {
  return {
    type: actionTypes.POST_OPTIONS_ERROR,
    section,
    statusCode,
    error
  };
}

export type PostOptionAction =
  PostOptionsRequestAction
  | PostOptionsSuccessAction
  | PostOptionsErrorAction;

export function postOptions(section: string, options: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {

    dispatch(postOptionsRequestActionCreator(section));

    return fetch(`${BASE_API_URL}/options`, {
      method: 'POST',
      body: JSON.stringify(options),
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdCreateHandleError(
        response,
        dispatch,
        postOptionsErrorActionCreator,
        'Not found',
        'Failed to update options'))
      .then((response) => response.json())
      .then((json) => {
        dispatch(postOptionsSuccessActionCreator(section));
        // return dispatch(fetchOptionsSuccessActionCreator(section, [json], 0));
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(postOptionsErrorActionCreator(section, response.status, value)));
        } else {
          return response.value;
        }
      });
  };
}
