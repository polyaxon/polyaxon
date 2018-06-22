import { Action } from 'redux';
import { handleAuthError, urlifyProjectName } from '../constants/utils';
import { BASE_API_URL } from '../constants/api';

export enum actionTypes {
  RECEIVE_LOGS = 'RECEIVE_LOGS',
  REQUEST_LOGS = 'REQUEST_LOGS',
}

export interface RequestLogsAction extends Action {
  type: actionTypes.REQUEST_LOGS;
  logs: string;
}

export interface ReceiveLogsAction extends Action {
  type: actionTypes.RECEIVE_LOGS;
  logs: string;
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

export type LogsAction =
  RequestLogsAction
  | ReceiveLogsAction;

export function fetchLogs(projectUniqueName: string, resources: string, id: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestLogsActionCreator());

    let logsUrl =
      BASE_API_URL + `/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/logs`;

    return fetch(logsUrl, {
      headers: {
        'Content-Type': 'text/plain;charset=UTF-8',
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.text())
      .then(text => dispatch(receiveLogsActionCreator(text)))
      .catch(error => undefined);
  };
}
