import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getCatalogEntityUrl, getCatalogUrl } from '../../urls/utils';
import { stdDeleteHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface DeleteK8SResourceRequestAction extends Action {
  type: actionTypes.DELETE_K8S_RESOURCE_REQUEST;
  name: string;
}

export interface DeleteK8SResourceSuccessAction extends Action {
  type: actionTypes.DELETE_K8S_RESOURCE_SUCCESS;
  name: string;
}

export interface DeleteK8SResourceErrorAction extends Action {
  type: actionTypes.DELETE_K8S_RESOURCE_ERROR;
  statusCode: number;
  error: any;
  name: string;
}

export function deleteK8SResourceRequestActionCreator(name: string): DeleteK8SResourceRequestAction {
  return {
    type: actionTypes.DELETE_K8S_RESOURCE_REQUEST,
    name,
  };
}

export function deleteK8SResourceSuccessActionCreator(name: string): DeleteK8SResourceSuccessAction {
  return {
    type: actionTypes.DELETE_K8S_RESOURCE_SUCCESS,
    name,
  };
}

export function deleteK8SResourceErrorActionCreator(statusCode: number,
                                                    error: any,
                                                    name: string): DeleteK8SResourceErrorAction {
  return {
    type: actionTypes.DELETE_K8S_RESOURCE_ERROR,
    statusCode,
    error,
    name,
  };
}

export type DeleteK8SResourceAction =
  DeleteK8SResourceRequestAction
  | DeleteK8SResourceSuccessAction
  | DeleteK8SResourceErrorAction;

export function deleteK8SResource(resourceType: string,
                                  owner: string,
                                  name: string,
                                  redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const k8sResourceUrl = getCatalogEntityUrl(resourceType, name, owner, false);

    dispatch(deleteK8SResourceRequestActionCreator(name));

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
        deleteK8SResourceErrorActionCreator,
        'K8SResource not found',
        `Failed to delete the ${resourceType} entity`,
        [name]))
      .then(() => {
        const dispatched = dispatch(deleteK8SResourceSuccessActionCreator(name));
        if (redirect) {
          history.push(getCatalogUrl(resourceType, owner, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(deleteK8SResourceErrorActionCreator(response.status, value, name)));
        } else {
          return dispatch(deleteK8SResourceErrorActionCreator(response.status, response.value, name));
        }
      });
  };
}
