import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { ProjectModel } from '../../models/project';
import { getProjectUrlFromName } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getProjectSuccessActionCreator } from './get';

export interface CreateProjectRequestAction extends Action {
  type: actionTypes.CREATE_PROJECT_REQUEST;
}

export interface CreateProjectSuccessAction extends Action {
  type: actionTypes.CREATE_PROJECT_SUCCESS;
}

export interface CreateProjectErrorAction extends Action {
  type: actionTypes.CREATE_PROJECT_ERROR;
  statusCode: number;
  error: any;
}

export function createProjectRequestActionCreator(): CreateProjectRequestAction {
  return {
    type: actionTypes.CREATE_PROJECT_REQUEST,
  };
}

export function createProjectSuccessActionCreator(): CreateProjectSuccessAction {
  return {
    type: actionTypes.CREATE_PROJECT_SUCCESS,
  };
}

export function createProjectErrorActionCreator(statusCode: number, error: any): CreateProjectErrorAction {
  return {
    type: actionTypes.CREATE_PROJECT_ERROR,
    statusCode,
    error,
  };
}

export type CreateProjectAction =
  CreateProjectRequestAction
  | CreateProjectSuccessAction
  | CreateProjectErrorAction;

export function createProject(project: ProjectModel, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {

    dispatch(createProjectRequestActionCreator());

    return fetch(`${BASE_API_URL}/projects`, {
      method: 'POST',
      body: JSON.stringify(project),
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
        createProjectErrorActionCreator,
        'Not found',
        'Failed to create project'))
      .then((response) => response.json())
      .then((json) => {
        dispatch(createProjectSuccessActionCreator());
        const dispatched = dispatch(getProjectSuccessActionCreator(json));
        if (redirect) {
          history.push(getProjectUrlFromName(json.unique_name, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(createProjectErrorActionCreator(response.status, value)));
        } else {
          return dispatch(createProjectErrorActionCreator(response.status, response.value));
        }
      });
  };
}
