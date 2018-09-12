import { Action } from 'redux';

import { BASE_API_URL } from '../constants/api';
import { handleAuthError } from '../constants/utils';
import { CodeReferenceModel } from '../models/codeReference';

export enum actionTypes {
  RECEIVE_CODE_REFERENCE = 'RECEIVE_CODE_REFERENCE',
  REQUEST_CODE_REFERENCE = 'REQUEST_CODE_REFERENCE',
}

export interface ReceiveCodeReferenceAction extends Action {
  type: actionTypes.RECEIVE_CODE_REFERENCE;
  codeReference: CodeReferenceModel;
}

export interface RequestCodeReferenceAction extends Action {
  type: actionTypes.REQUEST_CODE_REFERENCE;
}

export type CodeReferenceAction = ReceiveCodeReferenceAction | RequestCodeReferenceAction;

export function requestCodeReferenceActionCreator(): RequestCodeReferenceAction {
  return {
    type: actionTypes.REQUEST_CODE_REFERENCE,
  };
}

export function receiveCodeReferenceActionCreator(codeReference: CodeReferenceModel): ReceiveCodeReferenceAction {
  return {
    type: actionTypes.RECEIVE_CODE_REFERENCE,
    codeReference,
  };
}

export function fetchCodeReference(codeRefUrl: string): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestCodeReferenceActionCreator());
    return fetch(
      `${BASE_API_URL}${codeRefUrl}`, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveCodeReferenceActionCreator(json)));
  };
}
