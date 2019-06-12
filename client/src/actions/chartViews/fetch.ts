import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { ChartViewModel } from '../../models/chartView';
import { urlifyProjectName } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchChartViewsRequestAction extends Action {
  type: actionTypes.FETCH_CHART_VIEWS_REQUEST;
}

export interface FetchChartViewsSuccessAction extends Action {
  type: actionTypes.FETCH_CHART_VIEWS_SUCCESS;
  chartViews: ChartViewModel[];
  count: number;
}

export interface FetchChartViewsErrorAction extends Action {
  type: actionTypes.FETCH_CHART_VIEWS_ERROR;
  statusCode: number;
  error: any;
}

export function fetchChartViewsRequestActionCreator(): FetchChartViewsRequestAction {
  return {
    type: actionTypes.FETCH_CHART_VIEWS_REQUEST,
  };
}

export function fetchChartViewsSuccessActionCreator(chartViews: ChartViewModel[],
                                                    count: number): FetchChartViewsSuccessAction {
  return {
    type: actionTypes.FETCH_CHART_VIEWS_SUCCESS,
    chartViews,
    count
  };
}

export function fetchChartViewsErrorActionCreator(statusCode: number, error: any): FetchChartViewsErrorAction {
  return {
    type: actionTypes.FETCH_CHART_VIEWS_ERROR,
    statusCode,
    error
  };
}

export type FetchChartViewAction =
  FetchChartViewsRequestAction
  | FetchChartViewsSuccessAction
  | FetchChartViewsErrorAction;

export function fetchChartViews(projectUniqueName: string, resources: string, id: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(fetchChartViewsRequestActionCreator());

    const chartViewsUrl =
      `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/chartviews`;

    return fetch(
      chartViewsUrl, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        fetchChartViewsErrorActionCreator,
        'Chart views not found',
        'Failed to fetch chart views'))
      .then((response) => response.json())
      .then((json) => dispatch(fetchChartViewsSuccessActionCreator(json.results, json.count)));
  };
}
