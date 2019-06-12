import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { ChartViewModel } from '../../models/chartView';
import { urlifyProjectName } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getChartViewSuccessActionCreator } from './get';

export interface CreateChartViewRequestAction extends Action {
  type: actionTypes.CREATE_CHART_VIEW_REQUEST;
}

export interface CreateChartViewSuccessAction extends Action {
  type: actionTypes.CREATE_CHART_VIEW_SUCCESS;
}

export interface CreateChartViewErrorAction extends Action {
  type: actionTypes.CREATE_CHART_VIEW_ERROR;
  statusCode: number;
  error: any;
}

export function createChartViewRequestActionCreator(): CreateChartViewRequestAction {
  return {
    type: actionTypes.CREATE_CHART_VIEW_REQUEST,
  };
}

export function createChartViewSuccessActionCreator(): CreateChartViewSuccessAction {
  return {
    type: actionTypes.CREATE_CHART_VIEW_SUCCESS,
  };
}

export function createChartViewErrorActionCreator(statusCode: number, error: any): CreateChartViewErrorAction {
  return {
    type: actionTypes.CREATE_CHART_VIEW_ERROR,
    statusCode,
    error
  };
}

export type CreateChartViewAction =
  CreateChartViewRequestAction
  | CreateChartViewSuccessAction
  | CreateChartViewErrorAction;

export function createChartView(projectUniqueName: string, resources: string, id: number, data: ChartViewModel): any {
  return (dispatch: any, getState: any) => {
    dispatch(createChartViewRequestActionCreator());

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
      .then((response) => stdCreateHandleError(
        response,
        dispatch,
        createChartViewErrorActionCreator,
        'Not found',
        'Failed to create chart views'))
      .then((response) => response.json())
      .then((json) => {
        dispatch(createChartViewSuccessActionCreator());
        return dispatch(getChartViewSuccessActionCreator(json));
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(createChartViewErrorActionCreator(response.status, value)));
        } else {
          return response.value;
        }
      });
  };
}
