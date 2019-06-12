import { Action } from 'redux';

import { BASE_API_URL } from '../constants/api';
import { urlifyProjectName } from '../urls/utils';
import { stdHandleError } from './utils';

export enum actionTypes {
  FETCH_LOGS_REQUEST = 'FETCH_LOGS_REQUEST',
  FETCH_LOGS_SUCCESS = 'FETCH_LOGS_SUCCESS',
  FETCH_LOGS_ERROR = 'FETCH_LOGS_ERROR',
}

export interface FetchLogsRequestAction extends Action {
  type: actionTypes.FETCH_LOGS_REQUEST;
  logs: string;
}

export interface FetchLogsSuccessAction extends Action {
  type: actionTypes.FETCH_LOGS_SUCCESS;
  logs: string;
}

export interface FetchLogsErrorAction extends Action {
  type: actionTypes.FETCH_LOGS_ERROR;
  statusCode: number;
  error: any;
}

export function fetchLogsRequestActionCreator(): FetchLogsRequestAction {
  return {
    type: actionTypes.FETCH_LOGS_REQUEST,
    logs: ''
  };
}

export function fetchLogsSuccessActionCreator(logs: string): FetchLogsSuccessAction {
  return {
    type: actionTypes.FETCH_LOGS_SUCCESS,
    logs
  };
}

export function fetchLogsErrorActionCreator(statusCode: number, error: any): FetchLogsErrorAction {
  return {
    type: actionTypes.FETCH_LOGS_ERROR,
    statusCode,
    error
  };
}

export type LogsAction =
  FetchLogsRequestAction
  | FetchLogsSuccessAction
  | FetchLogsErrorAction;

export function fetchLogs(projectUniqueName: string,
                          resources: string,
                          id: number,
                          subResource?: string,
                          sid?: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(fetchLogsRequestActionCreator());

    let logsUrl = '';
    if (subResource && sid) {
      logsUrl =
        `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/${subResource}/${sid}/logs`;
    } else {
      logsUrl =
        `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/logs`;
    }

    return fetch(logsUrl, {
      headers: {
        'Content-Type': 'text/plain;charset=UTF-8',
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        fetchLogsErrorActionCreator,
        'Logs not found',
        'Failed to fetch logs'))
      .then((response) => response.text())
      .then((text) => dispatch(fetchLogsSuccessActionCreator(text)));
  };
}
