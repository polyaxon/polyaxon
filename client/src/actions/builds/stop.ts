import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getBuildUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface StopBuildRequestAction extends Action {
  type: actionTypes.STOP_BUILD_REQUEST;
  buildName: string;
}

export interface StopBuildSuccessAction extends Action {
  type: actionTypes.STOP_BUILD_SUCCESS;
  buildName: string;
}

export interface StopBuildErrorAction extends Action {
  type: actionTypes.STOP_BUILD_ERROR;
  statusCode: number;
  error: any;
  buildName: string;
}

export function stopBuildRequestActionCreator(buildName: string): StopBuildRequestAction {
  return {
    type: actionTypes.STOP_BUILD_REQUEST,
    buildName
  };
}

export function stopBuildSuccessActionCreator(buildName: string): StopBuildSuccessAction {
  return {
    type: actionTypes.STOP_BUILD_SUCCESS,
    buildName
  };
}

export function stopBuildErrorActionCreator(statusCode: number,
                                            error: any,
                                            buildName: string): StopBuildErrorAction {
  return {
    type: actionTypes.STOP_BUILD_ERROR,
    statusCode,
    error,
    buildName
  };
}

export type StopBuildAction =
  StopBuildRequestAction
  | StopBuildSuccessAction
  | StopBuildErrorAction;

export function stopBuild(buildName: string): any {
  return (dispatch: any, getState: any) => {
    const buildUrl = getBuildUrlFromName(buildName, false);

    dispatch(stopBuildRequestActionCreator(buildName));

    return fetch(
      `${BASE_API_URL}${buildUrl}/stop`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        stopBuildErrorActionCreator,
        'Build not found',
        'Failed to stop build',
        [buildName]))
      .then(() => dispatch(stopBuildSuccessActionCreator(buildName)));
  };
}
