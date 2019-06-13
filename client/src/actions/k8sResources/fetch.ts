import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { K8SResourceModel } from '../../models/k8sResource';
import { getCatalogUrl } from '../../urls/utils';
import { stdFetchHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchK8SResourcesRequestAction extends Action {
  type: actionTypes.FETCH_K8S_RESOURCES_REQUEST;
}

export interface FetchK8SResourcesSuccessAction extends Action {
  type: actionTypes.FETCH_K8S_RESOURCES_SUCCESS;
  k8sResources: K8SResourceModel[];
  count: number;
}

export interface FetchK8SResourcesErrorAction extends Action {
  type: actionTypes.FETCH_K8S_RESOURCES_ERROR;
  statusCode: number;
  error: any;
}

export function fetchK8SResourcesRequestActionCreator(): FetchK8SResourcesRequestAction {
  return {
    type: actionTypes.FETCH_K8S_RESOURCES_REQUEST,
  };
}

export function fetchK8SResourcesSuccessActionCreator(k8sResources: K8SResourceModel[],
                                                      count: number): FetchK8SResourcesSuccessAction {
  return {
    type: actionTypes.FETCH_K8S_RESOURCES_SUCCESS,
    k8sResources,
    count
  };
}

export function fetchK8SResourcesErrorActionCreator(statusCode: number, error: any): FetchK8SResourcesErrorAction {
  return {
    type: actionTypes.FETCH_K8S_RESOURCES_ERROR,
    statusCode,
    error,
  };
}

export type FetchK8SResourceAction =
  FetchK8SResourcesRequestAction
  | FetchK8SResourcesSuccessAction
  | FetchK8SResourcesErrorAction;

function _fetchK8SResources(k8sResourcesUrl: string,
                            dispatch: any,
                            getState: any): any {
  dispatch(fetchK8SResourcesRequestActionCreator());

  const dispatchActionCreator = (results: any, count: number) => {
    dispatch(fetchK8SResourcesSuccessActionCreator(results, count));
  };

  return fetch(`${BASE_API_URL}${k8sResourcesUrl}`, {
    headers: {
      Authorization: 'token ' + getState().auth.token
    }
  })
    .then((response) => stdFetchHandleError(
      response,
      dispatch,
      fetchK8SResourcesErrorActionCreator,
      'K8SResources not found',
      'Failed to fetch k8sResources'))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count))
    .catch((response) => {
      if (response.status === 400) {
        return response.value.json().then(
          (value: any) => dispatch(fetchK8SResourcesErrorActionCreator(response.status, value)));
      } else {
        return response.value;
      }
    });
}

export function fetchK8SResources(resourceType: string,
                                  owner: string): any {
  return (dispatch: any, getState: any) => {
    const k8sResourcesUrl = getCatalogUrl(resourceType, owner, false);
    return _fetchK8SResources(k8sResourcesUrl, dispatch, getState);
  };
}
