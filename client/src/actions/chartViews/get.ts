import { Action } from 'redux';

import { ChartViewModel } from '../../models/chartView';
import { actionTypes } from './actionTypes';

export interface GetChartViewRequestAction extends Action {
  type: actionTypes.GET_CHART_VIEW_REQUEST;
}

export interface GetChartViewSuccessAction extends Action {
  type: actionTypes.GET_CHART_VIEW_SUCCESS;
  chartView: ChartViewModel;
}

export interface GetChartViewErrorAction extends Action {
  type: actionTypes.GET_CHART_VIEW_ERROR;
  statusCode: number;
  error: any;
}

export function getChartViewRequestActionCreator(): GetChartViewRequestAction {
  return {
    type: actionTypes.GET_CHART_VIEW_REQUEST,
  };
}

export function getChartViewSuccessActionCreator(chartView: ChartViewModel): GetChartViewSuccessAction {
  return {
    type: actionTypes.GET_CHART_VIEW_SUCCESS,
    chartView,
  };
}

export function getChartViewErrorActionCreator(statusCode: number, error: any): GetChartViewErrorAction {
  return {
    type: actionTypes.GET_CHART_VIEW_ERROR,
    statusCode,
    error
  };
}

export type GetChartViewAction =
  GetChartViewRequestAction
  | GetChartViewSuccessAction
  | GetChartViewErrorAction;
