import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getProjectUrlFromName, getUserUrl } from '../../constants/utils';
import history from '../../history';
import { stdDeleteHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface DeleteProjectRequestAction extends Action {
  type: actionTypes.DELETE_PROJECT_REQUEST;
  projectName: string;
}

export interface DeleteProjectSuccessAction extends Action {
  type: actionTypes.DELETE_PROJECT_SUCCESS;
  projectName: string;
}

export interface DeleteProjectErrorAction extends Action {
  type: actionTypes.DELETE_PROJECT_ERROR;
  statusCode: number;
  error: any;
  projectName: string;
}

export function deleteProjectRequestActionCreator(projectName: string): DeleteProjectRequestAction {
  return {
    type: actionTypes.DELETE_PROJECT_REQUEST,
    projectName
  };
}

export function deleteProjectSuccessActionCreator(projectName: string): DeleteProjectSuccessAction {
  return {
    type: actionTypes.DELETE_PROJECT_SUCCESS,
    projectName
  };
}

export function deleteProjectErrorActionCreator(statusCode: number,
                                                error: any,
                                                projectName: string): DeleteProjectErrorAction {
  return {
    type: actionTypes.DELETE_PROJECT_ERROR,
    statusCode,
    error,
    projectName
  };
}

export type DeleteProjectAction =
  DeleteProjectRequestAction
  | DeleteProjectSuccessAction
  | DeleteProjectErrorAction;

export function deleteProject(projectName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const projectUrl = getProjectUrlFromName(projectName, false);

    dispatch(deleteProjectRequestActionCreator(projectName));

    return fetch(`${BASE_API_URL}${projectUrl}`, {
      method: 'DELETE',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdDeleteHandleError(
        response,
        dispatch,
        deleteProjectErrorActionCreator,
        'Project not found',
        'Failed to delete project',
        [projectName]))
      .then(() => {
        const dispatched = dispatch(deleteProjectSuccessActionCreator(projectName));
        if (redirect) {
          const values = projectName.split('.');
          history.push(getUserUrl(values[0], true));
        }
        return dispatched;
      });
  };
}
