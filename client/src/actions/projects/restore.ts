import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getProjectUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface RestoreProjectRequestAction extends Action {
  type: actionTypes.RESTORE_PROJECT_REQUEST;
  projectName: string;
}

export interface RestoreProjectSuccessAction extends Action {
  type: actionTypes.RESTORE_PROJECT_SUCCESS;
  projectName: string;
}

export interface RestoreProjectErrorAction extends Action {
  type: actionTypes.RESTORE_PROJECT_ERROR;
  statusCode: number;
  error: any;
  projectName: string;
}

export function restoreProjectRequestActionCreator(projectName: string): RestoreProjectRequestAction {
  return {
    type: actionTypes.RESTORE_PROJECT_REQUEST,
    projectName
  };
}

export function restoreProjectSuccessActionCreator(projectName: string): RestoreProjectSuccessAction {
  return {
    type: actionTypes.RESTORE_PROJECT_SUCCESS,
    projectName
  };
}

export function restoreProjectErrorActionCreator(statusCode: number,
                                                 error: any,
                                                 projectName: string): RestoreProjectErrorAction {
  return {
    type: actionTypes.RESTORE_PROJECT_ERROR,
    statusCode,
    error,
    projectName
  };
}

export type RestoreProjectAction =
  RestoreProjectRequestAction
  | RestoreProjectSuccessAction
  | RestoreProjectErrorAction;

export function restoreProject(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const projectUrl = getProjectUrlFromName(projectName, false);

    dispatch(restoreProjectRequestActionCreator(projectName));

    return fetch(`${BASE_API_URL}${projectUrl}/restore`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        restoreProjectErrorActionCreator,
        'Project not found',
        'Failed to restore project',
        [projectName]))
      .then(() => dispatch(restoreProjectSuccessActionCreator(projectName)));
  };
}
