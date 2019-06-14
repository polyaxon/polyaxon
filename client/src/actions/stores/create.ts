import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { StoreModel } from '../../models/store';
import { getCatalogEntityUrl, getCatalogUrl } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getStoreSuccessActionCreator } from './get';

export interface CreateStoreRequestAction extends Action {
  type: actionTypes.CREATE_STORE_REQUEST;
}

export interface CreateStoreSuccessAction extends Action {
  type: actionTypes.CREATE_STORE_SUCCESS;
}

export interface CreateStoreErrorAction extends Action {
  type: actionTypes.CREATE_STORE_ERROR;
  statusCode: number;
  error: any;
}

export function createStoreRequestActionCreator(): CreateStoreRequestAction {
  return {
    type: actionTypes.CREATE_STORE_REQUEST,
  };
}

export function createStoreSuccessActionCreator(): CreateStoreSuccessAction {
  return {
    type: actionTypes.CREATE_STORE_SUCCESS,
  };
}

export function createStoreErrorActionCreator(statusCode: number, error: any): CreateStoreErrorAction {
  return {
    type: actionTypes.CREATE_STORE_ERROR,
    statusCode,
    error
  };
}

export type CreateStoreAction =
  CreateStoreRequestAction
  | CreateStoreSuccessAction
  | CreateStoreErrorAction;

export function createStore(resourceType: string,
                            store: StoreModel,
                            owner?: string,
                            redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {

    dispatch(createStoreRequestActionCreator());

    const storeUrl = getCatalogUrl(resourceType, owner, false);
    return fetch(`${BASE_API_URL}${storeUrl}`, {
      method: 'POST',
      body: JSON.stringify(store),
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
        createStoreErrorActionCreator,
        'Not found',
        `Failed to create a new entity in ${store}`))
      .then((response) => response.json())
      .then((json) => {
        dispatch(createStoreSuccessActionCreator());
        const dispatched = dispatch(getStoreSuccessActionCreator(json));
        if (redirect) {
          history.push(getCatalogEntityUrl(resourceType, json.name, owner, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(createStoreErrorActionCreator(response.status, value)));
        } else {
          return dispatch(createStoreErrorActionCreator(response.status, response.value));
        }
      });
  };
}
