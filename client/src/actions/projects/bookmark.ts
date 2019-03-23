import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getProjectUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface BookmarkProjectRequestAction extends Action {
  type: actionTypes.BOOKMARK_PROJECT_REQUEST;
  projectName: string;
}

export interface BookmarkProjectSuccessAction extends Action {
  type: actionTypes.BOOKMARK_PROJECT_SUCCESS;
  projectName: string;
}

export interface BookmarkProjectErrorAction extends Action {
  type: actionTypes.BOOKMARK_PROJECT_ERROR;
  statusCode: number;
  error: any;
  projectName: string;
}

export function bookmarkProjectRequestActionCreator(projectName: string): BookmarkProjectRequestAction {
  return {
    type: actionTypes.BOOKMARK_PROJECT_REQUEST,
    projectName,
  };
}

export function bookmarkProjectSuccessActionCreator(projectName: string): BookmarkProjectSuccessAction {
  return {
    type: actionTypes.BOOKMARK_PROJECT_SUCCESS,
    projectName,
  };
}

export function bookmarkProjectErrorActionCreator(statusCode: number,
                                                  error: any,
                                                  projectName: string): BookmarkProjectErrorAction {
  return {
    type: actionTypes.BOOKMARK_PROJECT_ERROR,
    statusCode,
    error,
    projectName,
  };
}

export interface UnbookmarkProjectRequestAction extends Action {
  type: actionTypes.UNBOOKMARK_PROJECT_REQUEST;
  projectName: string;
}

export interface UnbookmarkProjectSuccessAction extends Action {
  type: actionTypes.UNBOOKMARK_PROJECT_SUCCESS;
  projectName: string;
}

export interface UnbookmarkProjectErrorAction extends Action {
  type: actionTypes.UNBOOKMARK_PROJECT_ERROR;
  statusCode: number;
  error: any;
  projectName: string;
}

export function unbookmarkProjectRequestActionCreator(projectName: string): UnbookmarkProjectRequestAction {
  return {
    type: actionTypes.UNBOOKMARK_PROJECT_REQUEST,
    projectName,
  };
}

export function unbookmarkProjectSuccessActionCreator(projectName: string): UnbookmarkProjectSuccessAction {
  return {
    type: actionTypes.UNBOOKMARK_PROJECT_SUCCESS,
    projectName,
  };
}

export function unbookmarkProjectErrorActionCreator(statusCode: number,
                                                    error: any,
                                                    projectName: string): UnbookmarkProjectErrorAction {
  return {
    type: actionTypes.UNBOOKMARK_PROJECT_ERROR,
    statusCode,
    error,
    projectName,
  };
}

export type BookmarkProjectAction =
  BookmarkProjectRequestAction
  | BookmarkProjectSuccessAction
  | BookmarkProjectErrorAction
  | UnbookmarkProjectRequestAction
  | UnbookmarkProjectSuccessAction
  | UnbookmarkProjectErrorAction;

export function bookmark(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const projectUrl = getProjectUrlFromName(projectName, false);

    dispatch(bookmarkProjectRequestActionCreator(projectName));

    return fetch(
      `${BASE_API_URL}${projectUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        bookmarkProjectErrorActionCreator,
        'Project not found',
        'Failed to bookmark project',
        [projectName]))
      .then(() => dispatch(bookmarkProjectSuccessActionCreator(projectName)));
  };
}

export function unbookmark(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const projectUrl = getProjectUrlFromName(projectName, false);

    dispatch(unbookmarkProjectRequestActionCreator(projectName));

    return fetch(
      `${BASE_API_URL}${projectUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        unbookmarkProjectErrorActionCreator,
        'PRoject not found',
        'Failed to unbookmark project',
        [projectName]))
      .then(() => dispatch(unbookmarkProjectSuccessActionCreator(projectName)));
  };
}
