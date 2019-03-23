import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getNotebookApiUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface StopNotebookRequestAction extends Action {
  type: actionTypes.STOP_NOTEBOOK_REQUEST;
  notebookName: string;
}

export interface StopNotebookSuccessAction extends Action {
  type: actionTypes.STOP_NOTEBOOK_SUCCESS;
  notebookName: string;
}

export interface StopNotebookErrorAction extends Action {
  type: actionTypes.STOP_NOTEBOOK_ERROR;
  statusCode: number;
  error: any;
  notebookName: string;
}

export function stopNotebookRequestActionCreator(notebookName: string): StopNotebookRequestAction {
  return {
    type: actionTypes.STOP_NOTEBOOK_REQUEST,
    notebookName
  };
}

export function stopNotebookSuccessActionCreator(notebookName: string): StopNotebookSuccessAction {
  return {
    type: actionTypes.STOP_NOTEBOOK_SUCCESS,
    notebookName
  };
}

export function stopNotebookErrorActionCreator(statusCode: number,
                                               error: any,
                                               notebookName: string): StopNotebookErrorAction {
  return {
    type: actionTypes.STOP_NOTEBOOK_ERROR,
    statusCode,
    error,
    notebookName
  };
}

export type StopNotebookAction =
  StopNotebookRequestAction
  | StopNotebookSuccessAction
  | StopNotebookErrorAction;

export function stopNotebook(notebookName: string): any {
  return (dispatch: any, getState: any) => {
    const notebookUrl = getNotebookApiUrlFromName(notebookName, false);

    dispatch(stopNotebookRequestActionCreator(notebookName));

    return fetch(
      `${BASE_API_URL}${notebookUrl}/stop`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        stopNotebookErrorActionCreator,
        'Notebook not found',
        'Failed to stop notebook',
        [notebookName]))
      .then(() => dispatch(stopNotebookSuccessActionCreator(notebookName)));
  };
}
