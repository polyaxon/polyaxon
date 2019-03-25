import { Action } from 'redux';

import { ChartViewModel } from '../../models/chartView';
import { actionTypes } from './actionTypes';

export interface GetChartViewRequestAction extends Action {
  type: actionTypes.GET_CHART_VIEW_REQUEST;
  viewId: number;
}

export interface GetChartViewSuccessAction extends Action {
  type: actionTypes.GET_CHART_VIEW_SUCCESS;
  chartView: ChartViewModel;
  viewId: number;
}

export interface GetChartViewErrorAction extends Action {
  type: actionTypes.GET_CHART_VIEW_ERROR;
  statusCode: number;
  error: any;
  viewId: number;
}

export function getChartViewRequestActionCreator(viewId: number): GetChartViewRequestAction {
  return {
    type: actionTypes.GET_CHART_VIEW_REQUEST,
    viewId
  };
}

export function getChartViewSuccessActionCreator(chartView: ChartViewModel): GetChartViewSuccessAction {
  return {
    type: actionTypes.GET_CHART_VIEW_SUCCESS,
    chartView,
    viewId: chartView.id
  };
}

export function getChartViewErrorActionCreator(statusCode: number, error: any, viewId: number): GetChartViewErrorAction {
  return {
    type: actionTypes.GET_CHART_VIEW_ERROR,
    statusCode,
    error,
    viewId
  };
}

export type GetChartViewAction =
  GetChartViewRequestAction
  | GetChartViewSuccessAction
  | GetChartViewErrorAction;
