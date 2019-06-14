import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { K8SResourceModel } from '../../models/k8sResource';
import { getCatalogUrl } from '../../urls/utils';
import { stdFetchHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchK8SResourcesNamesRequestAction extends Action {
  type: actionTypes.FETCH_K8S_RESOURCES_REQUEST;
}

export interface FetchK8SResourcesNamesSuccessAction extends Action {
  type: actionTypes.FETCH_K8S_RESOURCES_SUCCESS;
  k8sResources: K8SResourceModel[];
  count: number;
}

export interface FetchK8SResourcesNamesErrorAction extends Action {
  type: actionTypes.FETCH_K8S_RESOURCES_ERROR;
  statusCode: number;
  error: any;
}

export function fetchK8SResourcesNamesRequestActionCreator(): FetchK8SResourcesNamesRequestAction {
  return {
    type: actionTypes.FETCH_K8S_RESOURCES_REQUEST,
  };
}

export function fetchK8SResourcesNamesSuccessActionCreator(k8sResources: K8SResourceModel[],
                                                           count: number): FetchK8SResourcesNamesSuccessAction {
  return {
    type: actionTypes.FETCH_K8S_RESOURCES_SUCCESS,
    k8sResources,
    count,
  };
}

export function fetchK8SResourcesNamesErrorActionCreator(statusCode: number,
                                                         error: any): FetchK8SResourcesNamesErrorAction {
  return {
    type: actionTypes.FETCH_K8S_RESOURCES_ERROR,
    statusCode,
    error,
  };
}

export type FetchK8SResourceNameAction =
  FetchK8SResourcesNamesRequestAction
  | FetchK8SResourcesNamesSuccessAction
  | FetchK8SResourcesNamesErrorAction;

function _fetchK8SResourcesNames(k8sResourcesUrl: string,
                                 dispatch: any,
                                 getState: any): any {

  dispatch(fetchK8SResourcesNamesRequestActionCreator());

  const dispatchActionCreator = (results: any, count: number) => {
    return dispatch(fetchK8SResourcesNamesSuccessActionCreator(results, count));
  };

  return fetch(`${BASE_API_URL}${k8sResourcesUrl}`, {
    headers: {
      Authorization: 'token ' + getState().auth.token
    }
  })
    .then((response) => stdFetchHandleError(
      response,
      dispatch,
      fetchK8SResourcesNamesErrorActionCreator,
      'K8SResources not found',
      'Failed to fetch k8sResources'))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count))
    .catch((error) => undefined)
    .catch((response) => {
      if (response.status === 400) {
        return response.value.json().then(
          (value: any) => dispatch(fetchK8SResourcesNamesErrorActionCreator(response.status, value)));
      } else {
        return response.value;
      }
    });
}

export function fetchK8SResourcesNames(resourceType: string, owner: string): any {
  return (dispatch: any, getState: any) => {
    const k8sResourcesUrl = getCatalogUrl(resourceType, owner, false);
    return _fetchK8SResourcesNames(k8sResourcesUrl, dispatch, getState);
  };
}
