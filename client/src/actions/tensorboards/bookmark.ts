import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getTensorboardApiUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface BookmarkTensorboardRequestAction extends Action {
  type: actionTypes.BOOKMARK_TENSORBOARD_REQUEST;
  tensorboardName: string;
}

export interface BookmarkTensorboardSuccessAction extends Action {
  type: actionTypes.BOOKMARK_TENSORBOARD_SUCCESS;
  tensorboardName: string;
}

export interface BookmarkTensorboardErrorAction extends Action {
  type: actionTypes.BOOKMARK_TENSORBOARD_ERROR;
  statusCode: number;
  error: any;
  tensorboardName: string;
}

export function bookmarkTensorboardRequestActionCreator(tensorboardName: string): BookmarkTensorboardRequestAction {
  return {
    type: actionTypes.BOOKMARK_TENSORBOARD_REQUEST,
    tensorboardName,
  };
}

export function bookmarkTensorboardSuccessActionCreator(tensorboardName: string): BookmarkTensorboardSuccessAction {
  return {
    type: actionTypes.BOOKMARK_TENSORBOARD_SUCCESS,
    tensorboardName,
  };
}

export function bookmarkTensorboardErrorActionCreator(statusCode: number,
                                                      error: any,
                                                      tensorboardName: string): BookmarkTensorboardErrorAction {
  return {
    type: actionTypes.BOOKMARK_TENSORBOARD_ERROR,
    statusCode,
    error,
    tensorboardName,
  };
}

export interface UnbookmarkTensorboardRequestAction extends Action {
  type: actionTypes.UNBOOKMARK_TENSORBOARD_REQUEST;
  tensorboardName: string;
}

export interface UnbookmarkTensorboardSuccessAction extends Action {
  type: actionTypes.UNBOOKMARK_TENSORBOARD_SUCCESS;
  tensorboardName: string;
}

export interface UnbookmarkTensorboardErrorAction extends Action {
  type: actionTypes.UNBOOKMARK_TENSORBOARD_ERROR;
  statusCode: number;
  error: any;
  tensorboardName: string;
}

export function unbookmarkTensorboardRequestActionCreator(tensorboardName: string): UnbookmarkTensorboardRequestAction {
  return {
    type: actionTypes.UNBOOKMARK_TENSORBOARD_REQUEST,
    tensorboardName,
  };
}

export function unbookmarkTensorboardSuccessActionCreator(tensorboardName: string): UnbookmarkTensorboardSuccessAction {
  return {
    type: actionTypes.UNBOOKMARK_TENSORBOARD_SUCCESS,
    tensorboardName,
  };
}

export function unbookmarkTensorboardErrorActionCreator(statusCode: number,
                                                        error: any,
                                                        tensorboardName: string): UnbookmarkTensorboardErrorAction {
  return {
    type: actionTypes.UNBOOKMARK_TENSORBOARD_ERROR,
    statusCode,
    error,
    tensorboardName,
  };
}

export type BookmarkTensorboardAction =
  BookmarkTensorboardRequestAction
  | BookmarkTensorboardSuccessAction
  | BookmarkTensorboardErrorAction
  | UnbookmarkTensorboardRequestAction
  | UnbookmarkTensorboardSuccessAction
  | UnbookmarkTensorboardErrorAction;

export function bookmark(tensorboardName: string): any {
  return (dispatch: any, getState: any) => {
    const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);

    dispatch(bookmarkTensorboardRequestActionCreator(tensorboardName));

    return fetch(
      `${BASE_API_URL}${tensorboardUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        bookmarkTensorboardErrorActionCreator,
        'Tensorboard not found',
        'Failed to bookmark tensorboard',
        [tensorboardName]))
      .then(() => dispatch(bookmarkTensorboardSuccessActionCreator(tensorboardName)));
  };
}

export function unbookmark(tensorboardName: string): any {
  return (dispatch: any, getState: any) => {
    const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);

    dispatch(unbookmarkTensorboardRequestActionCreator(tensorboardName));

    return fetch(
      `${BASE_API_URL}${tensorboardUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        unbookmarkTensorboardErrorActionCreator,
        'Tensorboard not found',
        'Failed to unbookmark tensorboard',
        [tensorboardName]))
      .then(() => dispatch(unbookmarkTensorboardSuccessActionCreator(tensorboardName)));
  };
}
