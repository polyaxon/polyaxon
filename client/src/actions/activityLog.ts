import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../constants/api';
import {
  getProjectUrl,
  handleAuthError
} from '../constants/utils';
import history from '../history';
import { ActivityLogModel } from '../models/activitylog';

export enum actionTypes {
  RECEIVE_ACTIVITY_LOGS = 'RECEIVE_ACTIVITY_LOGS',
  REQUEST_ACTIVITY_LOGS = 'REQUEST_ACTIVITY_LOGS',
}

export interface ReceiveActivityLogsAction extends Action {
  type: actionTypes.RECEIVE_ACTIVITY_LOGS;
  activityLogs: ActivityLogModel[];
  count: number;
}

export interface RequestActivityLogsAction extends Action {
  type: actionTypes.REQUEST_ACTIVITY_LOGS;
}

export type ActivityLogAction =
  | ReceiveActivityLogsAction
  | RequestActivityLogsAction;

export function requestActivityLogsActionCreator(): RequestActivityLogsAction {
  return {
    type: actionTypes.REQUEST_ACTIVITY_LOGS,
  };
}

export function receiveActivityLogsActionCreator(activityLogs: ActivityLogModel[],
                                                 count: number): ReceiveActivityLogsAction {
  return {
    type: actionTypes.RECEIVE_ACTIVITY_LOGS,
    activityLogs,
    count
  };
}

function _fetchActivityLogs(activityLogsUrl: string,
                            filters: { [key: string]: number | boolean | string } = {},
                            dispatch: any,
                            getState: any): any {
  dispatch(requestActivityLogsActionCreator());
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
    .then((response) => handleAuthError(response, dispatch))
    .then((response) => response.json())
    .then((json) => dispatch(receiveActivityLogsActionCreator(json.results, json.count)));
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
    const activityLogsUrl = `${BASE_API_URL}/activitylogs/${getProjectUrl(user, projectName, false)}`;
    return _fetchActivityLogs(activityLogsUrl, filters, dispatch, getState);
  };
}
