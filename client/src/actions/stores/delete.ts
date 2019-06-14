import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getCatalogEntityUrl, getCatalogUrl } from '../../urls/utils';
import { stdDeleteHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface DeleteStoreRequestAction extends Action {
  type: actionTypes.DELETE_STORE_REQUEST;
  name: string;
}

export interface DeleteStoreSuccessAction extends Action {
  type: actionTypes.DELETE_STORE_SUCCESS;
  name: string;
}

export interface DeleteStoreErrorAction extends Action {
  type: actionTypes.DELETE_STORE_ERROR;
  statusCode: number;
  error: any;
  name: string;
}

export function deleteStoreRequestActionCreator(name: string): DeleteStoreRequestAction {
  return {
    type: actionTypes.DELETE_STORE_REQUEST,
    name,
  };
}

export function deleteStoreSuccessActionCreator(name: string): DeleteStoreSuccessAction {
  return {
    type: actionTypes.DELETE_STORE_SUCCESS,
    name,
  };
}

export function deleteStoreErrorActionCreator(statusCode: number,
                                              error: any,
                                              name: string): DeleteStoreErrorAction {
  return {
    type: actionTypes.DELETE_STORE_ERROR,
    statusCode,
    error,
    name,
  };
}

export type DeleteStoreAction =
  DeleteStoreRequestAction
  | DeleteStoreSuccessAction
  | DeleteStoreErrorAction;

export function deleteStore(resourceType: string,
                            owner: string,
                            name: string,
                            redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const k8sResourceUrl = getCatalogEntityUrl(resourceType, name, owner, false);

    dispatch(deleteStoreRequestActionCreator(name));

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
        deleteStoreErrorActionCreator,
        'Store not found',
        `Failed to delete the ${resourceType} entity`,
        [name]))
      .then(() => {
        const dispatched = dispatch(deleteStoreSuccessActionCreator(name));
        if (redirect) {
          history.push(getCatalogUrl(resourceType, owner, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(deleteStoreErrorActionCreator(response.status, value, name)));
        } else {
          return dispatch(deleteStoreErrorActionCreator(response.status, response.value, name));
        }
      });
  };
}
