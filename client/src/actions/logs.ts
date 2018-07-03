import { Action } from 'redux';
import { urlifyProjectName } from '../constants/utils';
import { BASE_API_URL } from '../constants/api';

export enum actionTypes {
  RECEIVE_LOGS = 'RECEIVE_LOGS',
  REQUEST_LOGS = 'REQUEST_LOGS',
  RECEIVE_LOGS_ERROR = 'RECEIVE_LOGS_ERROR',
}

export interface RequestLogsAction extends Action {
  type: actionTypes.REQUEST_LOGS;
  logs: string;
}

export interface ReceiveLogsAction extends Action {
  type: actionTypes.RECEIVE_LOGS;
  logs: string;
}

export interface ReceiveErrorAction extends Action {
  type: actionTypes.RECEIVE_LOGS_ERROR;
  statusCode: number;
  msg: string;
}

export function requestLogsActionCreator(): RequestLogsAction {
  return {
    type: actionTypes.REQUEST_LOGS,
    logs: ''
  };
}

export function receiveLogsActionCreator(logs: string): ReceiveLogsAction {
  return {
    type: actionTypes.RECEIVE_LOGS,
    logs
  };
}

export function receiveErrorActionCreator(statusCode: number, msg: string): ReceiveErrorAction {
  return {
    type: actionTypes.RECEIVE_LOGS_ERROR,
    statusCode,
    msg
  };
}

export type LogsAction =
  RequestLogsAction
  | ReceiveLogsAction
  | ReceiveErrorAction;

export function fetchLogs(projectUniqueName: string, resources: string, id: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestLogsActionCreator());

    let logsUrl =
      BASE_API_URL + `/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/logs`;

    function handleError(response: Response, dispatch: any): any {
      if (!response.ok) {
        if (response.status === 404) {
          dispatch(receiveErrorActionCreator(response.status, 'No logs'));
        } else {
          dispatch(receiveErrorActionCreator(response.status, 'Failed to fetch logs'));
        }

        return Promise.reject(response.statusText);
      }
      return response;
    }

    return fetch(logsUrl, {
      headers: {
        'Content-Type': 'text/plain;charset=UTF-8',
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleError(response, dispatch))
      .then(response => response.text())
      .then(text => dispatch(receiveLogsActionCreator(text)))
      .catch(error => undefined);
  };
}
