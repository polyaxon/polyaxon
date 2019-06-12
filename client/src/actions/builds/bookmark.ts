import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getBuildUrlFromName } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface BookmarkBuildRequestAction extends Action {
  type: actionTypes.BOOKMARK_BUILD_REQUEST;
  buildName: string;
}

export interface BookmarkBuildSuccessAction extends Action {
  type: actionTypes.BOOKMARK_BUILD_SUCCESS;
  buildName: string;
}

export interface BookmarkBuildErrorAction extends Action {
  type: actionTypes.BOOKMARK_BUILD_ERROR;
  statusCode: number;
  error: any;
  buildName: string;
}

export function bookmarkBuildRequestActionCreator(buildName: string): BookmarkBuildRequestAction {
  return {
    type: actionTypes.BOOKMARK_BUILD_REQUEST,
    buildName,
  };
}

export function bookmarkBuildSuccessActionCreator(buildName: string): BookmarkBuildSuccessAction {
  return {
    type: actionTypes.BOOKMARK_BUILD_SUCCESS,
    buildName,
  };
}

export function bookmarkBuildErrorActionCreator(statusCode: number,
                                                error: any,
                                                buildName: string): BookmarkBuildErrorAction {
  return {
    type: actionTypes.BOOKMARK_BUILD_ERROR,
    statusCode,
    error,
    buildName,
  };
}

export interface UnbookmarkBuildRequestAction extends Action {
  type: actionTypes.UNBOOKMARK_BUILD_REQUEST;
  buildName: string;
}

export interface UnbookmarkBuildSuccessAction extends Action {
  type: actionTypes.UNBOOKMARK_BUILD_SUCCESS;
  buildName: string;
}

export interface UnbookmarkBuildErrorAction extends Action {
  type: actionTypes.UNBOOKMARK_BUILD_ERROR;
  statusCode: number;
  error: any;
  buildName: string;
}

export function unbookmarkBuildRequestActionCreator(buildName: string): UnbookmarkBuildRequestAction {
  return {
    type: actionTypes.UNBOOKMARK_BUILD_REQUEST,
    buildName,
  };
}

export function unbookmarkBuildSuccessActionCreator(buildName: string): UnbookmarkBuildSuccessAction {
  return {
    type: actionTypes.UNBOOKMARK_BUILD_SUCCESS,
    buildName,
  };
}

export function unbookmarkBuildErrorActionCreator(statusCode: number,
                                                  error: any,
                                                  buildName: string): UnbookmarkBuildErrorAction {
  return {
    type: actionTypes.UNBOOKMARK_BUILD_ERROR,
    statusCode,
    error,
    buildName,
  };
}

export type BookmarkBuildAction =
  BookmarkBuildRequestAction
  | BookmarkBuildSuccessAction
  | BookmarkBuildErrorAction
  | UnbookmarkBuildRequestAction
  | UnbookmarkBuildSuccessAction
  | UnbookmarkBuildErrorAction;

export function bookmark(buildName: string): any {
  return (dispatch: any, getState: any) => {
    const buildUrl = getBuildUrlFromName(buildName, false);

    dispatch(bookmarkBuildRequestActionCreator(buildName));

    return fetch(
      `${BASE_API_URL}${buildUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        bookmarkBuildErrorActionCreator,
        'Build not found',
        'Failed to bookmark build',
        [buildName]))
      .then(() => dispatch(bookmarkBuildSuccessActionCreator(buildName)));
  };
}

export function unbookmark(buildName: string): any {
  return (dispatch: any, getState: any) => {
    const buildUrl = getBuildUrlFromName(buildName, false);

    dispatch(unbookmarkBuildRequestActionCreator(buildName));

    return fetch(
      `${BASE_API_URL}${buildUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        unbookmarkBuildErrorActionCreator,
        'Build not found',
        'Failed to unbookmark build',
        [buildName]))
      .then(() => dispatch(unbookmarkBuildSuccessActionCreator(buildName)));
  };
}
