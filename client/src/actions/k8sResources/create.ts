import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { K8SResourceModel } from '../../models/k8sResource';
import { getCatalogEntityUrl, getCatalogUrl } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getK8SResourceSuccessActionCreator } from './get';

export interface CreateK8SResourceRequestAction extends Action {
  type: actionTypes.CREATE_K8S_RESOURCE_REQUEST;
}

export interface CreateK8SResourceSuccessAction extends Action {
  type: actionTypes.CREATE_K8S_RESOURCE_SUCCESS;
}

export interface CreateK8SResourceErrorAction extends Action {
  type: actionTypes.CREATE_K8S_RESOURCE_ERROR;
  statusCode: number;
  error: any;
}

export function createK8SResourceRequestActionCreator(): CreateK8SResourceRequestAction {
  return {
    type: actionTypes.CREATE_K8S_RESOURCE_REQUEST,
  };
}

export function createK8SResourceSuccessActionCreator(): CreateK8SResourceSuccessAction {
  return {
    type: actionTypes.CREATE_K8S_RESOURCE_SUCCESS,
  };
}

export function createK8SResourceErrorActionCreator(statusCode: number, error: any): CreateK8SResourceErrorAction {
  return {
    type: actionTypes.CREATE_K8S_RESOURCE_ERROR,
    statusCode,
    error
  };
}

export type CreateK8SResourceAction =
  CreateK8SResourceRequestAction
  | CreateK8SResourceSuccessAction
  | CreateK8SResourceErrorAction;

export function createK8SResource(resourceType: string,
                                  k8sResource: K8SResourceModel,
                                  owner?: string,
                                  redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {

    dispatch(createK8SResourceRequestActionCreator());

    const k8sResourceUrl = getCatalogUrl(resourceType, owner, false);
    return fetch(`${BASE_API_URL}${k8sResourceUrl}`, {
      method: 'POST',
      body: JSON.stringify(k8sResource),
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
        createK8SResourceErrorActionCreator,
        'Not found',
        `Failed to create a new entity in ${k8sResource}`))
      .then((response) => response.json())
      .then((json) => {
        dispatch(createK8SResourceSuccessActionCreator());
        const dispatched = dispatch(getK8SResourceSuccessActionCreator(json));
        if (redirect) {
          history.push(getCatalogEntityUrl(resourceType, json.name, owner, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(createK8SResourceErrorActionCreator(response.status, value)));
        } else {
          return dispatch(createK8SResourceErrorActionCreator(response.status, response.value));
        }
      });
  };
}
