import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { AccessModel } from '../../models/access';
import { getCatalogEntityUrl } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface GetAccessRequestAction extends Action {
  type: actionTypes.GET_ACCESS_REQUEST;
  name: string;
}

export interface GetAccessSuccessAction extends Action {
  type: actionTypes.GET_ACCESS_SUCCESS;
  access: AccessModel;
  name: string;
}

export interface GetAccessErrorAction extends Action {
  type: actionTypes.GET_ACCESS_ERROR;
  statusCode: number;
  error: any;
  name: string;
}

export function getAccessRequestActionCreator(name: string): GetAccessRequestAction {
  return {
    type: actionTypes.GET_ACCESS_REQUEST,
    name
  };
}

export function getAccessSuccessActionCreator(access: AccessModel): GetAccessSuccessAction {
  return {
    type: actionTypes.GET_ACCESS_SUCCESS,
    access,
    name: access.name
  };
}

export function getAccessErrorActionCreator(statusCode: number,
                                            error: any,
                                            name: string): GetAccessErrorAction {
  return {
    type: actionTypes.GET_ACCESS_ERROR,
    statusCode,
    error,
    name
  };
}

export type GetAccessAction =
  GetAccessRequestAction
  | GetAccessSuccessAction
  | GetAccessErrorAction;

export function getAccess(resourceType: string, name: string, owner?: string): any {
  return (dispatch: any, getState: any) => {
    const accessUrl = getCatalogEntityUrl(resourceType, name, owner, false);

    dispatch(getAccessRequestActionCreator(name));

    return fetch(`${BASE_API_URL}${accessUrl}`, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        getAccessErrorActionCreator,
        'Access not found',
        `Failed to fetch the ${resourceType} entity`,
        [name]))
      .then((response) => response.json())
      .then((json) => dispatch(getAccessSuccessActionCreator(json)));
  };
}
