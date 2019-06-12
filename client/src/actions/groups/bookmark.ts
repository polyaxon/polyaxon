import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getGroupUrlFromName } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface BookmarkGroupRequestAction extends Action {
  type: actionTypes.BOOKMARK_GROUP_REQUEST;
  groupName: string;
}

export interface BookmarkGroupSuccessAction extends Action {
  type: actionTypes.BOOKMARK_GROUP_SUCCESS;
  groupName: string;
}

export interface BookmarkGroupErrorAction extends Action {
  type: actionTypes.BOOKMARK_GROUP_ERROR;
  statusCode: number;
  error: any;
  groupName: string;
}

export function bookmarkGroupRequestActionCreator(groupName: string): BookmarkGroupRequestAction {
  return {
    type: actionTypes.BOOKMARK_GROUP_REQUEST,
    groupName,
  };
}

export function bookmarkGroupSuccessActionCreator(groupName: string): BookmarkGroupSuccessAction {
  return {
    type: actionTypes.BOOKMARK_GROUP_SUCCESS,
    groupName,
  };
}

export function bookmarkGroupErrorActionCreator(statusCode: number,
                                                error: any,
                                                groupName: string): BookmarkGroupErrorAction {
  return {
    type: actionTypes.BOOKMARK_GROUP_ERROR,
    statusCode,
    error,
    groupName,
  };
}

export interface UnbookmarkGroupRequestAction extends Action {
  type: actionTypes.UNBOOKMARK_GROUP_REQUEST;
  groupName: string;
}

export interface UnbookmarkGroupSuccessAction extends Action {
  type: actionTypes.UNBOOKMARK_GROUP_SUCCESS;
  groupName: string;
}

export interface UnbookmarkGroupErrorAction extends Action {
  type: actionTypes.UNBOOKMARK_GROUP_ERROR;
  statusCode: number;
  error: any;
  groupName: string;
}

export function unbookmarkGroupRequestActionCreator(groupName: string): UnbookmarkGroupRequestAction {
  return {
    type: actionTypes.UNBOOKMARK_GROUP_REQUEST,
    groupName,
  };
}

export function unbookmarkGroupSuccessActionCreator(groupName: string): UnbookmarkGroupSuccessAction {
  return {
    type: actionTypes.UNBOOKMARK_GROUP_SUCCESS,
    groupName,
  };
}

export function unbookmarkGroupErrorActionCreator(statusCode: number,
                                                  error: any,
                                                  groupName: string): UnbookmarkGroupErrorAction {
  return {
    type: actionTypes.UNBOOKMARK_GROUP_ERROR,
    statusCode,
    error,
    groupName,
  };
}

export type BookmarkGroupAction =
  BookmarkGroupRequestAction
  | BookmarkGroupSuccessAction
  | BookmarkGroupErrorAction
  | UnbookmarkGroupRequestAction
  | UnbookmarkGroupSuccessAction
  | UnbookmarkGroupErrorAction;

export function bookmark(groupName: string): any {
  return (dispatch: any, getState: any) => {
    const groupUrl = getGroupUrlFromName(groupName, false);

    dispatch(bookmarkGroupRequestActionCreator(groupName));

    return fetch(
      `${BASE_API_URL}${groupUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        bookmarkGroupErrorActionCreator,
        'Group not found',
        'Failed to bookmark group',
        [groupName]))
      .then(() => dispatch(bookmarkGroupSuccessActionCreator(groupName)));
  };
}

export function unbookmark(groupName: string): any {
  return (dispatch: any, getState: any) => {
    const groupUrl = getGroupUrlFromName(groupName, false);

    dispatch(unbookmarkGroupRequestActionCreator(groupName));

    return fetch(
      `${BASE_API_URL}${groupUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        unbookmarkGroupErrorActionCreator,
        'Group not found',
        'Failed to unbookmark group',
        [groupName]))
      .then(() => dispatch(unbookmarkGroupSuccessActionCreator(groupName)));
  };
}
