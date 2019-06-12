import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getGroupUrlFromName } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface RestoreGroupRequestAction extends Action {
  type: actionTypes.RESTORE_GROUP_REQUEST;
  groupName: string;
}

export interface RestoreGroupSuccessAction extends Action {
  type: actionTypes.RESTORE_GROUP_SUCCESS;
  groupName: string;
}

export interface RestoreGroupErrorAction extends Action {
  type: actionTypes.RESTORE_GROUP_ERROR;
  statusCode: number;
  error: any;
  groupName: string;
}

export function restoreGroupRequestActionCreator(groupName: string): RestoreGroupRequestAction {
  return {
    type: actionTypes.RESTORE_GROUP_REQUEST,
    groupName
  };
}

export function restoreGroupSuccessActionCreator(groupName: string): RestoreGroupSuccessAction {
  return {
    type: actionTypes.RESTORE_GROUP_SUCCESS,
    groupName
  };
}

export function restoreGroupErrorActionCreator(statusCode: number,
                                               error: any,
                                               groupName: string): RestoreGroupErrorAction {
  return {
    type: actionTypes.RESTORE_GROUP_ERROR,
    statusCode,
    error,
    groupName
  };
}

export type RestoreGroupAction =
  RestoreGroupRequestAction
  | RestoreGroupSuccessAction
  | RestoreGroupErrorAction;

export function restoreGroup(groupName: string): any {
  return (dispatch: any, getState: any) => {
    const groupUrl = getGroupUrlFromName(groupName, false);

    dispatch(restoreGroupRequestActionCreator(groupName));

    return fetch(
      `${BASE_API_URL}${groupUrl}/restore`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        restoreGroupErrorActionCreator,
        'Group not found',
        'Failed to restore group',
        [groupName]))
      .then(() => dispatch(restoreGroupSuccessActionCreator(groupName)));
  };
}
