import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getExperimentUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface BookmarkExperimentRequestAction extends Action {
  type: actionTypes.BOOKMARK_EXPERIMENT_REQUEST;
  experimentName: string;
}

export interface BookmarkExperimentSuccessAction extends Action {
  type: actionTypes.BOOKMARK_EXPERIMENT_SUCCESS;
  experimentName: string;
}

export interface BookmarkExperimentErrorAction extends Action {
  type: actionTypes.BOOKMARK_EXPERIMENT_ERROR;
  statusCode: number;
  error: any;
  experimentName: string;
}

export function bookmarkExperimentRequestActionCreator(
  experimentName: string): BookmarkExperimentRequestAction {
  return {
    type: actionTypes.BOOKMARK_EXPERIMENT_REQUEST,
    experimentName,
  };
}

export function bookmarkExperimentSuccessActionCreator(
  experimentName: string): BookmarkExperimentSuccessAction {
  return {
    type: actionTypes.BOOKMARK_EXPERIMENT_SUCCESS,
    experimentName,
  };
}

export function bookmarkExperimentErrorActionCreator(statusCode: number,
                                                     error: any,
                                                     experimentName: string): BookmarkExperimentErrorAction {
  return {
    type: actionTypes.BOOKMARK_EXPERIMENT_ERROR,
    statusCode,
    error,
    experimentName,
  };
}

export interface UnbookmarkExperimentRequestAction extends Action {
  type: actionTypes.UNBOOKMARK_EXPERIMENT_REQUEST;
  experimentName: string;
}

export interface UnbookmarkExperimentSuccessAction extends Action {
  type: actionTypes.UNBOOKMARK_EXPERIMENT_SUCCESS;
  experimentName: string;
}

export interface UnbookmarkExperimentErrorAction extends Action {
  type: actionTypes.UNBOOKMARK_EXPERIMENT_ERROR;
  statusCode: number;
  error: any;
  experimentName: string;
}

export function unbookmarkExperimentRequestActionCreator(
  experimentName: string): UnbookmarkExperimentRequestAction {
  return {
    type: actionTypes.UNBOOKMARK_EXPERIMENT_REQUEST,
    experimentName,
  };
}

export function unbookmarkExperimentSuccessActionCreator(
  experimentName: string): UnbookmarkExperimentSuccessAction {
  return {
    type: actionTypes.UNBOOKMARK_EXPERIMENT_SUCCESS,
    experimentName,
  };
}

export function unbookmarkExperimentErrorActionCreator(statusCode: number,
                                                       error: any,
                                                       experimentName: string): UnbookmarkExperimentErrorAction {
  return {
    type: actionTypes.UNBOOKMARK_EXPERIMENT_ERROR,
    statusCode,
    error,
    experimentName,
  };
}

export type BookmarkExperimentAction =
  BookmarkExperimentRequestAction
  | BookmarkExperimentSuccessAction
  | BookmarkExperimentErrorAction
  | UnbookmarkExperimentRequestAction
  | UnbookmarkExperimentSuccessAction
  | UnbookmarkExperimentErrorAction;

export function bookmark(experimentName: string): any {
  return (dispatch: any, getState: any) => {
    const experimentUrl = getExperimentUrlFromName(experimentName, false);

    dispatch(bookmarkExperimentRequestActionCreator(experimentName));

    return fetch(
      `${BASE_API_URL}${experimentUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        bookmarkExperimentErrorActionCreator,
        'Experiment not found',
        'Failed to bookmark experiment',
        [experimentName]))
      .then(() => dispatch(bookmarkExperimentSuccessActionCreator(experimentName)));
  };
}

export function unbookmark(experimentName: string): any {
  return (dispatch: any, getState: any) => {
    const experimentUrl = getExperimentUrlFromName(experimentName, false);

    dispatch(unbookmarkExperimentRequestActionCreator(experimentName));

    return fetch(
      `${BASE_API_URL}${experimentUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        unbookmarkExperimentErrorActionCreator,
        'Experiment not found',
        'Failed to unbookmark experiment',
        [experimentName]))
      .then(() => dispatch(unbookmarkExperimentSuccessActionCreator(experimentName)));
  };
}
