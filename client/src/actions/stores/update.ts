import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { StoreModel } from '../../models/store';
import { getCatalogEntityUrl } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface UpdateStoreRequestAction extends Action {
  type: actionTypes.UPDATE_STORE_REQUEST;
  name: string;
}

export interface UpdateStoreSuccessAction extends Action {
  type: actionTypes.UPDATE_STORE_SUCCESS;
  store: StoreModel;
  name: string;
}

export interface UpdateStoreErrorAction extends Action {
  type: actionTypes.UPDATE_STORE_ERROR;
  statusCode: number;
  error: any;
  name: string;
}

export function updateStoreRequestActionCreator(name: string): UpdateStoreRequestAction {
  return {
    type: actionTypes.UPDATE_STORE_REQUEST,
    name
  };
}

export function updateStoreSuccessActionCreator(store: StoreModel, name: string): UpdateStoreSuccessAction {
  return {
    type: actionTypes.UPDATE_STORE_SUCCESS,
    store,
    name
  };
}

export function updateStoreErrorActionCreator(statusCode: number,
                                              error: any,
                                              name: string): UpdateStoreErrorAction {
  return {
    type: actionTypes.UPDATE_STORE_ERROR,
    statusCode,
    error,
    name
  };
}

export type UpdateStoreAction =
  UpdateStoreRequestAction
  | UpdateStoreSuccessAction
  | UpdateStoreErrorAction;

export function updateStore(resourceType: string,
                            owner: string,
                            name: string,
                            updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const storeUrl = getCatalogEntityUrl(resourceType, name, owner, false);

    dispatch(updateStoreRequestActionCreator(name));

    return fetch(`${BASE_API_URL}${storeUrl}`, {
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
        updateStoreErrorActionCreator,
        'Store not found',
        `Failed to update ${resourceType} entity`,
        [name]))
      .then((response) => response.json())
      .then((json) => dispatch(updateStoreSuccessActionCreator(json, name)))
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(updateStoreErrorActionCreator(response.status, value, name)));
        } else {
          return response.value;
        }
      });
  };
}
