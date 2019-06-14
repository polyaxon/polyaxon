import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { NotebookModel } from '../../models/notebook';
import {
  getNotebookApiUrlFromName,
  getProjectUniqueName,
  getProjectUrl,
  getProjectUrlFromName
} from '../../urls/utils';
import { getNotebookSuccessActionCreator } from '../notebooks';
import { stdCreateHandleError, stdHandleError } from '../utils';
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

export function startNotebook(user: string,
                              projectName: string,
                              notebook: NotebookModel,
                              redirect: boolean): any {
  return (dispatch: any, getState: any) => {
    const projectUniqueName = getProjectUniqueName(user, projectName);
    const projectUrl = getProjectUrl(user, projectName, false);

    dispatch(startProjectNotebookRequestActionCreator(projectUniqueName));

    return fetch(`${BASE_API_URL}${projectUrl}/notebook/start`, {
      method: 'POST',
      body: JSON.stringify(notebook),
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdCreateHandleError(
        response,
        dispatch,
        startProjectNotebookErrorActionCreator,
        'Project not found',
        'Failed to start notebook for project',
        [projectName]))
      .then((response) => response.json())
      .then((json) => {
        dispatch(startProjectNotebookSuccessActionCreator(projectUniqueName));
        const dispatched = dispatch(getNotebookSuccessActionCreator(json));
        if (redirect) {
          history.push(getNotebookApiUrlFromName( json.unique_name, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(startProjectNotebookErrorActionCreator(
              response.status, value, projectUniqueName)));
        } else {
          return dispatch(startProjectNotebookErrorActionCreator(
              response.status, response.value, projectUniqueName));
        }
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
