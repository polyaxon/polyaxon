import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../../constants/api';
import { OptionModel } from '../../models/option';
import { stdFetchHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchOptionsRequestAction extends Action {
  type: actionTypes.FETCH_OPTIONS_REQUEST;
  section: string
}

export interface FetchOptionsSuccessAction extends Action {
  type: actionTypes.FETCH_OPTIONS_SUCCESS;
  section: string;
  options: OptionModel[];
  count: number;
}

export interface FetchOptionsErrorAction extends Action {
  type: actionTypes.FETCH_OPTIONS_ERROR;
  section: string;
  statusCode: number;
  error: any;
}

export function fetchOptionsRequestActionCreator(section: string): FetchOptionsRequestAction {
  return {
    type: actionTypes.FETCH_OPTIONS_REQUEST,
    section
  };
}

export function fetchOptionsSuccessActionCreator(section: string,
                                                 options: OptionModel[],
                                                 count: number): FetchOptionsSuccessAction {
  return {
    type: actionTypes.FETCH_OPTIONS_SUCCESS,
    section,
    options,
    count
  };
}

export function fetchOptionsErrorActionCreator(section: string,
                                               statusCode: number,
                                               error: any): FetchOptionsErrorAction {
  return {
    type: actionTypes.FETCH_OPTIONS_ERROR,
    section,
    statusCode,
    error,
  };
}

export type FetchOptionAction =
  FetchOptionsRequestAction
  | FetchOptionsSuccessAction
  | FetchOptionsErrorAction;

function _fetchOptions(section: string,
                       optionsUrl: string,
                       dispatch: any,
                       getState: any): any {

  dispatch(fetchOptionsRequestActionCreator(section));
  return fetch(
    optionsUrl, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
    .then((response) => stdFetchHandleError(
      response,
      dispatch,
      fetchOptionsErrorActionCreator,
      'Options not found',
      'Failed to fetch Options',
      [section]))
    .then((response) => response.json())
    .then((json) => dispatch(fetchOptionsSuccessActionCreator(section, json, json.length)))
    .catch((response) => {
      if (response.status === 400) {
        return response.value.json().then(
          (value: any) => dispatch(fetchOptionsErrorActionCreator(section, response.status, value)));
      } else {
        return response.value;
      }
    });
}

export function fetchOptions(section: string, keys: string[]): any {
  return (dispatch: any, getState: any) => {
    const optionsUrl = `${BASE_API_URL}/options${url.format({query: {keys}})}`;
    return _fetchOptions(section, optionsUrl, dispatch, getState);
  };
}
