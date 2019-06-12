import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getBuildUrlFromName } from '../../urls/utils';
import { BuildModel } from '../../models/build';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface UpdateBuildRequestAction extends Action {
  type: actionTypes.UPDATE_BUILD_REQUEST;
  buildName: string;
}

export interface UpdateBuildSuccessAction extends Action {
  type: actionTypes.UPDATE_BUILD_SUCCESS;
  build: BuildModel;
  buildName: string;
}

export interface UpdateBuildErrorAction extends Action {
  type: actionTypes.UPDATE_BUILD_ERROR;
  statusCode: number;
  error: any;
  buildName: string;
}

export function updateBuildRequestActionCreator(buildName: string): UpdateBuildRequestAction {
  return {
    type: actionTypes.UPDATE_BUILD_REQUEST,
    buildName
  };
}

export function updateBuildSuccessActionCreator(build: BuildModel): UpdateBuildSuccessAction {
  return {
    type: actionTypes.UPDATE_BUILD_SUCCESS,
    build,
    buildName: build.unique_name
  };
}

export function updateBuildErrorActionCreator(statusCode: number,
                                              error: any,
                                              buildName: string): UpdateBuildErrorAction {
  return {
    type: actionTypes.UPDATE_BUILD_ERROR,
    statusCode,
    error,
    buildName
  };
}

export type UpdateBuildAction =
  UpdateBuildRequestAction
  | UpdateBuildSuccessAction
  | UpdateBuildErrorAction;

export function updateBuild(buildName: string, updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const buildUrl = getBuildUrlFromName(buildName, false);

    dispatch(updateBuildRequestActionCreator(buildName));

    return fetch(
      `${BASE_API_URL}${buildUrl}`, {
        method: 'PATCH',
        body: JSON.stringify(updateDict),
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
        updateBuildErrorActionCreator,
        'Build not found',
        'Failed to update build',
        [buildName]))
      .then((response) => response.json())
      .then((json) => dispatch(updateBuildSuccessActionCreator(json)))
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(updateBuildErrorActionCreator(response.status, value, buildName)));
        } else {
          return response.value;
        }
      });
  };
}
