import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { GroupModel } from '../../models/group';
import { getGroupUniqueName, getGroupUrl } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface GetGroupRequestAction extends Action {
  type: actionTypes.GET_GROUP_REQUEST;
  groupName: string;
}

export interface GetGroupSuccessAction extends Action {
  type: actionTypes.GET_GROUP_SUCCESS;
  group: GroupModel;
  groupName: string;
}

export interface GetGroupErrorAction extends Action {
  type: actionTypes.GET_GROUP_ERROR;
  statusCode: number;
  error: any;
  groupName: string;
}

export function getGroupRequestActionCreator(groupName: string): GetGroupRequestAction {
  return {
    type: actionTypes.GET_GROUP_REQUEST,
    groupName
  };
}

export function getGroupSuccessActionCreator(group: GroupModel): GetGroupSuccessAction {
  return {
    type: actionTypes.GET_GROUP_SUCCESS,
    group,
    groupName: group.unique_name
  };
}

export function getGroupErrorActionCreator(statusCode: number,
                                           error: any,
                                           groupName: string): GetGroupErrorAction {
  return {
    type: actionTypes.GET_GROUP_ERROR,
    statusCode,
    error,
    groupName
  };
}

export type GetGroupAction =
  GetGroupRequestAction
  | GetGroupSuccessAction
  | GetGroupErrorAction;

export function fetchGroup(user: string, projectName: string, groupId: number): any {
  return (dispatch: any, getState: any) => {
    const groupUrl = getGroupUrl(user, projectName, groupId, false);
    const groupName = getGroupUniqueName(user, projectName, groupId);

    dispatch(getGroupRequestActionCreator(groupName));

    return fetch(`${BASE_API_URL}${groupUrl}`, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        getGroupErrorActionCreator,
        'Group not found',
        'Failed to fetch group',
        [groupName]))
      .then((response) => response.json())
      .then((json) => dispatch(getGroupSuccessActionCreator(json)));
  };
}
