import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { AccessModel } from '../../models/access';
import { getCatalogEntityUrl, getCatalogUrl } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getAccessSuccessActionCreator } from './get';

export interface CreateAccessRequestAction extends Action {
  type: actionTypes.CREATE_ACCESS_REQUEST;
}

export interface CreateAccessSuccessAction extends Action {
  type: actionTypes.CREATE_ACCESS_SUCCESS;
}

export interface CreateAccessErrorAction extends Action {
  type: actionTypes.CREATE_ACCESS_ERROR;
  statusCode: number;
  error: any;
}

export function createAccessRequestActionCreator(): CreateAccessRequestAction {
  return {
    type: actionTypes.CREATE_ACCESS_REQUEST,
  };
}

export function createAccessSuccessActionCreator(): CreateAccessSuccessAction {
  return {
    type: actionTypes.CREATE_ACCESS_SUCCESS,
  };
}

export function createAccessErrorActionCreator(statusCode: number, error: any): CreateAccessErrorAction {
  return {
    type: actionTypes.CREATE_ACCESS_ERROR,
    statusCode,
    error
  };
}

export type CreateAccessAction =
  CreateAccessRequestAction
  | CreateAccessSuccessAction
  | CreateAccessErrorAction;

export function createAccess(resourceType: string,
                            access: AccessModel,
                            owner?: string,
                            redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {

    dispatch(createAccessRequestActionCreator());

    const accessUrl = getCatalogUrl(resourceType, owner, false);
    return fetch(`${BASE_API_URL}${accessUrl}`, {
      method: 'POST',
      body: JSON.stringify(access),
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
        createAccessErrorActionCreator,
        'Not found',
        `Failed to create a new entity in ${access}`))
      .then((response) => response.json())
      .then((json) => {
        dispatch(createAccessSuccessActionCreator());
        const dispatched = dispatch(getAccessSuccessActionCreator(json));
        if (redirect) {
          history.push(getCatalogEntityUrl(resourceType, json.name, owner, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(createAccessErrorActionCreator(response.status, value)));
        } else {
          return dispatch(createAccessErrorActionCreator(response.status, response.value));
        }
      });
  };
}
