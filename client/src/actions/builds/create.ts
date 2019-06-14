import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { BuildModel } from '../../models/build';
import { getBuildUrlFromName } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getBuildSuccessActionCreator } from './get';

export interface CreateBuildRequestAction extends Action {
  type: actionTypes.CREATE_BUILD_REQUEST;
}

export interface CreateBuildSuccessAction extends Action {
  type: actionTypes.CREATE_BUILD_SUCCESS;
}

export interface CreateBuildErrorAction extends Action {
  type: actionTypes.CREATE_BUILD_ERROR;
  statusCode: number;
  error: any;
}

export function createBuildRequestActionCreator(): CreateBuildRequestAction {
  return {
    type: actionTypes.CREATE_BUILD_REQUEST,
  };
}

export function createBuildSuccessActionCreator(): CreateBuildSuccessAction {
  return {
    type: actionTypes.CREATE_BUILD_SUCCESS,
  };
}

export function createBuildErrorActionCreator(statusCode: number, error: any): CreateBuildErrorAction {
  return {
    type: actionTypes.CREATE_BUILD_ERROR,
    statusCode,
    error
  };
}

export type CreateBuildAction =
  CreateBuildRequestAction
  | CreateBuildSuccessAction
  | CreateBuildErrorAction;

export function createBuild(user: string,
                            projectName: string,
                            build: BuildModel,
                            redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    dispatch(createBuildRequestActionCreator());

    return fetch(`${BASE_API_URL}/${user}/${projectName}/builds`, {
      method: 'POST',
      body: JSON.stringify(build),
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
        createBuildErrorActionCreator,
        'Not found',
        'Failed to create build'))
      .then((response) => response.json())
      .then((json) => {
        dispatch(createBuildSuccessActionCreator());
        const dispatched = dispatch(getBuildSuccessActionCreator(json));
        if (redirect) {
          history.push(getBuildUrlFromName(json.unique_name, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(createBuildErrorActionCreator(response.status, value)));
        } else {
          return dispatch(createBuildErrorActionCreator(response.status, response.value));
        }
      });
  };
}
