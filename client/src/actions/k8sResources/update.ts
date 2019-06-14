import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { K8SResourceModel } from '../../models/k8sResource';
import { getCatalogEntityUrl } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface UpdateK8SResourceRequestAction extends Action {
  type: actionTypes.UPDATE_K8S_RESOURCE_REQUEST;
  name: string;
}

export interface UpdateK8SResourceSuccessAction extends Action {
  type: actionTypes.UPDATE_K8S_RESOURCE_SUCCESS;
  k8sResource: K8SResourceModel;
  name: string;
}

export interface UpdateK8SResourceErrorAction extends Action {
  type: actionTypes.UPDATE_K8S_RESOURCE_ERROR;
  statusCode: number;
  error: any;
  name: string;
}

export function updateK8SResourceRequestActionCreator(name: string): UpdateK8SResourceRequestAction {
  return {
    type: actionTypes.UPDATE_K8S_RESOURCE_REQUEST,
    name
  };
}

export function updateK8SResourceSuccessActionCreator(k8sResource: K8SResourceModel,
                                                      name: string): UpdateK8SResourceSuccessAction {
  return {
    type: actionTypes.UPDATE_K8S_RESOURCE_SUCCESS,
    k8sResource,
    name
  };
}

export function updateK8SResourceErrorActionCreator(statusCode: number,
                                                    error: any,
                                                    name: string): UpdateK8SResourceErrorAction {
  return {
    type: actionTypes.UPDATE_K8S_RESOURCE_ERROR,
    statusCode,
    error,
    name
  };
}

export type UpdateK8SResourceAction =
  UpdateK8SResourceRequestAction
  | UpdateK8SResourceSuccessAction
  | UpdateK8SResourceErrorAction;

export function updateK8SResource(resourceType: string,
                                  owner: string,
                                  name: string,
                                  updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const k8sResourceUrl = getCatalogEntityUrl(resourceType, name, owner, false);

    dispatch(updateK8SResourceRequestActionCreator(name));

    return fetch(`${BASE_API_URL}${k8sResourceUrl}`, {
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
        updateK8SResourceErrorActionCreator,
        'K8SResource not found',
        `Failed to update ${resourceType} entity`,
        [name]))
      .then((response) => response.json())
      .then((json) => dispatch(updateK8SResourceSuccessActionCreator(json, name)))
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(updateK8SResourceErrorActionCreator(response.status, value, name)));
        } else {
          return dispatch(updateK8SResourceErrorActionCreator(response.status, response.value, name));
        }
      });
  };
}
