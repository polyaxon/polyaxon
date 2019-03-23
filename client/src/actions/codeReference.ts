import { Action } from 'redux';

import { BASE_API_URL } from '../constants/api';
import { CodeReferenceModel } from '../models/codeReference';
import { stdHandleError } from './utils';

export enum actionTypes {
  FETCH_CODE_REFERENCE_REQUEST = 'FETCH_CODE_REFERENCE_REQUEST',
  FETCH_CODE_REFERENCE_SUCCESS = 'FETCH_CODE_REFERENCE_SUCCESS',
  FETCH_CODE_REFERENCE_ERROR = 'FETCH_CODE_REFERENCE_ERROR',
}

export interface FetchCodeReferenceRequestAction extends Action {
  type: actionTypes.FETCH_CODE_REFERENCE_REQUEST;
}

export interface FetchCodeReferenceSuccessAction extends Action {
  type: actionTypes.FETCH_CODE_REFERENCE_SUCCESS;
  codeReference: CodeReferenceModel;
}

export interface FetchCodeReferenceErrorAction extends Action {
  type: actionTypes.FETCH_CODE_REFERENCE_ERROR;
  statusCode: number;
  error: any;
}

export type CodeReferenceAction =
  FetchCodeReferenceRequestAction
  | FetchCodeReferenceSuccessAction
  | FetchCodeReferenceErrorAction;

export function fetchCodeReferenceRequestActionCreator(): FetchCodeReferenceRequestAction {
  return {
    type: actionTypes.FETCH_CODE_REFERENCE_REQUEST,
  };
}

export function fetchCodeReferenceSuccessActionCreator(
  codeReference: CodeReferenceModel): FetchCodeReferenceSuccessAction {
  return {
    type: actionTypes.FETCH_CODE_REFERENCE_SUCCESS,
    codeReference,
  };
}

export function fetchCodeReferenceErrorActionCreator(statusCode: number, error: any): FetchCodeReferenceErrorAction {
  return {
    type: actionTypes.FETCH_CODE_REFERENCE_ERROR,
    statusCode,
    error
  };
}

export function fetchCodeReference(codeRefUrl: string): any {
  return (dispatch: any, getState: any) => {
    dispatch(fetchCodeReferenceRequestActionCreator());
    return fetch(
      `${BASE_API_URL}${codeRefUrl}`, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        fetchCodeReferenceErrorActionCreator,
        'Code reference not found',
        'Failed to fetch code reference'))
      .then((response) => response.json())
      .then((json) => dispatch(fetchCodeReferenceSuccessActionCreator(json)));
  };
}
