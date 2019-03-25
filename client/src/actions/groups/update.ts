import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getGroupUrlFromName, getProjectNameFromUniqueName, getSelectionUrlFromName } from '../../constants/utils';
import { GroupModel } from '../../models/group';
import { deleteExperimentsSuccessActionCreator } from '../experiments';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface UpdateGroupRequestAction extends Action {
  type: actionTypes.UPDATE_GROUP_REQUEST;
  groupName: string;
}

export interface UpdateGroupSuccessAction extends Action {
  type: actionTypes.UPDATE_GROUP_SUCCESS;
  group: GroupModel;
  groupName: string;
}

export interface UpdateGroupErrorAction extends Action {
  type: actionTypes.UPDATE_GROUP_ERROR;
  statusCode: number;
  error: any;
  groupName: string;
}

export function updateGroupRequestActionCreator(groupName: string): UpdateGroupRequestAction {
  return {
    type: actionTypes.UPDATE_GROUP_REQUEST,
    groupName
  };
}

export function updateGroupSuccessActionCreator(group: GroupModel): UpdateGroupSuccessAction {
  return {
    type: actionTypes.UPDATE_GROUP_SUCCESS,
    group,
    groupName: group.unique_name
  };
}

export function updateGroupErrorActionCreator(statusCode: number,
                                              error: any,
                                              groupName: string): UpdateGroupErrorAction {
  return {
    type: actionTypes.UPDATE_GROUP_ERROR,
    statusCode,
    error,
    groupName
  };
}

export type UpdateGroupAction =
  UpdateGroupRequestAction
  | UpdateGroupSuccessAction
  | UpdateGroupErrorAction;

export function updateGroup(groupName: string, updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const groupUrl = getGroupUrlFromName(groupName, false);

    dispatch(updateGroupRequestActionCreator(groupName));

    return fetch(
      `${BASE_API_URL}${groupUrl}`, {
        method: 'PATCH',
        body: JSON.stringify(updateDict),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdCreateHandleError(
        response,
        dispatch,
        updateGroupErrorActionCreator,
        'Group not found',
        'Failed to group',
        [groupName]))
      .then((response) => response.json())
      .then((json) => dispatch(updateGroupSuccessActionCreator(json)))
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(updateGroupErrorActionCreator(response.status, value, groupName)));
        } else {
          return response.value;
        }
      });
  };
}

export function updateSelection(groupName: string, updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const selectionUrl = getSelectionUrlFromName(groupName, false);

    dispatch(updateGroupRequestActionCreator(groupName));

    return fetch(
      `${BASE_API_URL}${selectionUrl}`, {
        method: 'PATCH',
        body: JSON.stringify(updateDict),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdCreateHandleError(
        response,
        dispatch,
        updateGroupErrorActionCreator,
        'Group not found',
        'Failed to group',
        [groupName]))
      .then(() => {
        if ('operation' in updateDict && updateDict.operation === 'remove') {
          return dispatch(
            deleteExperimentsSuccessActionCreator(getProjectNameFromUniqueName(groupName), updateDict.experiment_ids)
          );
        }
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(updateGroupErrorActionCreator(response.status, value, groupName)));
        } else {
          return response.value;
        }
      });
  };
}
