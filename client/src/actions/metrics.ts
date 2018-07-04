import { Action } from 'redux';
import { urlifyProjectName } from '../constants/utils';
import { BASE_API_URL } from '../constants/api';
import { MetricModel } from '../models/metric';

export enum actionTypes {
  RECEIVE_METRICS = 'RECEIVE_METRICS',
  REQUEST_METRICS = 'REQUEST_METRICS',
  RECEIVE_METRICS_ERROR = 'RECEIVE_METRICS_ERROR',
}

export interface RequestMetricsAction extends Action {
  type: actionTypes.REQUEST_METRICS;
  metrics: string;
}

export interface ReceiveMetricsAction extends Action {
  type: actionTypes.RECEIVE_METRICS;
  metrics: MetricModel[];
  count: number;
}

export interface ReceiveErrorAction extends Action {
  type: actionTypes.RECEIVE_METRICS_ERROR;
  metricCode: number;
  msg: string;
}

export function requestMetricsActionCreator(): RequestMetricsAction {
  return {
    type: actionTypes.REQUEST_METRICS,
    metrics: ''
  };
}

export function receiveMetricsActionCreator(metrics: MetricModel[], count: number): ReceiveMetricsAction {
  return {
    type: actionTypes.RECEIVE_METRICS,
    metrics,
    count
  };
}

export function receiveErrorActionCreator(metricCode: number, msg: string): ReceiveErrorAction {
  return {
    type: actionTypes.RECEIVE_METRICS_ERROR,
    metricCode,
    msg
  };
}

export type MetricsAction =
  RequestMetricsAction
  | ReceiveMetricsAction
  | ReceiveErrorAction;

export function fetchMetrics(projectUniqueName: string, resources: string, id: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestMetricsActionCreator());

    let metricsUrl =
      BASE_API_URL + `/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/metrics`;

    function handleError(response: Response, dispatch: any): any {
      if (!response.ok) {
        if (response.status === 404) {
          dispatch(receiveErrorActionCreator(response.status, 'No metrics'));
        } else {
          dispatch(receiveErrorActionCreator(response.status, 'Failed to fetch metrics'));
        }

        return Promise.reject(response.statusText);
      }
      return response;
    }

    return fetch(metricsUrl, {
      headers: {
        'Content-Type': 'text/plain;charset=UTF-8',
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleError(response, dispatch))
      .then(response => response.json())
      .then(json => dispatch(receiveMetricsActionCreator(json.results, json.count)));
  };
}
