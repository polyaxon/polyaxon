import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { BuildModel } from '../../models/build';
import { getBuildUniqueName, getBuildUrl } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface GetBuildRequestAction extends Action {
  type: actionTypes.GET_BUILD_REQUEST;
  buildName: string;
}

export interface GetBuildSuccessAction extends Action {
  type: actionTypes.GET_BUILD_SUCCESS;
  build: BuildModel;
  buildName: string;
}

export interface GetBuildErrorAction extends Action {
  type: actionTypes.GET_BUILD_ERROR;
  statusCode: number;
  error: any;
  buildName: string;
}

export function getBuildRequestActionCreator(buildName: string): GetBuildRequestAction {
  return {
    type: actionTypes.GET_BUILD_REQUEST,
    buildName
  };
}

export function getBuildSuccessActionCreator(build: BuildModel): GetBuildSuccessAction {
  return {
    type: actionTypes.GET_BUILD_SUCCESS,
    build,
    buildName: build.unique_name
  };
}

export function getBuildErrorActionCreator(statusCode: number,
                                           error: any,
                                           buildName: string): GetBuildErrorAction {
  return {
    type: actionTypes.GET_BUILD_ERROR,
    statusCode,
    error,
    buildName
  };
}

export type GetBuildAction =
  GetBuildRequestAction
  | GetBuildSuccessAction
  | GetBuildErrorAction;

export function fetchBuild(user: string, projectName: string, buildId: number | string): any {
  return (dispatch: any, getState: any) => {
    const buildName = getBuildUniqueName(user, projectName, buildId);
    const buildUrl = getBuildUrl(user, projectName, buildId, false);

    dispatch(getBuildRequestActionCreator(buildName));

    return fetch(
      `${BASE_API_URL}${buildUrl}`, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        getBuildErrorActionCreator,
        'Build not found',
        'Failed to fetch build',
        [buildName]))
      .then((response) => response.json())
      .then((json) => dispatch(getBuildSuccessActionCreator(json)));
  };
}
