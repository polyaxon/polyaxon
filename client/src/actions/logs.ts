import {Action} from 'redux';

export enum actionTypes {
  RECEIVE_LOGS = 'RECEIVE_LOGS',
  REQUEST_LOGS = 'REQUEST_LOGS',
}

export interface RequestLogsAction extends Action {
  type: actionTypes.REQUEST_LOGS;
}

export interface ReceiveLogsAction extends Action {
  type: actionTypes.RECEIVE_LOGS;
  logs: string[];
}

export function requestLogsActionCreator(): RequestLogsAction {
  return {
    type: actionTypes.REQUEST_LOGS,
  };
}

export function receiveLogsActionCreator(logs: string[]): ReceiveLogsAction {
  return {
    type: actionTypes.RECEIVE_LOGS,
    logs
  };
}

export type LogsAction =
  RequestLogsAction
  | ReceiveLogsAction;

export function fetchLogs(projectUniqueName: string, experimentSequence: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestLogsActionCreator());

    setTimeout(() => {
      const logs: string[] = []
      for (let i = 1; i < 10; i++) {
        logs.push('This is a log message')
      }
      dispatch(receiveLogsActionCreator(logs))
    }, 500);
    // return fetch(projectsUrl, {
    //   headers: {
    //     'Authorization': 'token ' + getState().auth.token
    //   }
    // })
    //   .then(response => handleAuthError(response, dispatch))
    //   .then(response => response.json())
    //   .then(json => dispatch(receiveProjectsActionCreator(json.results, json.count)))
    //   .catch(error => undefined);
  };
}
