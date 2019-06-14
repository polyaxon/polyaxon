import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { StoreModel } from '../../models/store';
import { getCatalogEntityUrl } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface GetStoreRequestAction extends Action {
  type: actionTypes.GET_STORE_REQUEST;
  name: string;
}

export interface GetStoreSuccessAction extends Action {
  type: actionTypes.GET_STORE_SUCCESS;
  store: StoreModel;
  name: string;
}

export interface GetStoreErrorAction extends Action {
  type: actionTypes.GET_STORE_ERROR;
  statusCode: number;
  error: any;
  name: string;
}

export function getStoreRequestActionCreator(name: string): GetStoreRequestAction {
  return {
    type: actionTypes.GET_STORE_REQUEST,
    name
  };
}

export function getStoreSuccessActionCreator(store: StoreModel): GetStoreSuccessAction {
  return {
    type: actionTypes.GET_STORE_SUCCESS,
    store,
    name: store.name
  };
}

export function getStoreErrorActionCreator(statusCode: number,
                                           error: any,
                                           name: string): GetStoreErrorAction {
  return {
    type: actionTypes.GET_STORE_ERROR,
    statusCode,
    error,
    name
  };
}

export type GetStoreAction =
  GetStoreRequestAction
  | GetStoreSuccessAction
  | GetStoreErrorAction;

export function getStore(resourceType: string, name: string, owner?: string): any {
  return (dispatch: any, getState: any) => {
    const storeUrl = getCatalogEntityUrl(resourceType, name, owner, false);

    dispatch(getStoreRequestActionCreator(name));

    return fetch(`${BASE_API_URL}${storeUrl}`, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        getStoreErrorActionCreator,
        'Store not found',
        `Failed to fetch the ${resourceType} entity`,
        [name]))
      .then((response) => response.json())
      .then((json) => dispatch(getStoreSuccessActionCreator(json)));
  };
}
