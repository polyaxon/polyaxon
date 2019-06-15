import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getCatalogEntityUrl, getCatalogUrl } from '../../urls/utils';
import { stdDeleteHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface DeleteAccessRequestAction extends Action {
  type: actionTypes.DELETE_ACCESS_REQUEST;
  name: string;
}

export interface DeleteAccessSuccessAction extends Action {
  type: actionTypes.DELETE_ACCESS_SUCCESS;
  name: string;
}

export interface DeleteAccessErrorAction extends Action {
  type: actionTypes.DELETE_ACCESS_ERROR;
  statusCode: number;
  error: any;
  name: string;
}

export function deleteAccessRequestActionCreator(name: string): DeleteAccessRequestAction {
  return {
    type: actionTypes.DELETE_ACCESS_REQUEST,
    name,
  };
}

export function deleteAccessSuccessActionCreator(name: string): DeleteAccessSuccessAction {
  return {
    type: actionTypes.DELETE_ACCESS_SUCCESS,
    name,
  };
}

export function deleteAccessErrorActionCreator(statusCode: number,
                                               error: any,
                                               name: string): DeleteAccessErrorAction {
  return {
    type: actionTypes.DELETE_ACCESS_ERROR,
    statusCode,
    error,
    name,
  };
}

export type DeleteAccessAction =
  DeleteAccessRequestAction
  | DeleteAccessSuccessAction
  | DeleteAccessErrorAction;

export function deleteAccess(resourceType: string,
                             owner: string,
                             name: string,
                             redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const k8sResourceUrl = getCatalogEntityUrl(resourceType, name, owner, false);

    dispatch(deleteAccessRequestActionCreator(name));

    return fetch(`${BASE_API_URL}${k8sResourceUrl}`, {
      method: 'DELETE',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdDeleteHandleError(
        response,
        dispatch,
        deleteAccessErrorActionCreator,
        'Access not found',
        `Failed to delete the ${resourceType} entity`,
        [name]))
      .then(() => {
        const dispatched = dispatch(deleteAccessSuccessActionCreator(name));
        if (redirect) {
          history.push(getCatalogUrl(resourceType, owner, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(deleteAccessErrorActionCreator(response.status, value, name)));
        } else {
          return dispatch(deleteAccessErrorActionCreator(response.status, response.value, name));
        }
      });
  };
}
