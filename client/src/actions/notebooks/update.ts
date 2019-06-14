import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { NotebookModel } from '../../models/notebook';
import { getNotebookApiUrlFromName } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface UpdateNotebookRequestAction extends Action {
  type: actionTypes.UPDATE_NOTEBOOK_REQUEST;
  notebookName: string;
}

export interface UpdateNotebookSuccessAction extends Action {
  type: actionTypes.UPDATE_NOTEBOOK_SUCCESS;
  notebook: NotebookModel;
  notebookName: string;
}

export interface UpdateNotebookErrorAction extends Action {
  type: actionTypes.UPDATE_NOTEBOOK_ERROR;
  statusCode: number;
  error: any;
  notebookName: string;
}

export function updateNotebookRequestActionCreator(notebookName: string): UpdateNotebookRequestAction {
  return {
    type: actionTypes.UPDATE_NOTEBOOK_REQUEST,
    notebookName
  };
}

export function updateNotebookSuccessActionCreator(notebook: NotebookModel): UpdateNotebookSuccessAction {
  return {
    type: actionTypes.UPDATE_NOTEBOOK_SUCCESS,
    notebook,
    notebookName: notebook.unique_name
  };
}

export function updateNotebookErrorActionCreator(statusCode: number,
                                                 error: any,
                                                 notebookName: string): UpdateNotebookErrorAction {
  return {
    type: actionTypes.UPDATE_NOTEBOOK_ERROR,
    statusCode,
    error,
    notebookName,
  };
}

export type UpdateNotebookAction =
  UpdateNotebookRequestAction
  | UpdateNotebookSuccessAction
  | UpdateNotebookErrorAction;

export function updateNotebook(notebookName: string, updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const notebookUrl = getNotebookApiUrlFromName(notebookName, false);

    dispatch(updateNotebookRequestActionCreator(notebookName));

    return fetch(
      `${BASE_API_URL}${notebookUrl}`, {
        method: 'PATCH',
        body: JSON.stringify(updateDict),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        }
      })
      .then((response) => stdCreateHandleError(
        response,
        dispatch,
        updateNotebookErrorActionCreator,
        'Notebook not found',
        'Failed to notebook',
        [notebookName]))
      .then((response) => response.json())
      .then((json) => dispatch(updateNotebookSuccessActionCreator(json)))
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(updateNotebookErrorActionCreator(response.status, value, notebookName)));
        } else {
          return dispatch(updateNotebookErrorActionCreator(response.status, response.value, notebookName));
        }
      });
  };
}

