import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { AccessModel } from '../../models/access';
import { getCatalogUrl } from '../../urls/utils';
import { stdFetchHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchAccessesRequestAction extends Action {
  type: actionTypes.FETCH_ACCESSES_REQUEST;
}

export interface FetchAccessesSuccessAction extends Action {
  type: actionTypes.FETCH_ACCESSES_SUCCESS;
  accesses: AccessModel[];
  count: number;
}

export interface FetchAccessesErrorAction extends Action {
  type: actionTypes.FETCH_ACCESSES_ERROR;
  statusCode: number;
  error: any;
}

export function fetchAccessesRequestActionCreator(): FetchAccessesRequestAction {
  return {
    type: actionTypes.FETCH_ACCESSES_REQUEST,
  };
}

export function fetchAccessesSuccessActionCreator(accesses: AccessModel[],
                                                  count: number): FetchAccessesSuccessAction {
  return {
    type: actionTypes.FETCH_ACCESSES_SUCCESS,
    accesses,
    count
  };
}

export function fetchAccessesErrorActionCreator(statusCode: number, error: any): FetchAccessesErrorAction {
  return {
    type: actionTypes.FETCH_ACCESSES_ERROR,
    statusCode,
    error,
  };
}

export type FetchAccessAction =
  FetchAccessesRequestAction
  | FetchAccessesSuccessAction
  | FetchAccessesErrorAction;

function _fetchAccesses(accessesUrl: string,
                        dispatch: any,
                        getState: any): any {
  dispatch(fetchAccessesRequestActionCreator());

  const dispatchActionCreator = (results: any, count: number) => {
    dispatch(fetchAccessesSuccessActionCreator(results, count));
  };

  return fetch(`${BASE_API_URL}${accessesUrl}`, {
    headers: {
      Authorization: 'token ' + getState().auth.token
    }
  })
    .then((response) => stdFetchHandleError(
      response,
      dispatch,
      fetchAccessesErrorActionCreator,
      'Accesses not found',
      'Failed to fetch accesses'))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count))
    .catch((response) => {
      if (response.status === 400) {
        return response.value.json().then(
          (value: any) => dispatch(fetchAccessesErrorActionCreator(response.status, value)));
      } else {
        return response.value;
      }
    });
}

export function fetchAccesses(resourceType: string,
                              owner: string): any {
  return (dispatch: any, getState: any) => {
    const accessesUrl = getCatalogUrl(resourceType, owner, false);
    return _fetchAccesses(accessesUrl, dispatch, getState);
  };
}
