import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getGroupUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface StopGroupRequestAction extends Action {
  type: actionTypes.STOP_GROUP_REQUEST;
  groupName: string;
}

export interface StopGroupSuccessAction extends Action {
  type: actionTypes.STOP_GROUP_SUCCESS;
  groupName: string;
}

export interface StopGroupErrorAction extends Action {
  type: actionTypes.STOP_GROUP_ERROR;
  statusCode: number;
  error: any;
  groupName: string;
}

export function stopGroupRequestActionCreator(groupName: string): StopGroupRequestAction {
  return {
    type: actionTypes.STOP_GROUP_REQUEST,
    groupName
  };
}

export function stopGroupSuccessActionCreator(groupName: string): StopGroupSuccessAction {
  return {
    type: actionTypes.STOP_GROUP_SUCCESS,
    groupName
  };
}

export function stopGroupErrorActionCreator(statusCode: number,
                                            error: any,
                                            groupName: string): StopGroupErrorAction {
  return {
    type: actionTypes.STOP_GROUP_ERROR,
    statusCode,
    error,
    groupName
  };
}

export type StopGroupAction =
  StopGroupRequestAction
  | StopGroupSuccessAction
  | StopGroupErrorAction;

export function stopGroup(groupName: string): any {
  return (dispatch: any, getState: any) => {
    const groupUrl = getGroupUrlFromName(groupName, false);

    dispatch(stopGroupRequestActionCreator(groupName));

    return fetch(
      `${BASE_API_URL}${groupUrl}/stop`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        stopGroupErrorActionCreator,
        'Group not found',
        'Failed to stop group',
        [groupName]))
      .then(() => dispatch(stopGroupSuccessActionCreator(groupName)));
  };
}
