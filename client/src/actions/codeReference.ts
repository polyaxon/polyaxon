import { Action } from 'redux';

import { BASE_API_URL } from '../constants/api';
import { CodeReferenceModel } from '../models/codeReference';
import { stdHandleError } from './utils';

export enum actionTypes {
  GET_CODE_REFERENCE_REQUEST = 'GET_CODE_REFERENCE_REQUEST',
  GET_CODE_REFERENCE_SUCCESS = 'GET_CODE_REFERENCE_SUCCESS',
  GET_CODE_REFERENCE_ERROR = 'GET_CODE_REFERENCE_ERROR',
}

export interface GetCodeReferenceRequestAction extends Action {
  type: actionTypes.GET_CODE_REFERENCE_REQUEST;
}

export interface GetCodeReferenceSuccessAction extends Action {
  type: actionTypes.GET_CODE_REFERENCE_SUCCESS;
  codeReference: CodeReferenceModel;
}

export interface GetCodeReferenceErrorAction extends Action {
  type: actionTypes.GET_CODE_REFERENCE_ERROR;
  statusCode: number;
  error: any;
}

export type CodeReferenceAction =
  GetCodeReferenceRequestAction
  | GetCodeReferenceSuccessAction
  | GetCodeReferenceErrorAction;

export function getCodeReferenceRequestActionCreator(): GetCodeReferenceRequestAction {
  return {
    type: actionTypes.GET_CODE_REFERENCE_REQUEST,
  };
}

export function getCodeReferenceSuccessActionCreator(
  codeReference: CodeReferenceModel): GetCodeReferenceSuccessAction {
  return {
    type: actionTypes.GET_CODE_REFERENCE_SUCCESS,
    codeReference,
  };
}

export function getCodeReferenceErrorActionCreator(statusCode: number, error: any): GetCodeReferenceErrorAction {
  return {
    type: actionTypes.GET_CODE_REFERENCE_ERROR,
    statusCode,
    error
  };
}

export function getCodeReference(codeRefUrl: string): any {
  return (dispatch: any, getState: any) => {
    dispatch(getCodeReferenceRequestActionCreator());
    return fetch(
      `${BASE_API_URL}${codeRefUrl}`, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        getCodeReferenceErrorActionCreator,
        'Code reference not found',
        'Failed to fetch code reference'))
      .then((response) => response.json())
      .then((json) => dispatch(getCodeReferenceSuccessActionCreator(json)));
  };
}
