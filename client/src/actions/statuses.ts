import { Action } from 'redux';

import { BASE_API_URL } from '../constants/api';
import { StatusModel } from '../models/status';
import { urlifyProjectName } from '../urls/utils';
import { stdHandleError } from './utils';

export enum actionTypes {
  FETCH_STATUSES_REQUEST = 'FETCH_STATUSES_REQUEST',
  FETCH_STATUSES_SUCCESS = 'FETCH_STATUSES_SUCCESS',
  FETCH_STATUSES_ERROR = 'FETCH_STATUSES_ERROR',
}

export interface FetchStatusesRequestAction extends Action {
  type: actionTypes.FETCH_STATUSES_REQUEST;
}

export interface FetchStatusesSuccessAction extends Action {
  type: actionTypes.FETCH_STATUSES_SUCCESS;
  statuses: StatusModel[];
  count: number;
}

export interface FetchStatusesErrorAction extends Action {
  type: actionTypes.FETCH_STATUSES_ERROR;
  statusCode: number;
  error: any;
}

export function fetchStatusesRequestActionCreator(): FetchStatusesRequestAction {
  return {
    type: actionTypes.FETCH_STATUSES_REQUEST,
  };
}

export function fetchStatusesSuccessActionCreator(statuses: StatusModel[], count: number): FetchStatusesSuccessAction {
  return {
    type: actionTypes.FETCH_STATUSES_SUCCESS,
    statuses,
    count
  };
}

export function fetchStatusesErrorActionCreator(statusCode: number, error: any): FetchStatusesErrorAction {
  return {
    type: actionTypes.FETCH_STATUSES_ERROR,
    statusCode,
    error
  };
}

export type StatusesAction =
  FetchStatusesRequestAction
  | FetchStatusesSuccessAction
  | FetchStatusesErrorAction;

export function fetchStatuses(projectUniqueName: string,
                              resources: string,
                              id: number,
                              subResource?: string,
                              sid?: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(fetchStatusesRequestActionCreator());

    let statusesUrl = '';
    if (subResource && sid) {
      statusesUrl =
        `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/${subResource}/${sid}/statuses`;
    } else {
      statusesUrl =
        `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/statuses`;
    }

    return fetch(statusesUrl, {
      headers: {
        'Content-Type': 'text/plain;charset=UTF-8',
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        fetchStatusesErrorActionCreator,
        'Statuses not found',
        'Failed to fetch statuses'))
      .then((response) => response.json())
      .then((json) => dispatch(fetchStatusesSuccessActionCreator(json.results, json.count)));
  };
}
