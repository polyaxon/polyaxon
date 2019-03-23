import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getNotebookApiUrl, getNotebookUniqueName } from '../../constants/utils';
import { NotebookModel } from '../../models/notebook';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface GetNotebookRequestAction extends Action {
  type: actionTypes.GET_NOTEBOOK_REQUEST;
  notebookName: string;
}

export interface GetNotebookSuccessAction extends Action {
  type: actionTypes.GET_NOTEBOOK_SUCCESS;
  notebook: NotebookModel;
}

export interface GetNotebookErrorAction extends Action {
  type: actionTypes.GET_NOTEBOOK_ERROR;
  statusCode: number;
  error: any;
  notebookName: string;
}

export function getNotebookRequestActionCreator(notebookName: string): GetNotebookRequestAction {
  return {
    type: actionTypes.GET_NOTEBOOK_REQUEST,
    notebookName
  };
}

export function getNotebookSuccessActionCreator(notebook: NotebookModel): GetNotebookSuccessAction {
  return {
    type: actionTypes.GET_NOTEBOOK_SUCCESS,
    notebook
  };
}

export function getNotebookErrorActionCreator(statusCode: number,
                                              error: any,
                                              notebookName: string): GetNotebookErrorAction {
  return {
    type: actionTypes.GET_NOTEBOOK_ERROR,
    statusCode,
    error,
    notebookName,
  };
}

export type GetNotebookAction =
  GetNotebookRequestAction
  | GetNotebookSuccessAction
  | GetNotebookErrorAction;


export function fetchNotebook(user: string, projectName: string, notebookId: number | string): any {
  return (dispatch: any, getState: any) => {
    const notebookUrl = getNotebookApiUrl(user, projectName, notebookId, false);
    const notebookName = getNotebookUniqueName(user, projectName, notebookId);

    dispatch(getNotebookRequestActionCreator(notebookName));

    return fetch(
      `${BASE_API_URL}${notebookUrl}`, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        getNotebookErrorActionCreator,
        'Notebook not found',
        'Failed to fetch notebook',
        [notebookName]))
      .then((response) => response.json())
      .then((json) => dispatch(getNotebookSuccessActionCreator(json)));
  };
}
