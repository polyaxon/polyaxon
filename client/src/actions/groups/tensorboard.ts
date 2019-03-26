import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import {
  getGroupUniqueName,
  getGroupUrl,
  getGroupUrlFromName,
  getTensorboardApiUrlFromName
} from '../../constants/utils';
import history from '../../history';
import { TensorboardModel } from '../../models/tensorboard';
import { getTensorboardSuccessActionCreator } from '../tensorboards';
import { stdCreateHandleError, stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface StartGroupTensorboardRequestAction extends Action {
  type: actionTypes.START_GROUP_TENSORBOARD_REQUEST;
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
  | StartGroupTensorboardErrorAction
  | StopGroupTensorboardRequestAction
  | StopGroupTensorboardSuccessAction
  | StopGroupTensorboardErrorAction;

export function startTensorboard(user: string,
                                 projectName: string,
                                 groupId: string,
                                 tensorboard: TensorboardModel,
                                 redirect: boolean): any {
  return (dispatch: any, getState: any) => {
    const groupName = getGroupUniqueName(user, projectName, groupId);
    const groupUrl = getGroupUrl(user, projectName, groupId, false);

    dispatch(startGroupTensorboardRequestActionCreator(groupName));

    return fetch(`${BASE_API_URL}${groupUrl}/tensorboard/start`, {
      method: 'POST',
      body: JSON.stringify(tensorboard),
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
        startGroupTensorboardErrorActionCreator,
        'Group not found',
        'Failed to start tensorboard for group',
        [groupName]))
      .then((response) => response.json())
      .then((json) => {
        const dispatched = dispatch(getTensorboardSuccessActionCreator(json));
        if (redirect) {
          history.push(getTensorboardApiUrlFromName( json.unique_name, true));
        }
        return dispatched;
      })
       .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(startGroupTensorboardErrorActionCreator(response.status, value, groupName)));
        } else {
          return response.value;
        }
      });
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
