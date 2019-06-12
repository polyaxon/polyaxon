import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getBuildUrlFromName } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface RestoreBuildRequestAction extends Action {
  type: actionTypes.RESTORE_BUILD_REQUEST;
  buildName: string;
}

export interface RestoreBuildSuccessAction extends Action {
  type: actionTypes.RESTORE_BUILD_SUCCESS;
  buildName: string;
}

export interface RestoreBuildErrorAction extends Action {
  type: actionTypes.RESTORE_BUILD_ERROR;
  statusCode: number;
  error: any;
  buildName: string;
}

export function restoreBuildRequestActionCreator(buildName: string): RestoreBuildRequestAction {
  return {
    type: actionTypes.RESTORE_BUILD_REQUEST,
    buildName
  };
}

export function restoreBuildSuccessActionCreator(buildName: string): RestoreBuildSuccessAction {
  return {
    type: actionTypes.RESTORE_BUILD_SUCCESS,
    buildName
  };
}

export function restoreBuildErrorActionCreator(statusCode: number,
                                               error: any,
                                               buildName: string): RestoreBuildErrorAction {
  return {
    type: actionTypes.RESTORE_BUILD_ERROR,
    statusCode,
    error,
    buildName
  };
}

export type RestoreBuildAction =
  RestoreBuildRequestAction
  | RestoreBuildSuccessAction
  | RestoreBuildErrorAction;

export function restoreBuild(buildName: string): any {
  return (dispatch: any, getState: any) => {
    const buildUrl = getBuildUrlFromName(buildName, false);

    dispatch(restoreBuildRequestActionCreator(buildName));

    return fetch(
      `${BASE_API_URL}${buildUrl}/restore`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        restoreBuildErrorActionCreator,
        'Build not found',
        'Failed to restore build',
        [buildName]))
      .then(() => dispatch(restoreBuildSuccessActionCreator(buildName)));
  };
}
