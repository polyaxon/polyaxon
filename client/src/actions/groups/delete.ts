import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getGroupUrlFromName, getProjectUrl } from '../../constants/utils';
import history from '../../history';
import { stdDeleteHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface DeleteGroupRequestAction extends Action {
  type: actionTypes.DELETE_GROUP_REQUEST;
  groupName: string;
}

export interface DeleteGroupSuccessAction extends Action {
  type: actionTypes.DELETE_GROUP_SUCCESS;
  groupName: string;
}

export interface DeleteGroupErrorAction extends Action {
  type: actionTypes.DELETE_GROUP_ERROR;
  statusCode: number;
  error: any;
  groupName: string;
}

export function deleteGroupRequestActionCreator(groupName: string): DeleteGroupRequestAction {
  return {
    type: actionTypes.DELETE_GROUP_REQUEST,
    groupName
  };
}

export function deleteGroupSuccessActionCreator(groupName: string): DeleteGroupSuccessAction {
  return {
    type: actionTypes.DELETE_GROUP_SUCCESS,
    groupName
  };
}

export function deleteGroupErrorActionCreator(statusCode: number,
                                              error: any,
                                              groupName: string): DeleteGroupErrorAction {
  return {
    type: actionTypes.DELETE_GROUP_ERROR,
    statusCode,
    error,
    groupName
  };
}

export type DeleteGroupAction =
  DeleteGroupRequestAction
  | DeleteGroupSuccessAction
  | DeleteGroupErrorAction;

export function deleteGroup(groupName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const groupUrl = getGroupUrlFromName(groupName, false);

    dispatch(deleteGroupRequestActionCreator(groupName));

    return fetch(
      `${BASE_API_URL}${groupUrl}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdDeleteHandleError(
        response,
        dispatch,
        deleteGroupErrorActionCreator,
        'Group not found',
        'Failed to delete group',
        [groupName]))
      .then(() => {
        const dispatched = dispatch(deleteGroupSuccessActionCreator(groupName));
        if (redirect) {
          const values = groupName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#group');
        }
        return dispatched;
      });
  };
}
