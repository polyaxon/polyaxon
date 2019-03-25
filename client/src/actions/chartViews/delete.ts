import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { urlifyProjectName } from '../../constants/utils';
import { stdDeleteHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface DeleteChartViewRequestAction extends Action {
  type: actionTypes.DELETE_CHART_VIEW_REQUEST;
  viewId: number;
}

export interface DeleteChartViewSuccessAction extends Action {
  type: actionTypes.DELETE_CHART_VIEW_SUCCESS;
  viewId: number;
}

export interface DeleteChartViewErrorAction extends Action {
  type: actionTypes.DELETE_CHART_VIEW_ERROR;
  statusCode: number;
  error: any;
  viewId: number;
}

export function deleteChartViewSuccessActionCreator(viewId: number): DeleteChartViewSuccessAction {
  return {
    type: actionTypes.DELETE_CHART_VIEW_SUCCESS,
    viewId,
  };
}

export function deleteChartViewErrorActionCreator(statusCode: number,
                                                  error: any,
                                                  viewId: number): DeleteChartViewErrorAction {
  return {
    type: actionTypes.DELETE_CHART_VIEW_ERROR,
    statusCode,
    error,
    viewId,
  };
}

export function deleteChartViewRequestActionCreator(viewId: number): DeleteChartViewRequestAction {
  return {
    type: actionTypes.DELETE_CHART_VIEW_REQUEST,
    viewId
  };
}

export type DeleteChartViewAction =
  DeleteChartViewSuccessAction
  | DeleteChartViewErrorAction
  | DeleteChartViewRequestAction;

export function deleteChartView(projectUniqueName: string, resources: string, id: number, viewId: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(deleteChartViewRequestActionCreator(viewId));

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
      .then((response) => stdDeleteHandleError(
        response,
        dispatch,
        deleteChartViewErrorActionCreator,
        'Chart views not found',
        'Failed to delete chart views',
        [viewId]))
      .then((json) => dispatch(deleteChartViewSuccessActionCreator(viewId)));
  };
}
