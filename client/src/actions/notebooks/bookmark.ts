import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getNotebookApiUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface BookmarkNotebookRequestAction extends Action {
  type: actionTypes.BOOKMARK_NOTEBOOK_REQUEST;
  notebookName: string;
}

export interface BookmarkNotebookSuccessAction extends Action {
  type: actionTypes.BOOKMARK_NOTEBOOK_SUCCESS;
  notebookName: string;
}

export interface BookmarkNotebookErrorAction extends Action {
  type: actionTypes.BOOKMARK_NOTEBOOK_ERROR;
  statusCode: number;
  error: any;
  notebookName: string;
}

export function bookmarkNotebookRequestActionCreator(notebookName: string): BookmarkNotebookRequestAction {
  return {
    type: actionTypes.BOOKMARK_NOTEBOOK_REQUEST,
    notebookName,
  };
}

export function bookmarkNotebookSuccessActionCreator(notebookName: string): BookmarkNotebookSuccessAction {
  return {
    type: actionTypes.BOOKMARK_NOTEBOOK_SUCCESS,
    notebookName,
  };
}

export function bookmarkNotebookErrorActionCreator(statusCode: number,
                                                   error: any,
                                                   notebookName: string): BookmarkNotebookErrorAction {
  return {
    type: actionTypes.BOOKMARK_NOTEBOOK_ERROR,
    statusCode,
    error,
    notebookName,
  };
}

export interface UnbookmarkNotebookRequestAction extends Action {
  type: actionTypes.UNBOOKMARK_NOTEBOOK_REQUEST;
  notebookName: string;
}

export interface UnbookmarkNotebookSuccessAction extends Action {
  type: actionTypes.UNBOOKMARK_NOTEBOOK_SUCCESS;
  notebookName: string;
}

export interface UnbookmarkNotebookErrorAction extends Action {
  type: actionTypes.UNBOOKMARK_NOTEBOOK_ERROR;
  statusCode: number;
  error: any;
  notebookName: string;
}

export function unbookmarkNotebookRequestActionCreator(notebookName: string): UnbookmarkNotebookRequestAction {
  return {
    type: actionTypes.UNBOOKMARK_NOTEBOOK_REQUEST,
    notebookName,
  };
}

export function unbookmarkNotebookSuccessActionCreator(notebookName: string): UnbookmarkNotebookSuccessAction {
  return {
    type: actionTypes.UNBOOKMARK_NOTEBOOK_SUCCESS,
    notebookName,
  };
}

export function unbookmarkNotebookErrorActionCreator(statusCode: number,
                                                     error: any,
                                                     notebookName: string): UnbookmarkNotebookErrorAction {
  return {
    type: actionTypes.UNBOOKMARK_NOTEBOOK_ERROR,
    statusCode,
    error,
    notebookName,
  };
}

export type BookmarkNotebookAction =
  BookmarkNotebookRequestAction
  | BookmarkNotebookSuccessAction
  | BookmarkNotebookErrorAction
  | UnbookmarkNotebookRequestAction
  | UnbookmarkNotebookSuccessAction
  | UnbookmarkNotebookErrorAction;

export function bookmark(notebookName: string): any {
  return (dispatch: any, getState: any) => {
    const notebookUrl = getNotebookApiUrlFromName(notebookName, false);

    dispatch(bookmarkNotebookRequestActionCreator(notebookName));

    return fetch(
      `${BASE_API_URL}${notebookUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        bookmarkNotebookErrorActionCreator,
        'Notebook not found',
        'Failed to bookmark notebook',
        [notebookName]))
      .then(() => dispatch(bookmarkNotebookSuccessActionCreator(notebookName)));
  };
}

export function unbookmark(notebookName: string): any {
  return (dispatch: any, getState: any) => {
    const notebookUrl = getNotebookApiUrlFromName(notebookName, false);

    dispatch(unbookmarkNotebookRequestActionCreator(notebookName));

    return fetch(
      `${BASE_API_URL}${notebookUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        unbookmarkNotebookErrorActionCreator,
        'Notebook not found',
        'Failed to unbookmark notebook',
        [notebookName]))
      .then(() => dispatch(unbookmarkNotebookSuccessActionCreator(notebookName)));
  };
}
