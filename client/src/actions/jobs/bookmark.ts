import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getJobUrlFromName } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface BookmarkJobRequestAction extends Action {
  type: actionTypes.BOOKMARK_JOB_REQUEST;
  jobName: string;
}

export interface BookmarkJobSuccessAction extends Action {
  type: actionTypes.BOOKMARK_JOB_SUCCESS;
  jobName: string;
}

export interface BookmarkJobErrorAction extends Action {
  type: actionTypes.BOOKMARK_JOB_ERROR;
  statusCode: number;
  error: any;
  jobName: string;
}

export function bookmarkJobRequestActionCreator(jobName: string): BookmarkJobRequestAction {
  return {
    type: actionTypes.BOOKMARK_JOB_REQUEST,
    jobName,
  };
}

export function bookmarkJobSuccessActionCreator(jobName: string): BookmarkJobSuccessAction {
  return {
    type: actionTypes.BOOKMARK_JOB_SUCCESS,
    jobName,
  };
}

export function bookmarkJobErrorActionCreator(statusCode: number,
                                              error: any,
                                              jobName: string): BookmarkJobErrorAction {
  return {
    type: actionTypes.BOOKMARK_JOB_ERROR,
    statusCode,
    error,
    jobName,
  };
}

export interface UnbookmarkJobRequestAction extends Action {
  type: actionTypes.UNBOOKMARK_JOB_REQUEST;
  jobName: string;
}

export interface UnbookmarkJobSuccessAction extends Action {
  type: actionTypes.UNBOOKMARK_JOB_SUCCESS;
  jobName: string;
}

export interface UnbookmarkJobErrorAction extends Action {
  type: actionTypes.UNBOOKMARK_JOB_ERROR;
  statusCode: number;
  error: any;
  jobName: string;
}

export function unbookmarkJobRequestActionCreator(jobName: string): UnbookmarkJobRequestAction {
  return {
    type: actionTypes.UNBOOKMARK_JOB_REQUEST,
    jobName,
  };
}

export function unbookmarkJobSuccessActionCreator(jobName: string): UnbookmarkJobSuccessAction {
  return {
    type: actionTypes.UNBOOKMARK_JOB_SUCCESS,
    jobName,
  };
}

export function unbookmarkJobErrorActionCreator(statusCode: number,
                                                error: any,
                                                jobName: string): UnbookmarkJobErrorAction {
  return {
    type: actionTypes.UNBOOKMARK_JOB_ERROR,
    statusCode,
    error,
    jobName,
  };
}

export type BookmarkJobAction =
  BookmarkJobRequestAction
  | BookmarkJobSuccessAction
  | BookmarkJobErrorAction
  | UnbookmarkJobRequestAction
  | UnbookmarkJobSuccessAction
  | UnbookmarkJobErrorAction;

export function bookmark(jobName: string): any {
  return (dispatch: any, getState: any) => {
    const jobUrl = getJobUrlFromName(jobName, false);

    dispatch(bookmarkJobRequestActionCreator(jobName));

    return fetch(
      `${BASE_API_URL}${jobUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        bookmarkJobErrorActionCreator,
        'Job not found',
        'Failed to bookmark job',
        [jobName]))
      .then(() => dispatch(bookmarkJobSuccessActionCreator(jobName)));
  };
}

export function unbookmark(jobName: string): any {
  return (dispatch: any, getState: any) => {
    const jobUrl = getJobUrlFromName(jobName, false);

    dispatch(unbookmarkJobRequestActionCreator(jobName));

    return fetch(
      `${BASE_API_URL}${jobUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        unbookmarkJobErrorActionCreator,
        'Job not found',
        'Failed to unbookmark job',
        [jobName]))
      .then(() => dispatch(unbookmarkJobSuccessActionCreator(jobName)));
  };
}
