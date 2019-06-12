import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getNotebookApiUrlFromName, getProjectUrl } from '../../urls/utils';
import { stdDeleteHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface DeleteNotebookRequestAction extends Action {
  type: actionTypes.DELETE_NOTEBOOK_REQUEST;
  notebookName: string;
}

export interface DeleteNotebookSuccessAction extends Action {
  type: actionTypes.DELETE_NOTEBOOK_SUCCESS;
  notebookName: string;
}

export interface DeleteNotebookErrorAction extends Action {
  type: actionTypes.DELETE_NOTEBOOK_ERROR;
  statusCode: number;
  error: any;
  notebookName: string;
}

export function deleteNotebookRequestActionCreator(notebookName: string): DeleteNotebookRequestAction {
  return {
    type: actionTypes.DELETE_NOTEBOOK_REQUEST,
    notebookName
  };
}

export function deleteNotebookSuccessActionCreator(notebookName: string): DeleteNotebookSuccessAction {
  return {
    type: actionTypes.DELETE_NOTEBOOK_SUCCESS,
    notebookName
  };
}

export function deleteNotebookErrorActionCreator(statusCode: number,
                                                 error: any,
                                                 notebookName: string): DeleteNotebookErrorAction {
  return {
    type: actionTypes.DELETE_NOTEBOOK_ERROR,
    statusCode,
    error,
    notebookName
  };
}

export type DeleteNotebookAction =
  DeleteNotebookRequestAction
  | DeleteNotebookSuccessAction
  | DeleteNotebookErrorAction;

export function deleteNotebook(notebookName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const notebookUrl = getNotebookApiUrlFromName(notebookName, false);

    dispatch(deleteNotebookRequestActionCreator(notebookName));

    return fetch(
      `${BASE_API_URL}${notebookUrl}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdDeleteHandleError(
        response,
        dispatch,
        deleteNotebookErrorActionCreator,
        'Notebook not found',
        'Failed to delete notebook',
        [notebookName]))
      .then(() => {
        const dispatched = dispatch(deleteNotebookSuccessActionCreator(notebookName));
        if (redirect) {
          const values = notebookName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#notebooks');
        }
        return dispatched;
      });
  };
}
