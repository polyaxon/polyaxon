import { Action } from 'redux';
import { BASE_API_URL } from '../constants/api';
import { handleAuthError, urlifyProjectName } from '../constants/utils';
import { ChartViewModel } from '../models/chartView';
import { MetricModel } from '../models/metric';

export enum actionTypes {
  RECEIVE_METRICS = 'RECEIVE_METRICS',
  REQUEST_METRICS = 'REQUEST_METRICS',
  RECEIVE_METRICS_ERROR = 'RECEIVE_METRICS_ERROR',
  RECEIVE_CHART_VIEWS = 'RECEIVE_CHART_VIEWS',
  REQUEST_CHART_VIEWS = 'REQUEST_CHART_VIEWS',
  RECEIVE_CHART_VIEW = 'RECEIVE_CHART_VIEW',
  DELETE_CHART_VIEW = 'DELETE_CHART_VIEW',
}

export interface RequestMetricsAction extends Action {
  type: actionTypes.REQUEST_METRICS;
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

export interface RequestChartViewsAction extends Action {
  type: actionTypes.REQUEST_CHART_VIEWS;
}

export interface ReceiveChartViewsAction extends Action {
  type: actionTypes.RECEIVE_CHART_VIEWS;
  chartViews: ChartViewModel[];
  count: number;
}

export interface ReceiveChartViewAction extends Action {
  type: actionTypes.RECEIVE_CHART_VIEW;
  chartView: ChartViewModel;
}

export interface DeleteChartViewAction extends Action {
  type: actionTypes.DELETE_CHART_VIEW;
  viewId: number;
}

export function requestMetricsActionCreator(): RequestMetricsAction {
  return {
    type: actionTypes.REQUEST_METRICS,
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

export function requestChartViewsActionCreator(): RequestChartViewsAction {
  return {
    type: actionTypes.REQUEST_CHART_VIEWS,
  };
}

export function receiveChartViewsActionCreator(chartViews: ChartViewModel[], count: number): ReceiveChartViewsAction {
  return {
    type: actionTypes.RECEIVE_CHART_VIEWS,
    chartViews,
    count
  };
}

export function receiveChartViewActionCreator(chartView: ChartViewModel): ReceiveChartViewAction {
  return {
    type: actionTypes.RECEIVE_CHART_VIEW,
    chartView,
  };
}

export function deleteChartViewActionCreator(viewId: number): DeleteChartViewAction {
  return {
    type: actionTypes.DELETE_CHART_VIEW,
    viewId,
  };
}

export type MetricsAction =
  RequestMetricsAction
  | ReceiveMetricsAction
  | ReceiveErrorAction
  | ReceiveChartViewAction
  | RequestChartViewsAction
  | ReceiveChartViewsAction
  | DeleteChartViewAction;

export function fetchMetrics(projectUniqueName: string, resources: string, id: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestMetricsActionCreator());

    const metricsUrl =
      `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/metrics`;

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
      .then((response) => handleError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveMetricsActionCreator(json.results, json.count)));
  };
}

export function fetchChartViews(projectUniqueName: string, resources: string, id: number): any {
  return (dispatch: any, getState: any) => {
    const chartViewsUrl =
      `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/chartviews`;
    dispatch(requestChartViewsActionCreator());
    return fetch(
      chartViewsUrl, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveChartViewsActionCreator(json.results, json.count)));
  };
}

export function createChartView(projectUniqueName: string, resources: string, id: number, data: ChartViewModel): any {
  return (dispatch: any, getState: any) => {
    const chartViewsUrl =
      `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/chartviews`;

    delete data.id;
    if (!data.name) {
      delete data.name;
    }
    return fetch(
      chartViewsUrl, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        }
      })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveChartViewActionCreator(json)));
  };
}

export function deleteChartView(projectUniqueName: string, resources: string, id: number, viewId: number): any {
  return (dispatch: any, getState: any) => {
    const chartViewsUrl =
      `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/chartviews/${viewId}`;

    return fetch(
      chartViewsUrl, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then((json) => dispatch(deleteChartViewActionCreator(viewId)));
  };
}
