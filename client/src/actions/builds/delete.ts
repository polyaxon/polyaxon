import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getBuildUrlFromName, getProjectUrl } from '../../constants/utils';
import history from '../../history';
import { stdDeleteHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface DeleteBuildRequestAction extends Action {
  type: actionTypes.DELETE_BUILD_REQUEST;
  buildName: string;
}

export interface DeleteBuildSuccessAction extends Action {
  type: actionTypes.DELETE_BUILD_SUCCESS;
  buildName: string;
}

export interface DeleteBuildErrorAction extends Action {
  type: actionTypes.DELETE_BUILD_ERROR;
  statusCode: number;
  error: any;
  buildName: string;
}

export function deleteBuildRequestActionCreator(buildName: string): DeleteBuildRequestAction {
  return {
    type: actionTypes.DELETE_BUILD_REQUEST,
    buildName
  };
}

export function deleteBuildSuccessActionCreator(buildName: string): DeleteBuildSuccessAction {
  return {
    type: actionTypes.DELETE_BUILD_SUCCESS,
    buildName
  };
}

export function deleteBuildErrorActionCreator(statusCode: number,
                                              error: any,
                                              buildName: string): DeleteBuildErrorAction {
  return {
    type: actionTypes.DELETE_BUILD_ERROR,
    statusCode,
    error,
    buildName
  };
}

export type DeleteBuildAction =
  DeleteBuildRequestAction
  | DeleteBuildSuccessAction
  | DeleteBuildErrorAction;

export function deleteBuild(buildName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const buildUrl = getBuildUrlFromName(buildName, false);

    dispatch(deleteBuildRequestActionCreator(buildName));

    return fetch(
      `${BASE_API_URL}${buildUrl}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdDeleteHandleError(
        response,
        dispatch,
        deleteBuildErrorActionCreator,
        'Build not found',
        'Failed to delete build',
        [buildName]))
      .then(() => {
        const dispatched = dispatch(deleteBuildSuccessActionCreator(buildName));
        if (redirect) {
          const values = buildName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#builds');
        }
        return dispatched;
      });
  };
}
