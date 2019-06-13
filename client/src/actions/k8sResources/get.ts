import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { K8SResourceModel } from '../../models/k8sResource';
import { getCatalogEntityUrl } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface GetK8SResourceRequestAction extends Action {
  type: actionTypes.GET_K8S_RESOURCE_REQUEST;
  name: string;
}

export interface GetK8SResourceSuccessAction extends Action {
  type: actionTypes.GET_K8S_RESOURCE_SUCCESS;
  k8sResource: K8SResourceModel;
  name: string;
}

export interface GetK8SResourceErrorAction extends Action {
  type: actionTypes.GET_K8S_RESOURCE_ERROR;
  statusCode: number;
  error: any;
  name: string;
}

export function getK8SResourceRequestActionCreator(name: string): GetK8SResourceRequestAction {
  return {
    type: actionTypes.GET_K8S_RESOURCE_REQUEST,
    name
  };
}

export function getK8SResourceSuccessActionCreator(k8sResource: K8SResourceModel): GetK8SResourceSuccessAction {
  return {
    type: actionTypes.GET_K8S_RESOURCE_SUCCESS,
    k8sResource,
    name: k8sResource.name
  };
}

export function getK8SResourceErrorActionCreator(statusCode: number,
                                                 error: any,
                                                 name: string): GetK8SResourceErrorAction {
  return {
    type: actionTypes.GET_K8S_RESOURCE_ERROR,
    statusCode,
    error,
    name
  };
}

export type GetK8SResourceAction =
  GetK8SResourceRequestAction
  | GetK8SResourceSuccessAction
  | GetK8SResourceErrorAction;

export function getK8SResource(resourceType: string, name: string, owner?: string): any {
  return (dispatch: any, getState: any) => {
    const k8sResourceUrl = getCatalogEntityUrl(resourceType, name, owner, false);

    dispatch(getK8SResourceRequestActionCreator(name));

    return fetch(`${BASE_API_URL}${k8sResourceUrl}`, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        getK8SResourceErrorActionCreator,
        'K8SResource not found',
        `Failed to fetch the ${resourceType} entity`,
        [name]))
      .then((response) => response.json())
      .then((json) => dispatch(getK8SResourceSuccessActionCreator(json)));
  };
}
