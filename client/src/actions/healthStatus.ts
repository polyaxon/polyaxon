import { Action } from 'redux';

import { BASE_URL } from '../constants/api';
import { stdHandleError } from './utils';

export enum actionTypes {
  FETCH_HEALTH_STATUS_REQUEST = 'FETCH_HEALTH_STATUS_REQUEST',
  FETCH_HEALTH_STATUS_SUCCESS = 'FETCH_HEALTH_STATUS_SUCCESS',
  FETCH_HEALTH_STATUS_ERROR = 'FETCH_HEALTH_STATUS_ERROR',
}

export interface FetchHealthStatusRequestAction extends Action {
  type: actionTypes.FETCH_HEALTH_STATUS_REQUEST;
}

export interface FetchHealthStatusSuccessAction extends Action {
  type: actionTypes.FETCH_HEALTH_STATUS_SUCCESS;
  status: { [key: string]: any };
}

export interface FetchHealthStatusErrorAction extends Action {
  type: actionTypes.FETCH_HEALTH_STATUS_ERROR;
  statusCode: number;
  error: any;
}

export function fetchHealthStatusRequestActionCreator(): FetchHealthStatusRequestAction {
  return {
    type: actionTypes.FETCH_HEALTH_STATUS_REQUEST,
  };
}

export function fetchHealthStatusSuccessActionCreator(status: { [key: string]: any }): FetchHealthStatusSuccessAction {
  return {
    type: actionTypes.FETCH_HEALTH_STATUS_SUCCESS,
    status
  };
}

export function fetchHealthStatusErrorActionCreator(statusCode: number, error: any): FetchHealthStatusErrorAction {
  return {
    type: actionTypes.FETCH_HEALTH_STATUS_ERROR,
    statusCode,
    error
  };
}

export type HealthStatusAction =
  FetchHealthStatusRequestAction
  | FetchHealthStatusSuccessAction
  | FetchHealthStatusErrorAction;

export function fetchHealthStatus(): any {
  return (dispatch: any) => {
    dispatch(fetchHealthStatusRequestActionCreator());

    return fetch(BASE_URL + '/_status', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        fetchHealthStatusErrorActionCreator,
        'Health status not found',
        'Failed to fetch health status'))
      .then((response) => response.json())
      .then((json) => dispatch(fetchHealthStatusSuccessActionCreator(json)));
  };
}
