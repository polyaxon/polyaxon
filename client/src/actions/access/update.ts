import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { AccessModel } from '../../models/access';
import { getCatalogEntityUrl } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface UpdateAccessRequestAction extends Action {
  type: actionTypes.UPDATE_ACCESS_REQUEST;
  name: string;
}

export interface UpdateAccessSuccessAction extends Action {
  type: actionTypes.UPDATE_ACCESS_SUCCESS;
  access: AccessModel;
  name: string;
}

export interface UpdateAccessErrorAction extends Action {
  type: actionTypes.UPDATE_ACCESS_ERROR;
  statusCode: number;
  error: any;
  name: string;
}

export function updateAccessRequestActionCreator(name: string): UpdateAccessRequestAction {
  return {
    type: actionTypes.UPDATE_ACCESS_REQUEST,
    name
  };
}

export function updateAccessSuccessActionCreator(access: AccessModel, name: string): UpdateAccessSuccessAction {
  return {
    type: actionTypes.UPDATE_ACCESS_SUCCESS,
    access,
    name
  };
}

export function updateAccessErrorActionCreator(statusCode: number,
                                               error: any,
                                               name: string): UpdateAccessErrorAction {
  return {
    type: actionTypes.UPDATE_ACCESS_ERROR,
    statusCode,
    error,
    name
  };
}

export type UpdateAccessAction =
  UpdateAccessRequestAction
  | UpdateAccessSuccessAction
  | UpdateAccessErrorAction;

export function updateAccess(resourceType: string,
                             owner: string,
                             name: string,
                             updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const accessUrl = getCatalogEntityUrl(resourceType, name, owner, false);

    dispatch(updateAccessRequestActionCreator(name));

    return fetch(`${BASE_API_URL}${accessUrl}`, {
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
        updateAccessErrorActionCreator,
        'Access not found',
        `Failed to update ${resourceType} entity`,
        [name]))
      .then((response) => response.json())
      .then((json) => dispatch(updateAccessSuccessActionCreator(json, name)))
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(updateAccessErrorActionCreator(response.status, value, name)));
        } else {
          return dispatch(updateAccessErrorActionCreator(response.status, response.value, name));
        }
      });
  };
}
