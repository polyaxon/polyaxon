import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../constants/api';
import history from '../history';
import { ActivityLogModel } from '../models/activitylog';
import { getProjectUrl, } from '../urls/utils';
import { stdHandleError } from './utils';

export enum actionTypes {
  FETCH_ACTIVITY_LOGS_REQUEST = 'FETCH_ACTIVITY_LOGS_REQUEST',
  FETCH_ACTIVITY_LOGS_SUCCESS = 'FETCH_ACTIVITY_LOGS_SUCCESS',
  FETCH_ACTIVITY_LOGS_ERROR = 'FETCH_ACTIVITY_LOGS_ERROR',
}

export interface FetchActivityLogsSuccessAction extends Action {
  type: actionTypes.FETCH_ACTIVITY_LOGS_SUCCESS;
  activityLogs: ActivityLogModel[];
  count: number;
}

export interface FetchActivityLogsRequestAction extends Action {
  type: actionTypes.FETCH_ACTIVITY_LOGS_REQUEST;
}

export interface FetchActivityLogsFailureAction extends Action {
  type: actionTypes.FETCH_ACTIVITY_LOGS_ERROR;
  statusCode: number;
  error: any;
}

export function fetchActivityLogsSuccessActionCreator(activityLogs: ActivityLogModel[],
                                                      count: number): FetchActivityLogsSuccessAction {
  return {
    type: actionTypes.FETCH_ACTIVITY_LOGS_SUCCESS,
    activityLogs,
    count
  };
}

export function fetchActivityLogsRequestActionCreator(): FetchActivityLogsRequestAction {
  return {
    type: actionTypes.FETCH_ACTIVITY_LOGS_REQUEST,
  };
}

export function fetchActivityLogsFailureActionCreator(statusCode: number, error: any): FetchActivityLogsFailureAction {
  return {
    type: actionTypes.FETCH_ACTIVITY_LOGS_ERROR,
    statusCode,
    error
  };
}

export type ActivityLogAction =
  | FetchActivityLogsSuccessAction
  | FetchActivityLogsRequestAction
  | FetchActivityLogsFailureAction;

function _fetchActivityLogs(activityLogsUrl: string,
                            filters: { [key: string]: number | boolean | string } = {},
                            dispatch: any,
                            getState: any): any {
  dispatch(fetchActivityLogsRequestActionCreator());

  const urlPieces = location.hash.split('?');
  const baseUrl = urlPieces[0];
  if (Object.keys(filters).length) {
    activityLogsUrl += url.format({query: filters});
    if (baseUrl) {
      history.push(baseUrl + url.format({query: filters}));
    }
  } else if (urlPieces.length > 1) {
    history.push(baseUrl);
  }
  return fetch(
    activityLogsUrl, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
    .then((response) => stdHandleError(
        response,
        dispatch,
        fetchActivityLogsFailureActionCreator,
        'Activities not found',
        'Failed to fetch activities'))
    .then((response) => response.json())
    .then((json) => dispatch(fetchActivityLogsSuccessActionCreator(json.results, json.count)));
}

export function fetchActivityLogs(filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const activityLogsUrl = `${BASE_API_URL}/activitylogs`;
    return _fetchActivityLogs(activityLogsUrl, filters, dispatch, getState);
  };
}

export function fetchHistoryLogs(filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const activityLogsUrl = `${BASE_API_URL}/historylogs`;
    return _fetchActivityLogs(activityLogsUrl, filters, dispatch, getState);
  };
}

export function fetchProjectActivityLogs(user: string,
                                         projectName: string,
                                         filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const activityLogsUrl = `${BASE_API_URL}/activitylogs${getProjectUrl(user, projectName, false)}`;
    return _fetchActivityLogs(activityLogsUrl, filters, dispatch, getState);
  };
}
