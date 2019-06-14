import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { StoreModel } from '../../models/store';
import { getCatalogUrl } from '../../urls/utils';
import { stdFetchHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchStoresRequestAction extends Action {
  type: actionTypes.FETCH_STORES_REQUEST;
}

export interface FetchStoresSuccessAction extends Action {
  type: actionTypes.FETCH_STORES_SUCCESS;
  stores: StoreModel[];
  count: number;
}

export interface FetchStoresErrorAction extends Action {
  type: actionTypes.FETCH_STORES_ERROR;
  statusCode: number;
  error: any;
}

export function fetchStoresRequestActionCreator(): FetchStoresRequestAction {
  return {
    type: actionTypes.FETCH_STORES_REQUEST,
  };
}

export function fetchStoresSuccessActionCreator(stores: StoreModel[],
                                                count: number): FetchStoresSuccessAction {
  return {
    type: actionTypes.FETCH_STORES_SUCCESS,
    stores,
    count
  };
}

export function fetchStoresErrorActionCreator(statusCode: number, error: any): FetchStoresErrorAction {
  return {
    type: actionTypes.FETCH_STORES_ERROR,
    statusCode,
    error,
  };
}

export type FetchStoreAction =
  FetchStoresRequestAction
  | FetchStoresSuccessAction
  | FetchStoresErrorAction;

function _fetchStores(storesUrl: string,
                      dispatch: any,
                      getState: any): any {
  dispatch(fetchStoresRequestActionCreator());

  const dispatchActionCreator = (results: any, count: number) => {
    dispatch(fetchStoresSuccessActionCreator(results, count));
  };

  return fetch(`${BASE_API_URL}${storesUrl}`, {
    headers: {
      Authorization: 'token ' + getState().auth.token
    }
  })
    .then((response) => stdFetchHandleError(
      response,
      dispatch,
      fetchStoresErrorActionCreator,
      'Stores not found',
      'Failed to fetch stores'))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count))
    .catch((response) => {
      if (response.status === 400) {
        return response.value.json().then(
          (value: any) => dispatch(fetchStoresErrorActionCreator(response.status, value)));
      } else {
        return response.value;
      }
    });
}

export function fetchStores(resourceType: string,
                            owner: string): any {
  return (dispatch: any, getState: any) => {
    const storesUrl = getCatalogUrl(resourceType, owner, false);
    return _fetchStores(storesUrl, dispatch, getState);
  };
}
