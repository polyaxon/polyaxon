import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getProjectUrlFromName } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface SetProjectGitRequestAction extends Action {
  type: actionTypes.SET_PROJECT_GIT_REQUEST;
  projectName: string;
}

export interface SetProjectGitSuccessAction extends Action {
  type: actionTypes.SET_PROJECT_GIT_SUCCESS;
  projectName: string;
}

export interface SetProjectGitErrorAction extends Action {
  type: actionTypes.SET_PROJECT_GIT_ERROR;
  statusCode: number;
  error: any;
  projectName: string;
}

export function setProjectGitRequestActionCreator(projectName: string): SetProjectGitRequestAction {
  return {
    type: actionTypes.SET_PROJECT_GIT_REQUEST,
    projectName
  };
}

export function setProjectGitSuccessActionCreator(projectName: string): SetProjectGitSuccessAction {
  return {
    type: actionTypes.SET_PROJECT_GIT_SUCCESS,
    projectName,
  };
}

export function setProjectGitErrorActionCreator(statusCode: number,
                                                error: any,
                                                projectName: string): SetProjectGitErrorAction {
  return {
    type: actionTypes.SET_PROJECT_GIT_ERROR,
    statusCode,
    error,
    projectName
  };
}

export type SetProjectGitAction =
  SetProjectGitRequestAction
  | SetProjectGitSuccessAction
  | SetProjectGitErrorAction;

export function setProjectGit(projectName: string, updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const projectUrl = getProjectUrlFromName(projectName, false);

    dispatch(setProjectGitRequestActionCreator(projectName));

    return fetch(`${BASE_API_URL}/${projectUrl}/repo/external/`, {
      method: 'POST',
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
        setProjectGitErrorActionCreator,
        'Project not found',
        'Failed to set git repo on project',
        [projectName]))
      .then(() => dispatch(setProjectGitSuccessActionCreator(projectName)))
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(setProjectGitErrorActionCreator(response.status, value, projectName)));
        } else {
          return response.value;
        }
      });
  };
}
