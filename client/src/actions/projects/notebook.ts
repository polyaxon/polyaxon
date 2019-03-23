import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getProjectUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface StartProjectNotebookRequestAction extends Action {
  type: actionTypes.START_PROJECT_NOTEBOOK_REQUEST;
  projectName: string;
}

export interface StartProjectNotebookSuccessAction extends Action {
  type: actionTypes.START_PROJECT_NOTEBOOK_SUCCESS;
  projectName: string;
}

export interface StartProjectNotebookErrorAction extends Action {
  type: actionTypes.START_PROJECT_NOTEBOOK_ERROR;
  statusCode: number;
  error: any;
  projectName: string;
}

export function startProjectNotebookRequestActionCreator(projectName: string): StartProjectNotebookRequestAction {
  return {
    type: actionTypes.START_PROJECT_NOTEBOOK_REQUEST,
    projectName
  };
}

export function startProjectNotebookSuccessActionCreator(projectName: string): StartProjectNotebookSuccessAction {
  return {
    type: actionTypes.START_PROJECT_NOTEBOOK_SUCCESS,
    projectName
  };
}

export function startProjectNotebookErrorActionCreator(statusCode: number,
                                                       error: any,
                                                       projectName: string): StartProjectNotebookErrorAction {
  return {
    type: actionTypes.START_PROJECT_NOTEBOOK_ERROR,
    statusCode,
    error,
    projectName
  };
}

export interface StopProjectNotebookRequestAction extends Action {
  type: actionTypes.STOP_PROJECT_NOTEBOOK_REQUEST;
  projectName: string;
}

export interface StopProjectNotebookSuccessAction extends Action {
  type: actionTypes.STOP_PROJECT_NOTEBOOK_SUCCESS;
  projectName: string;
}

export interface StopProjectNotebookErrorAction extends Action {
  type: actionTypes.STOP_PROJECT_NOTEBOOK_ERROR;
  statusCode: number;
  error: any;
  projectName: string;
}

export function stopProjectNotebookRequestActionCreator(projectName: string): StopProjectNotebookRequestAction {
  return {
    type: actionTypes.STOP_PROJECT_NOTEBOOK_REQUEST,
    projectName
  };
}

export function stopProjectNotebookSuccessActionCreator(projectName: string): StopProjectNotebookSuccessAction {
  return {
    type: actionTypes.STOP_PROJECT_NOTEBOOK_SUCCESS,
    projectName
  };
}

export function stopProjectNotebookErrorActionCreator(statusCode: number,
                                                      error: any,
                                                      projectName: string): StopProjectNotebookErrorAction {
  return {
    type: actionTypes.STOP_PROJECT_NOTEBOOK_ERROR,
    statusCode,
    error,
    projectName
  };
}

export type NotebookProjectAction =
  StartProjectNotebookRequestAction
  | StartProjectNotebookSuccessAction
  | StartProjectNotebookErrorAction
  | StopProjectNotebookRequestAction
  | StopProjectNotebookSuccessAction
  | StopProjectNotebookErrorAction;

export function startNotebook(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const projectUrl = getProjectUrlFromName(projectName, false);

    dispatch(startProjectNotebookRequestActionCreator(projectName));

    return fetch(`${BASE_API_URL}${projectUrl}/notebook/start`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        startProjectNotebookErrorActionCreator,
        'Project not found',
        'Failed to start notebook for project',
        [projectName]))
      .then(() => {
        return dispatch(startProjectNotebookSuccessActionCreator(projectName));
      });
  };
}

export function stopNotebook(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const projectUrl = getProjectUrlFromName(projectName, false);

    dispatch(stopProjectNotebookRequestActionCreator(projectName));

    return fetch(`${BASE_API_URL}${projectUrl}/notebook/stop`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        stopProjectNotebookErrorActionCreator,
        'Project not found',
        'Failed to stop notebook for project',
        [projectName]))
      .then(() => {
        return dispatch(stopProjectNotebookSuccessActionCreator(projectName));
      });
  };
}
