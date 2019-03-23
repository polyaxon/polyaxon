import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getGroupUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface StartGroupTensorboardRequestAction extends Action {
  type: actionTypes.START_GROUP_TENSORBOARD_REQUEST;
  groupName: string;
}

export interface StartGroupTensorboardSuccessAction extends Action {
  type: actionTypes.START_GROUP_TENSORBOARD_SUCCESS;
  groupName: string;
}

export interface StartGroupTensorboardErrorAction extends Action {
  type: actionTypes.START_GROUP_TENSORBOARD_ERROR;
  statusCode: number;
  error: any;
  groupName: string;
}

export function startGroupTensorboardRequestActionCreator(groupName: string): StartGroupTensorboardRequestAction {
  return {
    type: actionTypes.START_GROUP_TENSORBOARD_REQUEST,
    groupName,
  };
}

export function startGroupTensorboardSuccessActionCreator(groupName: string): StartGroupTensorboardSuccessAction {
  return {
    type: actionTypes.START_GROUP_TENSORBOARD_SUCCESS,
    groupName,
  };
}

export function startGroupTensorboardErrorActionCreator(statusCode: number,
                                                        error: any,
                                                        groupName: string): StartGroupTensorboardErrorAction {
  return {
    type: actionTypes.START_GROUP_TENSORBOARD_ERROR,
    statusCode,
    error,
    groupName,
  };
}

export interface StopGroupTensorboardRequestAction extends Action {
  type: actionTypes.STOP_GROUP_TENSORBOARD_REQUEST;
  groupName: string;
}

export interface StopGroupTensorboardSuccessAction extends Action {
  type: actionTypes.STOP_GROUP_TENSORBOARD_SUCCESS;
  groupName: string;
}

export interface StopGroupTensorboardErrorAction extends Action {
  type: actionTypes.STOP_GROUP_TENSORBOARD_ERROR;
  statusCode: number;
  error: any;
  groupName: string;
}

export function stopGroupTensorboardRequestActionCreator(groupName: string): StopGroupTensorboardRequestAction {
  return {
    type: actionTypes.STOP_GROUP_TENSORBOARD_REQUEST,
    groupName,
  };
}

export function stopGroupTensorboardSuccessActionCreator(groupName: string): StopGroupTensorboardSuccessAction {
  return {
    type: actionTypes.STOP_GROUP_TENSORBOARD_SUCCESS,
    groupName,
  };
}

export function stopGroupTensorboardErrorActionCreator(statusCode: number,
                                                       error: any,
                                                       groupName: string): StopGroupTensorboardErrorAction {
  return {
    type: actionTypes.STOP_GROUP_TENSORBOARD_ERROR,
    statusCode,
    error,
    groupName,
  };
}

export type TensorboardGroupAction =
  StartGroupTensorboardRequestAction
  | StartGroupTensorboardSuccessAction
  | StartGroupTensorboardErrorAction
  | StopGroupTensorboardRequestAction
  | StopGroupTensorboardSuccessAction
  | StopGroupTensorboardErrorAction;

export function startTensorboard(groupName: string): any {
  return (dispatch: any, getState: any) => {
    const groupUrl = getGroupUrlFromName(groupName, false);

    dispatch(startGroupTensorboardRequestActionCreator(groupName));

    return fetch(`${BASE_API_URL}${groupUrl}/tensorboard/start`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        startGroupTensorboardErrorActionCreator,
        'Group not found',
        'Failed to start tensorboard for group',
        [groupName]))
      .then(() => dispatch(startGroupTensorboardSuccessActionCreator(groupName)));
  };
}

export function stopTensorboard(groupName: string): any {
  return (dispatch: any, getState: any) => {
    const groupUrl = getGroupUrlFromName(groupName, false);

    dispatch(stopGroupTensorboardRequestActionCreator(groupName));

    return fetch(`${BASE_API_URL}${groupUrl}/tensorboard/stop`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        stopGroupTensorboardErrorActionCreator,
        'Group/Tensorboard not found',
        'Failed to stop tensorboard for group',
        [groupName]))
      .then(() => dispatch(stopGroupTensorboardSuccessActionCreator(groupName)));
  };
}
