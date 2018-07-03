import { Action } from 'redux';
import { urlifyProjectName } from '../constants/utils';
import { BASE_API_URL } from '../constants/api';
import { StatusModel } from '../models/status';

export enum actionTypes {
  RECEIVE_STATUSES = 'RECEIVE_STATUSES',
  REQUEST_STATUSES = 'REQUEST_STATUSES',
  RECEIVE_STATUSES_ERROR = 'RECEIVE_STATUSES_ERROR',
}

export interface RequestStatusesAction extends Action {
  type: actionTypes.REQUEST_STATUSES;
  statuses: string;
}

export interface ReceiveStatusesAction extends Action {
  type: actionTypes.RECEIVE_STATUSES;
  statuses: StatusModel[];
  count: number;
}

export interface ReceiveErrorAction extends Action {
  type: actionTypes.RECEIVE_STATUSES_ERROR;
  statusCode: number;
  msg: string;
}

export function requestStatusesActionCreator(): RequestStatusesAction {
  return {
    type: actionTypes.REQUEST_STATUSES,
    statuses: ''
  };
}

export function receiveStatusesActionCreator(statuses: StatusModel[], count: number): ReceiveStatusesAction {
  return {
    type: actionTypes.RECEIVE_STATUSES,
    statuses,
    count
  };
}

export function receiveErrorActionCreator(statusCode: number, msg: string): ReceiveErrorAction {
  return {
    type: actionTypes.RECEIVE_STATUSES_ERROR,
    statusCode,
    msg
  };
}

export type StatusesAction =
  RequestStatusesAction
  | ReceiveStatusesAction
  | ReceiveErrorAction;

export function fetchStatuses(projectUniqueName: string, resources: string, id: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestStatusesActionCreator());

    let statusesUrl =
      BASE_API_URL + `/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/statuses`;

    function handleError(response: Response, dispatch: any): any {
      if (!response.ok) {
        if (response.status === 404) {
          dispatch(receiveErrorActionCreator(response.status, 'No statuses'));
        } else {
          dispatch(receiveErrorActionCreator(response.status, 'Failed to fetch statuses'));
        }

        return Promise.reject(response.statusText);
      }
      return response;
    }

    return fetch(statusesUrl, {
      headers: {
        'Content-Type': 'text/plain;charset=UTF-8',
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleError(response, dispatch))
      .then(response => response.json())
      .then(json => dispatch(receiveStatusesActionCreator(json.results, json.count)));
  };
}
