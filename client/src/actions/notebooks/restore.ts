import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getNotebookApiUrlFromName } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface RestoreNotebookRequestAction extends Action {
  type: actionTypes.RESTORE_NOTEBOOK_REQUEST;
  notebookName: string;
}

export interface RestoreNotebookSuccessAction extends Action {
  type: actionTypes.RESTORE_NOTEBOOK_SUCCESS;
  notebookName: string;
}

export interface RestoreNotebookErrorAction extends Action {
  type: actionTypes.RESTORE_NOTEBOOK_ERROR;
  statusCode: number;
  error: any;
  notebookName: string;
}

export function restoreNotebookRequestActionCreator(notebookName: string): RestoreNotebookRequestAction {
  return {
    type: actionTypes.RESTORE_NOTEBOOK_REQUEST,
    notebookName
  };
}

export function restoreNotebookSuccessActionCreator(notebookName: string): RestoreNotebookSuccessAction {
  return {
    type: actionTypes.RESTORE_NOTEBOOK_SUCCESS,
    notebookName
  };
}

export function restoreNotebookErrorActionCreator(statusCode: number,
                                                  error: any,
                                                  notebookName: string): RestoreNotebookErrorAction {
  return {
    type: actionTypes.RESTORE_NOTEBOOK_ERROR,
    statusCode,
    error,
    notebookName
  };
}

export type RestoreNotebookAction =
  RestoreNotebookRequestAction
  | RestoreNotebookSuccessAction
  | RestoreNotebookErrorAction;

export function restoreNotebook(notebookName: string): any {
  return (dispatch: any, getState: any) => {
    const notebookUrl = getNotebookApiUrlFromName(notebookName, false);

    dispatch(restoreNotebookRequestActionCreator(notebookName));

    return fetch(
      `${BASE_API_URL}${notebookUrl}/restore`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        restoreNotebookErrorActionCreator,
        'Notebook not found',
        'Failed to restore notebook',
        [notebookName]))
      .then(() => dispatch(restoreNotebookSuccessActionCreator(notebookName)));
  };
}
