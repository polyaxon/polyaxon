import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { ProjectModel } from '../../models/project';
import { getProjectUrlFromName } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface UpdateProjectRequestAction extends Action {
  type: actionTypes.UPDATE_PROJECT_REQUEST;
  projectName: string;
}

export interface UpdateProjectSuccessAction extends Action {
  type: actionTypes.UPDATE_PROJECT_SUCCESS;
  project: ProjectModel;
  projectName: string;
}

export interface UpdateProjectErrorAction extends Action {
  type: actionTypes.UPDATE_PROJECT_ERROR;
  statusCode: number;
  error: any;
  projectName: string;
}

export function updateProjectRequestActionCreator(projectName: string): UpdateProjectRequestAction {
  return {
    type: actionTypes.UPDATE_PROJECT_REQUEST,
    projectName
  };
}

export function updateProjectSuccessActionCreator(project: ProjectModel): UpdateProjectSuccessAction {
  return {
    type: actionTypes.UPDATE_PROJECT_SUCCESS,
    project,
    projectName: project.unique_name,
  };
}

export function updateProjectErrorActionCreator(statusCode: number,
                                                error: any,
                                                projectName: string): UpdateProjectErrorAction {
  return {
    type: actionTypes.UPDATE_PROJECT_ERROR,
    statusCode,
    error,
    projectName
  };
}

export type UpdateProjectAction =
  UpdateProjectRequestAction
  | UpdateProjectSuccessAction
  | UpdateProjectErrorAction;

export function updateProject(projectName: string, updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const projectUrl = getProjectUrlFromName(projectName, false);

    dispatch(updateProjectRequestActionCreator(projectName));

    return fetch(`${BASE_API_URL}/${projectUrl}`, {
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
        updateProjectErrorActionCreator,
        'Project not found',
        'Failed to project',
        [projectName]))
      .then((response) => response.json())
      .then((json) => dispatch(updateProjectSuccessActionCreator(json)))
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(updateProjectErrorActionCreator(response.status, value, projectName)));
        } else {
          return response.value;
        }
      });
  };
}
