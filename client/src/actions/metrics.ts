import { Action } from 'redux';

import { BASE_API_URL } from '../constants/api';
import { MetricModel } from '../models/metric';
import { urlifyProjectName } from '../urls/utils';
import { stdHandleError } from './utils';

export enum actionTypes {
  FETCH_METRICS_REQUEST = 'FETCH_METRICS_REQUEST',
  FETCH_METRICS_SUCCESS = 'FETCH_METRICS_SUCCESS',
  FETCH_METRICS_ERROR = 'FETCH_METRICS_ERROR',
}

export interface FetchMetricsRequestAction extends Action {
  type: actionTypes.FETCH_METRICS_REQUEST;
}

export interface FetchMetricsSuccessAction extends Action {
  type: actionTypes.FETCH_METRICS_SUCCESS;
  metrics: MetricModel[];
  count: number;
}

export interface FetchMetricsErrorAction extends Action {
  type: actionTypes.FETCH_METRICS_ERROR;
  statusCode: number;
  error: any;
}

export function fetchMetricsRequestActionCreator(): FetchMetricsRequestAction {
  return {
    type: actionTypes.FETCH_METRICS_REQUEST,
  };
}

export function fetchMetricsSuccessActionCreator(metrics: MetricModel[], count: number): FetchMetricsSuccessAction {
  return {
    type: actionTypes.FETCH_METRICS_SUCCESS,
    metrics,
    count
  };
}

export function fetchMetricsErrorActionCreator(statusCode: number, error: any): FetchMetricsErrorAction {
  return {
    type: actionTypes.FETCH_METRICS_ERROR,
    statusCode,
    error
  };
}

export type MetricsAction =
  FetchMetricsRequestAction
  | FetchMetricsSuccessAction
  | FetchMetricsErrorAction;

export function fetchMetrics(projectUniqueName: string, resources: string, id: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(fetchMetricsRequestActionCreator());

    const metricsUrl =
      `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/metrics`;

    return fetch(metricsUrl, {
      headers: {
        'Content-Type': 'text/plain;charset=UTF-8',
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        fetchMetricsErrorActionCreator,
        'Metrics not found',
        'Failed to fetch metrics'))
      .then((response) => response.json())
      .then((json) => dispatch(fetchMetricsSuccessActionCreator(json.results, json.count)));
  };
}
