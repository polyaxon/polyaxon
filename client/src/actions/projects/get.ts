import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { ProjectModel } from '../../models/project';
import { getProjectUniqueName, getProjectUrl } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface GetProjectRequestAction extends Action {
  type: actionTypes.GET_PROJECT_REQUEST;
  projectName: string;
}

export interface GetProjectSuccessAction extends Action {
  type: actionTypes.GET_PROJECT_SUCCESS;
  project: ProjectModel;
  projectName: string;
}

export interface GetProjectErrorAction extends Action {
  type: actionTypes.GET_PROJECT_ERROR;
  statusCode: number;
  error: any;
  projectName: string;
}

export function getProjectRequestActionCreator(projectName: string): GetProjectRequestAction {
  return {
    type: actionTypes.GET_PROJECT_REQUEST,
    projectName
  };
}

export function getProjectSuccessActionCreator(project: ProjectModel): GetProjectSuccessAction {
  return {
    type: actionTypes.GET_PROJECT_SUCCESS,
    project,
    projectName: project.unique_name
  };
}

export function getProjectErrorActionCreator(statusCode: number,
                                             error: any,
                                             projectName: string): GetProjectErrorAction {
  return {
    type: actionTypes.GET_PROJECT_ERROR,
    statusCode,
    error,
    projectName
  };
}

export type GetProjectAction =
  GetProjectRequestAction
  | GetProjectSuccessAction
  | GetProjectErrorAction;

export function fetchProject(user: string, projectName: string): any {
  return (dispatch: any, getState: any) => {
    const projectUrl = getProjectUrl(user, projectName, false);
    const projectUniqueName = getProjectUniqueName(user, projectName);

    dispatch(getProjectRequestActionCreator(projectUniqueName));

    return fetch(`${BASE_API_URL}${projectUrl}`, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        getProjectErrorActionCreator,
        'Project not found',
        'Failed to fetch project',
        [projectUniqueName]))
      .then((response) => response.json())
      .then((json) => dispatch(getProjectSuccessActionCreator(json)));
  };
}
